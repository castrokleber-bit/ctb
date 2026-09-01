"""FGTS e Sistema S — rubricas da União sem conta na DCA, vindas de `manual/`.

Fecha o maior gap conhecido do projeto (CLAUDE.md §Fontes: "FGTS (CEF) e Sistema S (RFB)
só em manual/"). Fonte, data e método de cada valor estão declarados em
`manual/README.md` e em cada linha de `manual/fgts_sistema_s.csv` (regra 1 do
CLAUDE.md). Cobre 2016-2025.
"""

from __future__ import annotations

import csv

from pipeline.fontes.http import RAIZ

ARQUIVO = RAIZ / "manual" / "fgts_sistema_s.csv"
BASE_INCIDENCIA = "salarios"
ANOS_DISPONIVEIS = range(2016, 2026)


class ErroManualUniao(RuntimeError):
    pass


def carregar(ano: int) -> dict[str, float]:
    """rubrica -> valor_reais para `ano`. Devolve `{}` (com aviso) para anos sem fonte
    ainda — nunca inventa um valor para preencher a lacuna."""
    if not ARQUIVO.exists():
        raise ErroManualUniao(f"arquivo manual não encontrado: {ARQUIVO}")
    valores: dict[str, float] = {}
    with ARQUIVO.open(encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f, delimiter=";")
        for linha in leitor:
            if int(linha["ano"]) != ano:
                continue
            valores[linha["rubrica"]] = float(linha["valor_reais"])
    if not valores:
        print(f"  aviso: manual/fgts_sistema_s.csv não tem FGTS/Sistema S para {ano} — "
              "linhas não incluídas (gap conhecido, ver manual/README.md).")
    return valores
