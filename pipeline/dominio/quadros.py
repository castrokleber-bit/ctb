"""Calcula os indicadores de publicação a partir da tabela intermediária.

CLAUDE.md §Convenções: os quatro indicadores (R$ bi, % PIB, % total, per capita) nunca
são armazenados — são calculados aqui, na publicação. O per capita usa sempre a
população do Brasil inteiro (não a da esfera), mesmo critério do `CTB2024.xlsx`: é o
que faz o per capita de cada linha somar ao per capita do total.

Quatro dos cinco quadros da planilha são construídos até esta passada — ver
`docs/decisoes-pendentes.md` e a Fase 2 do `PROJETO-CTB.md`:

- `bygov_detalhado`: por esfera, aberto por rubrica.
- `bases_incidencia`: agregado por base de incidência.
- `ad_esfera`: os itens mais relevantes de cada esfera, nomeados, resto em "Demais".
- `principais_tributos`: ranking cruzando esferas onde a planilha original cruza.

`RD ESFERA` (depende de transferências constitucionais, com pelo menos duas
modalidades — Salário-Educação e Seguro-Receita ICMS — sem fonte identificada ainda)
fica para uma passada seguinte.
"""

from __future__ import annotations

from dataclasses import dataclass

import polars as pl

from pipeline.dominio.dicionario import carregar_rotulos_base_incidencia

ROTULO_ESFERA = {"U": "União", "E": "Estados", "M": "Municípios"}
ROTULO_CONSOLIDADO = "Setor Público Consolidado"
ESFERAS_COM_CONSOLIDADO = ("U", "E", "M", "consolidado")

# --- AD ESFERA -------------------------------------------------------------------
#
# Reverso-engenheirado do CTB2024.xlsx (aba AD ESFERA, 2026-08-31): não é uma
# categoria econômica aplicada uniformemente — é "os 2 a 4 maiores itens de cada
# esfera, nomeados; o resto em Demais". Conferido exato contra os valores de 2024:
#   Estados: soma do resto (IRRF+ITCD+TAXAS+Previ.Estadual+Contribuições) = 211,532,
#            bate com o "Demais" publicado (211,532).
#   Municípios: soma do resto (IRRF+ITBI+TAXAS+Previd.Municipal+Contribuições) =
#            139,529, bate exato.
#   União: "Impostos" = IR+IPI+IOF+ITR+Comércio Exterior = 994,879, bate exato.
#          "Contribuições Sociais" = Cofins+CSLL+PIS-PASEP+CPMF+Contrib.Seg.Serv.
#          Público+Outras contrib. sociais+Salário Educação+FGTS+Sistema S = 710,864
#          (2026-09-01: FGTS e Sistema S passaram a vir de manual/, ver
#          pipeline/dominio/manual_uniao.py — antes ficavam de fora).
#          "Demais" antigo = Taxas+Contribuições Econômicas+Multas e Dívida Ativa =
#          225,833; sob a opção B não há mais Multas e Dívida Ativa (redistribuída
#          nas rubricas de origem), então "Demais" aqui é Taxas+Contribuições
#          Econômicas (CIDE, sem royalties)+Royalties e Compensações Financeiras.
CATEGORIA_AD_ESFERA_UNIAO = {
    "IR": "Impostos", "IPI": "Impostos", "IOF": "Impostos", "ITR": "Impostos",
    "Imp. sobre Comércio Exterior": "Impostos", "Outros impostos": "Impostos",
    "Cofins": "Contribuições Sociais", "CSLL": "Contribuições Sociais",
    "PIS-PASEP": "Contribuições Sociais", "CPMF": "Contribuições Sociais",
    "Contrib. Seg. Serv. Público": "Contribuições Sociais",
    "Outras contribuições sociais": "Contribuições Sociais",
    "Salário Educação": "Contribuições Sociais",
    "FGTS": "Contribuições Sociais",
    "Sistema S": "Contribuições Sociais",
    "Previdência Social": "Previdência Social",
    "Taxas": "Demais", "Contribuições Econômicas": "Demais",
    "Royalties e Compensações Financeiras": "Demais",
}
ORDEM_AD_ESFERA_UNIAO = ["Impostos", "Contribuições Sociais", "Previdência Social", "Demais"]

