"""Imputação de municípios sem DCA no ano.

Procedimento do `PROJETO-CTB.md` §5 / `CLAUDE.md` §Imputação municipal: receita
tributária per capita média da faixa populacional, calculada por rubrica — nunca sobre
o total agregado, senão a composição tributária municipal fica distorcida.

Faixas: as 18 do FPM Interior (Decreto-Lei 1.881/1981), em
`dicionario/faixas_populacionais.csv` — decisão 3.
"""

from __future__ import annotations

import csv
import statistics
from dataclasses import dataclass
from pathlib import Path

from pipeline.dominio.dicionario import Mapeamento, classificar
from pipeline.fontes.cache import esferas_por_ente, itens_dca
from pipeline.fontes.http import RAIZ

LIMIAR_DECLARANTES = 30  # PROJETO-CTB.md §5
LIMIAR_PARADA = 500_000  # idem


class ErroImputacao(RuntimeError):
    """Salvaguarda disparada: nunca contornada silenciosamente."""


@dataclass(frozen=True)
class Faixa:
    numero: int
    descricao: str
    minimo: int
    maximo: float  # pode ser +inf


@dataclass(frozen=True)
class RelatorioImputacao:
    ano: int
    total_municipios: int
    declarantes: int
    municipios_imputados: list[str]
    populacao_coberta: int
    populacao_total: int
    receita_declarada: float
    receita_imputada: float
    faixas_mescladas: dict[int, list[int]]  # faixa fina -> faixas cujo pool foi somado

    @property
    def pct_populacao_coberta(self) -> float:
        return self.populacao_coberta / self.populacao_total * 100

    @property
    def pct_receita_imputada(self) -> float:
        total = self.receita_declarada + self.receita_imputada
        return self.receita_imputada / total * 100 if total else 0.0


def carregar_faixas() -> list[Faixa]:
    caminho = RAIZ / "dicionario" / "faixas_populacionais.csv"
    if not caminho.exists():
        raise ErroImputacao(f"faixas populacionais ausentes: {caminho}")
    faixas = []
    with caminho.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            maximo = float(r["populacao_max"]) if r["populacao_max"].strip() else float("inf")
            faixas.append(Faixa(
                int(r["faixa"]), r["descricao"], int(r["populacao_min"]), maximo,
            ))
    if not faixas:
        raise ErroImputacao(f"nenhuma faixa lida de {caminho}")
    return sorted(faixas, key=lambda f: f.numero)


def faixa_de(populacao: int, faixas: list[Faixa]) -> Faixa:
    for f in faixas:
        if f.minimo <= populacao <= f.maximo:
            return f
    raise ErroImputacao(
        f"população {populacao:,} não cai em nenhuma faixa — "
        "dicionario/faixas_populacionais.csv está incompleto"
    )


def _pool_para_media(numero: int, faixas: list[Faixa], declarantes_por_faixa: dict[int, int]
                     ) -> tuple[list[int], dict[int, list[int]]]:
    """Faixas cujo conjunto de declarantes entra no cálculo da média de `numero`.

    Se a própria faixa já tem declarantes suficientes, o pool é só ela. Senão, mescla
    com a faixa vizinha mais próxima em população (a de número adjacente que ainda não
    está no pool), em cascata, até atingir o limiar ou esgotar as faixas.
    """
    ordenadas = sorted(faixas, key=lambda f: f.numero)
    indice = {f.numero: i for i, f in enumerate(ordenadas)}
    pos = indice[numero]
    pool = {numero}
    total = declarantes_por_faixa.get(numero, 0)
    esquerda, direita = pos - 1, pos + 1
    while total < LIMIAR_DECLARANTES and (esquerda >= 0 or direita < len(ordenadas)):
        cand_e = ordenadas[esquerda].numero if esquerda >= 0 else None
        cand_d = ordenadas[direita].numero if direita < len(ordenadas) else None
        # prioriza o vizinho com mais declarantes disponíveis, para convergir mais rápido
        if cand_e is not None and (
            cand_d is None
            or declarantes_por_faixa.get(cand_e, 0) >= declarantes_por_faixa.get(cand_d, 0)
        ):
            pool.add(cand_e)
            total += declarantes_por_faixa.get(cand_e, 0)
            esquerda -= 1
        elif cand_d is not None:
            pool.add(cand_d)
            total += declarantes_por_faixa.get(cand_d, 0)
            direita += 1
        else:
            break
    mesclas = sorted(pool - {numero})
    return sorted(pool), ({numero: mesclas} if mesclas else {})


