"""Fase 5 — escreve os JSON que o site estático lê (`dados/publicado/`).

Sem lógica de cálculo aqui: só serializa o que `agregacao.py`/`quadros.py`/
`rd_esfera.py` já produzem. `site/` não tem backend nem banco — lê estes arquivos
direto.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import polars as pl

from pipeline.dominio.agregacao import calcular_ano
from pipeline.dominio.dicionario import carregar_mapeamentos
from pipeline.dominio.manual_uniao import ANOS_DISPONIVEIS as ANOS_FGTS_SISTEMA_S
from pipeline.dominio.quadros import (
    ROTULO_ESFERA, ad_esfera, bases_incidencia, bygov_detalhado, principais_tributos,
    rd_por_esfera_indicadores, total_por_esfera,
)
from pipeline.dominio.rd_esfera import ANOS_DISPONIVEIS as ANOS_RD_ESFERA
from pipeline.dominio.rd_esfera import calcular as calcular_rd_esfera
from pipeline.fontes.http import RAIZ
from pipeline.fontes.sidra import pib_corrente, populacao_brasil

DIR_INTERMEDIARIO = RAIZ / "dados" / "intermediario"
DIR_PUBLICADO = RAIZ / "dados" / "publicado"

VERSAO_SCHEMA = 1


class ErroPublicar(RuntimeError):
    pass


def _linhas(linhas) -> list[dict]:
    return [asdict(l) for l in linhas]


def _transferencias(resultado_rd, origem: str, destino: str) -> list[dict]:
    itens = sorted(
        (t for t in resultado_rd.transferencias if t.bloco_origem == origem and t.bloco_destino == destino),
        key=lambda t: -t.valor_reais,
    )
    return [
        {"modalidade": t.modalidade, "valor_reais": t.valor_reais, "valor_bi": t.valor_reais / 1e9}
        for t in itens
    ]


def _cobertura_municipal(relatorio) -> dict:
    """Mesma `RelatorioImputacao` que `docs/resultado-{ano}.md` usa — nunca rederiva a
    cobertura por conta própria (já houve um bug aqui: contar o DF, que declara
    ISS/IPTU/ITBI no bloco Municípios pela regra do DF, como se fosse um município)."""
    return {
        "total_municipios": relatorio.total_municipios,
        "declarantes": relatorio.declarantes,
        "imputados": len(relatorio.municipios_imputados),
        "pct_populacao_coberta": relatorio.pct_populacao_coberta,
        "pct_receita_imputada": relatorio.pct_receita_imputada,
    }


def _publicar_ano(ano: int) -> dict:
    if not (DIR_INTERMEDIARIO / f"{ano}.parquet").exists():
        raise ErroPublicar(
            f"{ano}: dados/intermediario/{ano}.parquet não existe — rode "
            f"`uv run ctb calcular --anos {ano}` primeiro."
        )
    df, relatorio_imputacao = calcular_ano(ano)
    pib, data_pib = pib_corrente(ano)
    populacao = populacao_brasil(ano)

    ad_totais = total_por_esfera(df)
    total = sum(ad_totais.values())

    saida: dict = {
        "ano": ano,
        "versao_schema": VERSAO_SCHEMA,
        "pib_reais": pib,
        "pib_bi": pib / 1e9,
        "data_extracao_pib": data_pib.isoformat(),
        "populacao": populacao,
        "total_geral": {
            "valor_reais": total,
            "valor_bi": total / 1e9,
            "pct_pib": (total / pib * 100) if pib else 0.0,
        },
        "ad_esfera": {
            esf: {"valor_reais": ad_totais.get(esf, 0.0), "valor_bi": ad_totais.get(esf, 0.0) / 1e9}
            for esf in ("U", "E", "M")
        },
        "quadros": {
            "ad_esfera": {esf: _linhas(l) for esf, l in ad_esfera(df, pib, populacao).items()},
            "bygov_detalhado": {esf: _linhas(l) for esf, l in bygov_detalhado(df, pib, populacao).items()},
            "principais_tributos": _linhas(principais_tributos(df, pib, populacao)),
            "bases_incidencia": _linhas(bases_incidencia(df, pib, populacao)),
        },
        "rd_esfera": None,
        "gap_fgts_sistema_s": ano not in ANOS_FGTS_SISTEMA_S,
        "cobertura_imputacao": _cobertura_municipal(relatorio_imputacao),
    }

    if ano in ANOS_RD_ESFERA:
        resultado_rd = calcular_rd_esfera(ano, df, ad_totais)
        rd_indicadores = rd_por_esfera_indicadores(resultado_rd.rd_por_esfera, pib, populacao)
        saida["rd_esfera"] = {
            "por_esfera": {esf: asdict(rd_indicadores[esf]) for esf in ("U", "E", "M")},
            "transferencias": {
                "uniao_estados": _transferencias(resultado_rd, "U", "E"),
                "uniao_municipios": _transferencias(resultado_rd, "U", "M"),
                "estados_municipios": _transferencias(resultado_rd, "E", "M"),
            },
        }

    return saida


def _publicar_metodologia() -> dict:
    """Página de metodologia gerada a partir do próprio dicionário (PROJETO-CTB.md
    §Fase 5) — nunca um texto solto que pode dessincronizar do que o código realmente
    aplica."""
    saida = {}
    for esfera in ("U", "E", "M"):
        saida[esfera] = [
            {
                "cod_conta": m.cod_conta, "rubrica": m.rubrica, "tributo": m.tributo,
                "base_incidencia": m.base_incidencia, "bloco": m.bloco,
                "vigencia_inicio": m.vigencia_inicio, "vigencia_fim": m.vigencia_fim,
                "observacao": m.observacao,
            }
            for m in carregar_mapeamentos(esfera)
        ]
    return saida


def executar(anos: range) -> Path:
    DIR_PUBLICADO.mkdir(parents=True, exist_ok=True)
    for ano in anos:
        print(f"  publicando {ano}...")
        dados_ano = _publicar_ano(ano)
        destino = DIR_PUBLICADO / f"{ano}.json"
        destino.write_text(json.dumps(dados_ano, ensure_ascii=False, indent=2), encoding="utf-8")

    # anos_disponiveis reflete todo {ano}.json já em disco, não só os processados nesta
    # chamada — republicar um ano isolado (ex.: --anos 2025) nunca pode apagar os outros
    # da lista que o site usa pro seletor de ano.
    anos_publicados = sorted(
        int(p.stem) for p in DIR_PUBLICADO.glob("*.json") if p.stem.isdigit()
    )
    metadados = {
        "anos_disponiveis": anos_publicados,
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "rotulo_esfera": ROTULO_ESFERA,
        "versao_schema": VERSAO_SCHEMA,
    }
    (DIR_PUBLICADO / "metadados.json").write_text(
        json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("  publicando metodologia...")
    (DIR_PUBLICADO / "metodologia.json").write_text(
        json.dumps(_publicar_metodologia(), ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\n{len(anos_publicados)} ano(s) publicado(s) em {DIR_PUBLICADO}")
    return DIR_PUBLICADO