# Estados e municípios: só os dois itens nomeados têm entrada; qualquer outra rubrica
# cai em "Demais" pelo padrão do dicionário — é o comportamento correto (Demais é
# catch-all por definição), não uma falha silenciosa.
CATEGORIA_AD_ESFERA_ESTADOS = {"ICMS": "ICMS", "IPVA": "IPVA"}
ORDEM_AD_ESFERA_ESTADOS = ["ICMS", "IPVA", "Demais"]

CATEGORIA_AD_ESFERA_MUNICIPIOS = {"ISS": "ISS", "IPTU": "IPTU"}
ORDEM_AD_ESFERA_MUNICIPIOS = ["ISS", "IPTU", "Demais"]

_AD_ESFERA_POR_ESFERA = {
    "U": (CATEGORIA_AD_ESFERA_UNIAO, ORDEM_AD_ESFERA_UNIAO),
    "E": (CATEGORIA_AD_ESFERA_ESTADOS, ORDEM_AD_ESFERA_ESTADOS),
    "M": (CATEGORIA_AD_ESFERA_MUNICIPIOS, ORDEM_AD_ESFERA_MUNICIPIOS),
}

# --- PRINCIPAIS TRIBUTOS ----------------------------------------------------------
#
# Reverso-engenheirado do CTB2024.xlsx (aba PRINCIPAIS TRIBUTOS, 2026-08-31): a
# maioria das linhas é uma rubrica de uma esfera só (conferido exato contra 2024:
# ICMS, Cofins, IPI, CSLL, PIS-PASEP, IOF, IPVA, ITCD, ITR, CPMF). Três cruzam
# esferas — "Imposto de Renda (Global)" confere exato: IR da União (764,550) +
# IRRF de Estados (81,090) + IRRF de Municípios (48,839) = 894,479. ISS/IPTU/ITBI já
# vêm com a parcela do DF embutida (regra do DF, decisão 2), sem soma adicional.
# "Previdência Social Ampliada" é a soma de RGPS + Previ. Estadual + Previd.
# Municipal — a hipótese aproxima o valor antigo (673,083) mas não fechei ao
# centavo; reportado como está, sem forçar.
#
# Desvio deliberado: a planilha separa Imposto de Importação de Imposto de
# Exportação; o dicionário da União agrega os dois numa conta só (a exportação é
# marginal, <0,3% do grupo). Publicado aqui como "Comércio Exterior" combinado,
# rotulado como tal — mais honesto que fingir separação que não existe no cálculo.
DEFINICOES_PRINCIPAIS_TRIBUTOS: list[tuple[str, list[tuple[str, str]]]] = [
    ("ICMS", [("E", "ICMS")]),
    ("Previdência Social Ampliada", [
        ("U", "Previdência Social"), ("E", "Previ. Estadual"), ("M", "Previd. Municipal"),
    ]),
    ("Imposto de Renda (Global)", [("U", "IR"), ("E", "IRRF"), ("M", "IRRF")]),
    ("Cofins", [("U", "Cofins")]),
    ("IPI", [("U", "IPI")]),
    ("CSLL", [("U", "CSLL")]),
    ("PIS-PASEP", [("U", "PIS-PASEP")]),
    ("ISS", [("M", "ISS")]),
    ("Comércio Exterior (Importação + Exportação)", [("U", "Imp. sobre Comércio Exterior")]),
    ("IPVA", [("E", "IPVA")]),
    ("IPTU", [("M", "IPTU")]),
    ("IOF", [("U", "IOF")]),
    ("ITBI", [("M", "ITBI")]),
    ("ITCD", [("E", "ITCD")]),
    ("ITR", [("U", "ITR")]),
    ("CPMF", [("U", "CPMF")]),
]


@dataclass(frozen=True)
class LinhaQuadro:
    rotulo: str
    valor_reais: float
    valor_bi: float
    pct_pib: float
    pct_total: float
    per_capita: float


