"""Leitura da aba `byGOVDetalhado` da planilha de referência.

`CTB2024.xlsx` é especificação e referência de comparação — nunca fonte de dados
(CLAUDE.md). Isto só lê os rótulos e valores publicados para comparar contra o que o
pipeline calcula; não alimenta nenhum cálculo.
"""

from __future__ import annotations

import warnings
from pathlib import Path

CHAVE_BLOCO = {"UNIÃO": "U", "ESTADOS": "E", "MUNICÍPIOS": "M", "MUNICIPIOS": "M"}


def publicado_por_esfera(caminho: Path) -> dict[str, dict[str, float]]:
    """esfera ('U'/'E'/'M') -> {rótulo da linha: valor publicado em R$ bi}."""
    import openpyxl

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = openpyxl.load_workbook(caminho, data_only=True, read_only=True)
    blocos: dict[str, dict[str, float]] = {"U": {}, "E": {}, "M": {}}
    atual: str | None = None
    try:
        for linha in wb["byGOVDetalhado"].iter_rows(max_col=2, values_only=True):
            rotulo = str(linha[0]).strip() if linha[0] is not None else ""
            chave = rotulo.upper()
            bloco = next((v for k, v in CHAVE_BLOCO.items() if chave == k or chave.startswith(k)), None)
            if bloco is not None:
                atual = bloco
                continue
            if atual and rotulo and isinstance(linha[1], (int, float)):
                blocos[atual][rotulo] = float(linha[1])
    finally:
        wb.close()
    return blocos
