"""Monta a tabela intermediária (formato longo) para um ano.

Uma linha por (esfera de publicação, ente, rubrica, base de incidência). "Esfera" aqui
é o **bloco de publicação** (`U`/`E`/`M`), não o literal `esfera` da DCA — o DF reporta
como esfera `D`, mas parte do que ele declara é publicado no bloco Municípios (regra do
DF, decisão 2). `id_ente` preserva quem de fato declarou.

Os quatro indicadores (R$ bi, % PIB, % total, per capita) não são calculados aqui —
CLAUDE.md §Convenções: "calculados na publicação, nunca armazenados". Isso é trabalho
de `pipeline/dominio/quadros.py`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import polars as pl

from pipeline.dominio.dicionario import (
    ErroDicionario, carregar_mapeamentos, carregar_politica_colunas, classificar,
)
from pipeline.dominio.imputacao import RelatorioImputacao, imputar_municipios
from pipeline.dominio import manual_uniao
from pipeline.fontes.cache import DIR_ENTES, esferas_por_ente, itens_dca
from pipeline.fontes.http import RAIZ
from pipeline.fontes.sidra import populacao_municipios

# Versão do dicionário usada no cálculo. Constante datada, não um hash automático —
# incremente manualmente quando uma mudança no dicionário alterar número publicado
# (regra 6 do CLAUDE.md exige reportar o diff; esta versão é o que permite rastrear
# qual dicionário produziu qual número).
VERSAO_DICIONARIO = "2026-08-31"

FONTE_DCA = "Siconfi DCA"
FONTE_IMPUTADO = "imputado"
FONTE_MANUAL = "manual"
METODO_IMPUTACAO = "per_capita_faixa_fpm"

DIR_INTERMEDIARIO = RAIZ / "dados" / "intermediario"

COLUNAS = [
    "ano", "esfera", "id_ente", "nome_ente", "rubrica", "base_incidencia",
    "valor_reais", "imputado", "metodo_imputacao", "fonte", "versao_dicionario",
]


class ErroAgregacao(RuntimeError):
    """Uma conta ficou órfã na hora de agregar — o dicionário mudou ou o cache tem
    dado novo que a Fase 1 não viu. Nunca é ignorado."""


def _nomes_entes() -> dict[str, str]:
    entes = json.loads(DIR_ENTES.read_text(encoding="utf-8"))["items"]
    return {str(e["cod_ibge"]): e["ente"] for e in entes}


def _falhar_se_orfas(orfas: list[str], esfera: str, ente: str, ano: int) -> None:
    if orfas:
        raise ErroAgregacao(
            f"{ano}, ente {ente} (esfera {esfera}): {len(orfas)} conta(s) órfã(s) "
            f"apareceram na agregação que a Fase 1 não tinha visto: {orfas}. "
            "Rode `uv run ctb dicionario validar` para confirmar e atualize o "
            "dicionário antes de recalcular."
        )


def _linhas_de_ente(
    ano: int, cod: str, nome: str, valores: dict[tuple[str, str, str], float],
) -> list[dict]:
    return [
        dict(
            ano=ano, esfera=bloco, id_ente=cod, nome_ente=nome, rubrica=rubrica,
            base_incidencia=base, valor_reais=valor, imputado=False,
            metodo_imputacao=None, fonte=FONTE_DCA, versao_dicionario=VERSAO_DICIONARIO,
        )
        for (bloco, rubrica, base), valor in valores.items()
    ]


def _base_dominante_por_rubrica(linhas_declaradas: list[dict]) -> dict[str, str]:
    """Para rubricas com mais de uma base_incidencia (ex.: "Outros impostos"),
    escolhe a que concentra mais receita declarada — usada só para rotular as linhas
    imputadas, que são calculadas por rubrica (CLAUDE.md §Imputação municipal), sem
    granularidade de base.
    """
    soma: dict[tuple[str, str], float] = {}
    for l in linhas_declaradas:
        if l["esfera"] != "M":
            continue
        chave = (l["rubrica"], l["base_incidencia"])
        soma[chave] = soma.get(chave, 0.0) + l["valor_reais"]
    dominante: dict[str, str] = {}
    melhor: dict[str, float] = {}
    for (rubrica, base), total in soma.items():
        if rubrica not in melhor or total > melhor[rubrica]:
            melhor[rubrica] = total
            dominante[rubrica] = base
    return dominante


def _populacoes_com_fallback(ano: int, forcar_sidra: bool) -> dict[str, int]:
    """SIDRA às vezes não tem estimativa para um município específico (visto em 2024:
    Boa Esperança do Norte-MT, 5101837). Sem população, `imputar_municipios` excluiria
    o município do universo inteiro sem avisar — nunca demos passe livre a isso.

    Usa o cadastro de entes do Siconfi como respaldo (ele já traz um campo
    `populacao`, é a mesma fonte usada em todo o resto do projeto) e avisa qual
    município precisou do respaldo, para nunca ficar escondido.
    """
    populacoes = dict(populacao_municipios(ano, forcar=forcar_sidra))
    entes = json.loads(DIR_ENTES.read_text(encoding="utf-8"))["items"]
    faltando = []
    for e in entes:
        cod = str(e["cod_ibge"])
        if e["esfera"] == "M" and cod not in populacoes:
            populacoes[cod] = e["populacao"]
            faltando.append(f"{cod} ({e['ente']}, {e['populacao']:,} hab. via cadastro Siconfi)")
    if faltando:
        print(f"  aviso: {len(faltando)} município(s) sem população no SIDRA, "
              f"usando o cadastro Siconfi como respaldo: {', '.join(faltando)}")
    return populacoes


def calcular_ano(ano: int, *, forcar_sidra: bool = False) -> tuple[pl.DataFrame, RelatorioImputacao]:
    esferas = esferas_por_ente()
    nomes = _nomes_entes()
    politica = carregar_politica_colunas()

    linhas: list[dict] = []

    # União
    mapas_u = carregar_mapeamentos("U")
    for cod, itens in itens_dca(ano, "U", esferas).items():
        valores, orfas = classificar(itens, "U", ano, mapas_u, politica, por_bloco=True, com_base=True)
        _falhar_se_orfas(orfas, "U", cod, ano)
        linhas += _linhas_de_ente(ano, cod, nomes.get(cod, cod), valores)

    # FGTS e Sistema S — sem conta na DCA, vêm de manual/ (ver manual_uniao.py e
    # manual/README.md para fonte e data de cada valor).
    for rubrica, valor in manual_uniao.carregar(ano).items():
        linhas.append(dict(
            ano=ano, esfera="U", id_ente="1", nome_ente=nomes.get("1", "União"),
            rubrica=rubrica, base_incidencia=manual_uniao.BASE_INCIDENCIA,
            valor_reais=valor, imputado=False, metodo_imputacao=None,
            fonte=FONTE_MANUAL, versao_dicionario=VERSAO_DICIONARIO,
        ))

    # Estados + DF — cada ente com seu literal esfera (E ou D) para a política de
    # colunas, mas sempre com o dicionário de estados; o bloco de publicação sai do
    # próprio dicionário (regra do DF).
    mapas_e = carregar_mapeamentos("E")
    for cod, itens in itens_dca(ano, "E", esferas).items():
        esfera_real = esferas[cod]
        valores, orfas = classificar(itens, esfera_real, ano, mapas_e, politica, por_bloco=True, com_base=True)
        _falhar_se_orfas(orfas, esfera_real, cod, ano)
        linhas += _linhas_de_ente(ano, cod, nomes.get(cod, cod), valores)

    # Municípios declarantes
    mapas_m = carregar_mapeamentos("M")
    cache_m = itens_dca(ano, "M", esferas)
    for cod, itens in cache_m.items():
        if not itens:
            continue
        valores, orfas = classificar(itens, "M", ano, mapas_m, politica, por_bloco=True, com_base=True)
        _falhar_se_orfas(orfas, "M", cod, ano)
        linhas += _linhas_de_ente(ano, cod, nomes.get(cod, cod), valores)

    # Municípios imputados
    populacoes = _populacoes_com_fallback(ano, forcar_sidra)
    imputados, relatorio = imputar_municipios(ano, mapas_m, politica, populacoes)
    base_dominante = _base_dominante_por_rubrica(linhas)
    for cod, valores_rubrica in imputados.items():
        for rubrica, valor in valores_rubrica.items():
            linhas.append(dict(
                ano=ano, esfera="M", id_ente=cod, nome_ente=nomes.get(cod, cod),
                rubrica=rubrica, base_incidencia=base_dominante.get(rubrica, "demais"),
                valor_reais=valor, imputado=True, metodo_imputacao=METODO_IMPUTACAO,
                fonte=FONTE_IMPUTADO, versao_dicionario=VERSAO_DICIONARIO,
            ))

    if not linhas:
        raise ErroAgregacao(f"{ano}: nenhuma linha produzida — cache vazio?")

    df = pl.DataFrame(linhas, schema={
        "ano": pl.Int32, "esfera": pl.Utf8, "id_ente": pl.Utf8, "nome_ente": pl.Utf8,
        "rubrica": pl.Utf8, "base_incidencia": pl.Utf8, "valor_reais": pl.Float64,
        "imputado": pl.Boolean, "metodo_imputacao": pl.Utf8, "fonte": pl.Utf8,
        "versao_dicionario": pl.Utf8,
    })
    DIR_INTERMEDIARIO.mkdir(parents=True, exist_ok=True)
    df.write_parquet(DIR_INTERMEDIARIO / f"{ano}.parquet")
    return df, relatorio