def _linha(rotulo: str, valor: float, pib: float, populacao: int, total_geral: float) -> LinhaQuadro:
    return LinhaQuadro(
        rotulo=rotulo,
        valor_reais=valor,
        valor_bi=valor / 1e9,
        pct_pib=(valor / pib * 100) if pib else 0.0,
        pct_total=(valor / total_geral * 100) if total_geral else 0.0,
        per_capita=(valor / populacao) if populacao else 0.0,
    )


def bygov_detalhado(
    df: pl.DataFrame, pib: float, populacao: int
) -> dict[str, list[LinhaQuadro]]:
    """Por esfera (U/E/M), a lista de rubricas ordenada da maior para a menor."""
    total_geral = float(df["valor_reais"].sum())
    agrupado = (
        df.group_by(["esfera", "rubrica"])
        .agg(pl.col("valor_reais").sum())
        .sort("valor_reais", descending=True)
    )
    resultado: dict[str, list[LinhaQuadro]] = {"U": [], "E": [], "M": []}
    for esfera, rubrica, valor in agrupado.iter_rows():
        resultado[esfera].append(_linha(rubrica, valor, pib, populacao, total_geral))
    return resultado


def bases_incidencia(df: pl.DataFrame, pib: float, populacao: int) -> list[LinhaQuadro]:
    """Agregado por base de incidência, cruzando as três esferas.

    `base_incidencia` na tabela intermediária é o identificador snake_case do dicionário
    (`bens_servicos`, `patrimonio`) — nunca publicado cru; `carregar_rotulos_base_incidencia`
    troca pelo rótulo de `bases_incidencia.csv` (acesso direto ao dict, não `.get(...)`:
    todo valor aqui já foi validado contra esse mesmo CSV em `carregar_mapeamentos`, um
    `KeyError` significaria dicionário e validação dessincronizados, não dado inesperado).
    """
    total_geral = float(df["valor_reais"].sum())
    rotulos = carregar_rotulos_base_incidencia()
    agrupado = (
        df.group_by("base_incidencia")
        .agg(pl.col("valor_reais").sum())
        .sort("valor_reais", descending=True)
    )
    return [
        _linha(rotulos[base], valor, pib, populacao, total_geral)
        for base, valor in agrupado.iter_rows()
    ]


def ad_esfera(df: pl.DataFrame, pib: float, populacao: int) -> dict[str, list[LinhaQuadro]]:
    """Os itens mais relevantes de cada esfera, nomeados; o resto em "Demais".

    Ver a regra reverso-engenheirada no comentário de `CATEGORIA_AD_ESFERA_UNIAO`.
    A soma por esfera bate, ao centavo, com `total_por_esfera` — é a mesma tabela,
    outro agrupamento; diferença aqui seria bug, não resíduo esperado.
    """
    total = float(df["valor_reais"].sum())
    resultado: dict[str, list[LinhaQuadro]] = {}
    for esfera, (categorias, ordem) in _AD_ESFERA_POR_ESFERA.items():
        sub = df.filter(pl.col("esfera") == esfera)
        somas: dict[str, float] = {c: 0.0 for c in ordem}
        rubricas_nao_mapeadas = set()
        for rubrica, valor in sub.group_by("rubrica").agg(pl.col("valor_reais").sum()).iter_rows():
            categoria = categorias.get(rubrica)
            if categoria is None:
                categoria = "Demais"
                rubricas_nao_mapeadas.add(rubrica)
            somas[categoria] = somas.get(categoria, 0.0) + valor
        if rubricas_nao_mapeadas:
            print(f"  aviso: esfera {esfera}, rubrica(s) sem categoria nomeada, "
                  f"foram para Demais: {sorted(rubricas_nao_mapeadas)}")
        resultado[esfera] = [_linha(cat, somas[cat], pib, populacao, total) for cat in ordem]
    return resultado


