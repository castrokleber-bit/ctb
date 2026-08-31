"""Calcula os indicadores de publicação a partir da tabela intermediária.

CLAUDE.md §Convenções: os quatro indicadores (R$ bi, % PIB, % total, per capita) nunca
são armazenados — são calculados aqui, na publicação. O per capita usa sempre a
população do Brasil inteiro (não a da esfera), mesmo critério do `CTB2024.xlsx`: é o
que faz o per capita de cada linha somar ao per capita do total.

Só dois dos cinco quadros da planilha são construídos nesta passada — ver
`docs/decisoes-pendentes.md` e a Fase 2 do `PROJETO-CTB.md`:

- `bygov_detalhado`: por esfera, aberto por rubrica.
- `bases_incidencia`: agregado por base de incidência.

AD ESFERA (categoria econômica), PRINCIPAIS TRIBUTOS (agregação cruzando esferas) e
RD ESFERA (depende de transferências) ficam para uma passada seguinte.
"""

from __future__ import annotations

from dataclasses import dataclass

import polars as pl

ROTULO_ESFERA = {"U": "União", "E": "Estados", "M": "Municípios"}


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
    """Agregado por base de incidência, cruzando as três esferas."""
    total_geral = float(df["valor_reais"].sum())
    agrupado = (
        df.group_by("base_incidencia")
        .agg(pl.col("valor_reais").sum())
        .sort("valor_reais", descending=True)
    )
    return [
        _linha(base, valor, pib, populacao, total_geral)
        for base, valor in agrupado.iter_rows()
    ]


def total_geral(df: pl.DataFrame) -> float:
    return float(df["valor_reais"].sum())


def total_por_esfera(df: pl.DataFrame) -> dict[str, float]:
    agrupado = df.group_by("esfera").agg(pl.col("valor_reais").sum())
    return {esfera: valor for esfera, valor in agrupado.iter_rows()}
