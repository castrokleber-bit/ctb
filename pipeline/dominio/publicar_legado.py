"""Publica 2000-2015 direto de `manual/ctb_resumo_*.csv` — metodologia antiga do
`CTB-Resumo.xlsx`, sem passar pelo Siconfi/DCA nem pelo dicionário de classificação.

Exceção deliberada à regra de escopo do CLAUDE.md ("CTB-Resumo.xlsx é especificação e
referência de comparação, nunca fonte de dados") — pedido explícito do usuário em
2026-09-02, pra estender a série pra trás de 2016 sem reconstruir o dicionário pra eras
do plano de contas anteriores. Ver `manual/README.md` §`ctb_resumo_*.csv` pro raciocínio
completo e pra consequência que isso tem nos quadros (a linha "Multas e Dívida Ativa"
some em 2016 — mudança de metodologia, não erro).

Mesmo formato de JSON que `publicar.py::_publicar_ano` produz pros anos 2016+, com
`"fonte_dados": "ctb_resumo_legado"` em vez de `"siconfi_dca"` — o site sinaliza a
diferença, não esconde. `cobertura_imputacao` fica `None` (não existe declarante
municipal nessa fonte) e `gap_fgts_sistema_s` fica `False` (a planilha antiga já inclui
FGTS/Sistema S nos próprios números da União).
"""

from __future__ import annotations

import csv
from dataclasses import asdict

from pipeline.dominio.quadros import (
    ESFERAS_COM_CONSOLIDADO, _linha, ad_por_esfera_indicadores, consolidar_linhas,
    rd_por_esfera_indicadores,
)
from pipeline.fontes.http import RAIZ

DIR_MANUAL = RAIZ / "manual"
ANOS_DISPONIVEIS = range(2000, 2016)


class ErroPublicarLegado(RuntimeError):
    pass


def _ler_csv(nome: str) -> list[dict]:
    caminho = DIR_MANUAL / nome
    if not caminho.exists():
        raise ErroPublicarLegado(f"arquivo manual ausente: {caminho}")
    with caminho.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def _do_ano(linhas: list[dict], ano: int) -> list[dict]:
    return [r for r in linhas if int(r["ano"]) == ano]


def _pib_populacao(ano: int) -> tuple[float, int, str]:
    linhas = _do_ano(_ler_csv("ctb_resumo_pib_populacao.csv"), ano)
    if not linhas:
        raise ErroPublicarLegado(f"{ano}: ausente em ctb_resumo_pib_populacao.csv")
    r = linhas[0]
    return float(r["pib_reais"]), int(r["populacao"]), r["data_extracao"]


def _agrupar_por_esfera(linhas: list[dict], chave: str) -> dict[str, dict[str, float]]:
    por_esfera: dict[str, dict[str, float]] = {"U": {}, "E": {}, "M": {}}
    for r in linhas:
        por_esfera[r["esfera"]][r[chave]] = float(r["valor_reais"])
    return por_esfera


def _linhas_quadro(valores: dict[str, float], pib, populacao, total, *, ordenar=False) -> list:
    linhas = [_linha(rotulo, valor, pib, populacao, total) for rotulo, valor in valores.items()]
    if ordenar:
        linhas.sort(key=lambda l: -l.valor_reais)
    return linhas