def principais_tributos(df: pl.DataFrame, pib: float, populacao: int) -> list[LinhaQuadro]:
    """Ranking cruzando esferas onde a planilha original cruza — ver
    `DEFINICOES_PRINCIPAIS_TRIBUTOS`. "Demais tributos" é sempre o plugue (total
    geral menos a soma das linhas nomeadas), não uma lista fixa de rubricas.
    """
    total = float(df["valor_reais"].sum())
    somas_por_par = {
        (esfera, rubrica): valor
        for esfera, rubrica, valor in
        df.group_by(["esfera", "rubrica"]).agg(pl.col("valor_reais").sum()).iter_rows()
    }
    linhas = []
    soma_nomeadas = 0.0
    for rotulo, pares in DEFINICOES_PRINCIPAIS_TRIBUTOS:
        valor = sum(somas_por_par.get(par, 0.0) for par in pares)
        soma_nomeadas += valor
        linhas.append(_linha(rotulo, valor, pib, populacao, total))
    linhas.sort(key=lambda l: -l.valor_reais)
    linhas.append(_linha("Demais tributos", total - soma_nomeadas, pib, populacao, total))
    return linhas


def total_geral(df: pl.DataFrame) -> float:
    return float(df["valor_reais"].sum())


def total_por_esfera(df: pl.DataFrame) -> dict[str, float]:
    agrupado = df.group_by("esfera").agg(pl.col("valor_reais").sum())
    return {esfera: valor for esfera, valor in agrupado.iter_rows()}


def rd_por_esfera_indicadores(
    rd_por_esfera: dict[str, float], pib: float, populacao: int
) -> dict[str, LinhaQuadro]:
    """RD ESFERA com os quatro indicadores de publicação, mesmo formato dos outros
    quadros — usa `ROTULO_ESFERA[esf]` como rótulo. Inclui "consolidado" (União +
    Estados + Municípios, o Setor Público Consolidado) como uma quarta linha."""
    total = sum(rd_por_esfera.values())
    resultado = {
        esf: _linha(ROTULO_ESFERA[esf], rd_por_esfera.get(esf, 0.0), pib, populacao, total)
        for esf in ("U", "E", "M")
    }
    resultado["consolidado"] = _linha(ROTULO_CONSOLIDADO, total, pib, populacao, total)
    return resultado


def ad_por_esfera_indicadores(
    ad_por_esfera: dict[str, float], pib: float, populacao: int
) -> dict[str, LinhaQuadro]:
    """AD ESFERA (arrecadação direta) por esfera com os quatro indicadores — mesmo
    formato de `rd_por_esfera_indicadores`, com "consolidado" como quarta linha."""
    total = sum(ad_por_esfera.values())
    resultado = {
        esf: _linha(ROTULO_ESFERA[esf], ad_por_esfera.get(esf, 0.0), pib, populacao, total)
        for esf in ("U", "E", "M")
    }
    resultado["consolidado"] = _linha(ROTULO_CONSOLIDADO, total, pib, populacao, total)
    return resultado


def consolidar_linhas(
    por_esfera: dict[str, list[LinhaQuadro]], pib: float, populacao: int
) -> list[LinhaQuadro]:
    """Soma linhas de mesmo rótulo entre esferas — a visão "Setor Público Consolidado"
    de um quadro aberto por esfera (AD ESFERA, byGOVDetalhado). Rótulos que só existem
    numa esfera (ex.: ICMS, só Estados) aparecem com o valor dessa esfera; rótulos que
    se repetem (ex.: TAXAS, Royalties e Compensações Financeiras, Outros impostos —
    aparecem em mais de uma esfera) são somados numa linha nacional só.
    """
    soma_por_rotulo: dict[str, float] = {}
    ordem: list[str] = []
    for linhas in por_esfera.values():
        for l in linhas:
            if l.rotulo not in soma_por_rotulo:
                ordem.append(l.rotulo)
            soma_por_rotulo[l.rotulo] = soma_por_rotulo.get(l.rotulo, 0.0) + l.valor_reais
    total = sum(soma_por_rotulo.values())
    return [_linha(rotulo, soma_por_rotulo[rotulo], pib, populacao, total) for rotulo in ordem]