def imputar_municipios(
    ano: int,
    mapas: list[Mapeamento],
    politica: dict[tuple[str, str], str],
    populacoes: dict[str, int],
) -> tuple[dict[str, dict[str, float]], RelatorioImputacao]:
    """Devolve `(valores_por_municipio_faltante, relatorio)`.

    `valores_por_municipio_faltante`: cod_ibge -> {rubrica: valor_imputado_reais}.
    Todo valor aqui é imputado por definição — quem monta a tabela final marca
    `imputado=True` e `metodo_imputacao="per_capita_faixa_fpm"` para essas linhas.
    """
    esferas = esferas_por_ente()
    uf_do_df = {cod for cod, e in esferas.items() if e == "D"}
    todos = {
        cod: pop for cod, pop in populacoes.items()
        if esferas.get(cod) == "M" and cod[:2] not in uf_do_df
    }
    if not todos:
        raise ErroImputacao("nenhum município no universo — população não carregada?")

    cache = itens_dca(ano, "M", esferas)
    declarantes = {cod for cod, itens in cache.items() if itens and cod in todos}
    faltantes = sorted(set(todos) - declarantes)

    faixas = carregar_faixas()
    faixa_do_municipio = {cod: faixa_de(pop, faixas).numero for cod, pop in todos.items()}

    grandes_ausentes = [
        cod for cod in faltantes
        if todos[cod] > LIMIAR_PARADA
    ]
    if grandes_ausentes:
        detalhes = ", ".join(f"{cod} ({todos[cod]:,} hab.)" for cod in grandes_ausentes)
        raise ErroImputacao(
            f"{ano}: município(s) acima de {LIMIAR_PARADA:,} habitantes sem DCA: "
            f"{detalhes}. Imputar pela média da faixa é inaceitável neste porte — "
            "decisão manual necessária (PROJETO-CTB.md §5)."
        )

    # valores por rubrica de cada declarante, e contagem de declarantes por faixa
    rubricas_por_municipio: dict[str, dict[str, float]] = {}
    for cod in declarantes:
        valores, _ = classificar(cache[cod], "M", ano, mapas, politica)
        rubricas_por_municipio[cod] = valores

    declarantes_por_faixa: dict[int, int] = {f.numero: 0 for f in faixas}
    for cod in declarantes:
        declarantes_por_faixa[faixa_do_municipio[cod]] += 1

    rubricas_do_dicionario = sorted({m.rubrica for m in mapas})

    faixas_mescladas: dict[int, list[int]] = {}
    per_capita_por_faixa: dict[int, dict[str, float]] = {}
    for f in faixas:
        pool_faixas, mesclas = _pool_para_media(f.numero, faixas, declarantes_por_faixa)
        faixas_mescladas.update(mesclas)
        cods_pool = [c for c in declarantes if faixa_do_municipio[c] in pool_faixas]
        pop_pool = sum(todos[c] for c in cods_pool)
        media: dict[str, float] = {}
        for rubrica in rubricas_do_dicionario:
            soma_rubrica = sum(rubricas_por_municipio[c].get(rubrica, 0.0) for c in cods_pool)
            media[rubrica] = (soma_rubrica / pop_pool) if pop_pool else 0.0
        per_capita_por_faixa[f.numero] = media

    imputados: dict[str, dict[str, float]] = {}
    receita_imputada_total = 0.0
    for cod in faltantes:
        f = faixa_do_municipio[cod]
        pop = todos[cod]
        valores = {rub: taxa * pop for rub, taxa in per_capita_por_faixa[f].items()}
        imputados[cod] = valores
        receita_imputada_total += sum(valores.values())

    receita_declarada_total = sum(
        sum(v.values()) for v in rubricas_por_municipio.values()
    )
    relatorio = RelatorioImputacao(
        ano=ano,
        total_municipios=len(todos),
        declarantes=len(declarantes),
        municipios_imputados=faltantes,
        populacao_coberta=sum(todos[c] for c in declarantes),
        populacao_total=sum(todos.values()),
        receita_declarada=receita_declarada_total,
        receita_imputada=receita_imputada_total,
        faixas_mescladas=faixas_mescladas,
    )
    return imputados, relatorio