def publicar_ano_legado(ano: int) -> dict:
    if ano not in ANOS_DISPONIVEIS:
        raise ErroPublicarLegado(
            f"{ano} fora do intervalo legado (2000-2015) — use publicar.py para 2016+"
        )

    pib, populacao, data_extracao_pib = _pib_populacao(ano)

    bygov = _agrupar_por_esfera(_do_ano(_ler_csv("ctb_resumo_bygov_detalhado.csv"), ano), "rubrica")
    ad_categorias = _agrupar_por_esfera(_do_ano(_ler_csv("ctb_resumo_ad_esfera.csv"), ano), "categoria")

    ad_totais = {esf: sum(v.values()) for esf, v in bygov.items()}
    total = sum(ad_totais.values())

    # byGOVDetalhado é ordenado por valor (mesma convenção de `quadros.bygov_detalhado`);
    # AD ESFERA mantém a ordem fixa das categorias da própria planilha (mesma convenção
    # de `quadros.ad_esfera`, que usa `ORDEM_AD_ESFERA_*` em vez de ordenar por valor).
    quadro_bygov = {esf: _linhas_quadro(v, pib, populacao, total, ordenar=True) for esf, v in bygov.items()}
    quadro_ad = {esf: _linhas_quadro(v, pib, populacao, total) for esf, v in ad_categorias.items()}

    principais_valores = {
        r["tributo"]: float(r["valor_reais"]) for r in _do_ano(_ler_csv("ctb_resumo_principais_tributos.csv"), ano)
    }
    demais_tributos = principais_valores.pop("Demais tributos", 0.0)
    principais_linhas = _linhas_quadro(principais_valores, pib, populacao, total, ordenar=True)
    principais_linhas.append(_linha("Demais tributos", demais_tributos, pib, populacao, total))

    bases_valores = {
        r["base_incidencia"]: float(r["valor_reais"]) for r in _do_ano(_ler_csv("ctb_resumo_bases_incidencia.csv"), ano)
    }
    bases_linhas = _linhas_quadro(bases_valores, pib, populacao, total, ordenar=True)

    rd_totais = {r["esfera"]: float(r["valor_reais"]) for r in _do_ano(_ler_csv("ctb_resumo_rd_esfera.csv"), ano)}
    rd_indicadores = rd_por_esfera_indicadores(rd_totais, pib, populacao)

    transferencias_ano = _do_ano(_ler_csv("ctb_resumo_rd_transferencias.csv"), ano)

    def _bloco(origem: str, destino: str) -> list[dict]:
        itens = sorted(
            (r for r in transferencias_ano if r["bloco_origem"] == origem and r["bloco_destino"] == destino),
            key=lambda r: -float(r["valor_reais"]),
        )
        return [
            {
                "modalidade": r["modalidade"],
                "valor_reais": float(r["valor_reais"]),
                "valor_bi": float(r["valor_reais"]) / 1e9,
            }
            for r in itens
        ]

    return {
        "ano": ano,
        "versao_schema": 1,
        "pib_reais": pib,
        "pib_bi": pib / 1e9,
        "data_extracao_pib": data_extracao_pib,
        "populacao": populacao,
        "fonte_dados": "ctb_resumo_legado",
        "total_geral": {
            "valor_reais": total,
            "valor_bi": total / 1e9,
            "pct_pib": (total / pib * 100) if pib else 0.0,
        },
        "ad_esfera": {
            esf: asdict(l) for esf, l in ad_por_esfera_indicadores(ad_totais, pib, populacao).items()
        },
        "quadros": {
            "ad_esfera": {
                **{esf: [asdict(l) for l in linhas] for esf, linhas in quadro_ad.items()},
                "consolidado": [asdict(l) for l in consolidar_linhas(quadro_ad, pib, populacao)],
            },
            "bygov_detalhado": {
                **{esf: [asdict(l) for l in linhas] for esf, linhas in quadro_bygov.items()},
                "consolidado": [asdict(l) for l in consolidar_linhas(quadro_bygov, pib, populacao)],
            },
            "principais_tributos": [asdict(l) for l in principais_linhas],
            "bases_incidencia": [asdict(l) for l in bases_linhas],
        },
        "rd_esfera": {
            "por_esfera": {esf: asdict(rd_indicadores[esf]) for esf in ESFERAS_COM_CONSOLIDADO},
            "transferencias": {
                "uniao_estados": _bloco("U", "E"),
                "uniao_municipios": _bloco("U", "M"),
                "estados_municipios": _bloco("E", "M"),
            },
        },
        "gap_fgts_sistema_s": False,
        "cobertura_imputacao": None,
    }
