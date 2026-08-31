"""Leitura do cache da DCA já baixado — sem ir à rede.

Usado por tudo que precisa iterar sobre os itens de um ou mais entes de uma esfera para
um ano: o validador do dicionário (Fase 1) e a agregação/imputação (Fase 2). Extraído de
`pipeline/dominio/validar.py` para não duplicar entre os dois.
"""

from __future__ import annotations

import json

from pipeline.fontes.http import RAIZ

DIR_CACHE_DCA = RAIZ / "dados" / "bruto" / "siconfi_dca"
DIR_ENTES = RAIZ / "dados" / "bruto" / "siconfi_entes" / "cadastro" / "entes.json"

# O DF usa o dicionário dos estados: entrega uma DCA só, com competências das duas
# esferas. A separação acontece na coluna `bloco` do dicionário, não na leitura.
ESFERAS_DO_DICIONARIO = {"U": ("U",), "E": ("E", "D"), "M": ("M",)}


def esferas_por_ente() -> dict[str, str]:
    """cod_ibge (string) -> esfera ('U', 'E', 'D' ou 'M')."""
    entes = json.loads(DIR_ENTES.read_text(encoding="utf-8"))["items"]
    return {str(e["cod_ibge"]): e["esfera"] for e in entes}


def itens_dca(ano: int, esfera_alvo: str, esferas: dict[str, str]) -> dict[str, list[dict]]:
    """cod_ibge do ente -> itens crus da DCA daquele ano, só para a esfera pedida.

    Lê do cache; não busca nada na rede. Um dicionário vazio significa "ano não
    cacheado", não "sem dados" — quem chama decide se isso é erro.
    """
    dir_ano = DIR_CACHE_DCA / str(ano)
    if not dir_ano.exists():
        return {}
    aceitas = ESFERAS_DO_DICIONARIO[esfera_alvo]
    por_ente = {}
    for arq in dir_ano.iterdir():
        if esferas.get(arq.stem) not in aceitas:
            continue
        por_ente[arq.stem] = json.loads(arq.read_text(encoding="utf-8")).get("items", [])
    return por_ente
