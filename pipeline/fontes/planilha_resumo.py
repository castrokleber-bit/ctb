"""Leitura de `CTB-Resumo.xlsx` — a série histórica publicada, 2000-2024.

`CTB-Resumo.xlsx` é referência de comparação, nunca fonte de dados (CLAUDE.md). Layout:
cada aba tem os anos em blocos de 4 colunas (R$ Bilhões, % PIB, % Total, Per capita),
começando em 2000; os rótulos ficam na coluna A, com blocos de esfera (`UNIÃO`,
`ESTADOS`, `MUNICÍPIOS (6)` — o "(6)" é nota de rodapé, ignorada no casamento) separados
por linha em branco.
"""

from __future__ import annotations

import warnings
from pathlib import Path

CHAVE_BLOCO = {"UNIÃO": "U", "ESTADOS": "E", "MUNICÍPIOS": "M"}


def _mapa_colunas_ano(linha_anos: tuple) -> dict[int, int]:
    """coluna (0-based) da célula 'R$ Bilhões' de cada ano."""
    return {int(v): i for i, v in enumerate(linha_anos) if isinstance(v, (int, float))}


def ler_aba(caminho: Path, aba: str) -> dict[int, dict]:
    """`{ano: {"pib": R$ bi, "populacao": int, "total": R$ bi, "blocos": {"U"/"E"/"M":
    {rótulo: R$ bi}}}}`. `rótulo` mantém a indentação/numeração da planilha tal como
    está lá — quem casa com o dicionário novo faz isso explicitamente, para não esconder
    rótulo não reconhecido.
    """
    import openpyxl

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = openpyxl.load_workbook(caminho, data_only=True, read_only=True)
    ws = wb[aba]
    linhas = list(ws.iter_rows(values_only=True))
    wb.close()

    cols_ano = _mapa_colunas_ano(linhas[2])
    resultado: dict[int, dict] = {ano: {"blocos": {"U": {}, "E": {}, "M": {}}} for ano in cols_ano}

    bloco_atual: str | None = None
    for linha in linhas[3:]:
        rotulo = str(linha[0]).strip() if linha[0] is not None else ""
        if not rotulo:
            continue
        if rotulo.startswith("Transferências Constitucionais"):
            # aba RD ESFERA: a partir daqui é o detalhe de transferências, fora do
            # escopo desta leitura (só o headline por esfera, linhas TOTAL/U/E/M acima).
            break
        chave = rotulo.upper()
        bloco = next((v for k, v in CHAVE_BLOCO.items() if chave == k or chave.startswith(k)), None)
        if bloco is not None:
            bloco_atual = bloco
            # Em "byGOVDetalhado" a linha do bloco é só cabeçalho (valores nas linhas
            # indentadas abaixo). Em "RD ESFERA" ela já carrega o total da esfera — capta
            # os dois casos guardando sob a chave "_total" quando a própria linha tem
            # valor numérico.
            for ano, col_rs in cols_ano.items():
                valor = linha[col_rs]
                if isinstance(valor, (int, float)):
                    resultado[ano]["blocos"][bloco]["_total"] = float(valor)
            continue
        if rotulo.startswith("("):  # nota de rodapé
            continue
        for ano, col_rs in cols_ano.items():
            valor = linha[col_rs]
            if not isinstance(valor, (int, float)):
                continue
            if rotulo == "PIB":
                resultado[ano]["pib"] = float(valor)
            elif rotulo == "População":
                resultado[ano]["populacao"] = int(valor)
            elif rotulo in ("TOTAL", "RECEITA DISPONÍVEL"):
                resultado[ano]["total"] = float(valor)
            elif bloco_atual is not None:
                resultado[ano]["blocos"][bloco_atual][rotulo] = float(valor)

    return resultado
