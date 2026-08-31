"""Linha de comando do projeto CTB.

Hoje só a Fase 0 está implementada. Os demais subcomandos previstos no CLAUDE.md
(`ingerir`, `calcular`, `cobertura`, `publicar`, `comparar-historico`) recusam-se a
rodar com uma mensagem que diz em que fase eles entram — melhor que um stub que
devolve um resultado vazio.
"""

from __future__ import annotations

import argparse
import sys

FASES_PENDENTES = {
    "ingerir": "sem uso próprio — `ctb calcular` busca e cacheia sob demanda "
               "(pipeline/fontes/http.py), não há passo de ingestão separado que "
               "valha a pena manter",
    "cobertura": "Fase 3 — depende da varredura municipal completa dos dez anos",
    "publicar": "Fase 5 — depende da série calculada (2016-2025) e do site",
    "comparar-historico": "Fase 4 — depende da série calculada",
}


def _intervalo(texto: str) -> range:
    """Aceita `2016-2025` ou `2024`."""
    if "-" in texto:
        inicio, fim = texto.split("-", 1)
        return range(int(inicio), int(fim) + 1)
    ano = int(texto)
    return range(ano, ano + 1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ctb", description=__doc__)
    sub = parser.add_subparsers(dest="comando", required=True)

    fontes = sub.add_parser("fontes", help="diagnóstico das fontes externas")
    fontes_sub = fontes.add_subparsers(dest="acao", required=True)
    testar = fontes_sub.add_parser(
        "testar", help="Fase 0 — testa os endpoints e gera docs/viabilidade-fontes.md"
    )
    testar.add_argument("--anos", type=_intervalo, default=_intervalo("2016-2025"))
    testar.add_argument(
        "--amostra-municipios", type=int, default=300,
        help="municípios sorteados por ano para estimar a cobertura (os acima de "
             "500 mil habitantes são sempre testados por censo)",
    )
    testar.add_argument("--semente", type=int, default=20260830)

    varrer = fontes_sub.add_parser(
        "varrer-municipios",
        help="censo completo dos 5.570 municípios para o cache (~15 min por ano)",
    )
    varrer.add_argument("--anos", type=_intervalo, required=True)
    varrer.add_argument("--conexoes", type=int, default=6,
                        help="a API do Tesouro é pública e lenta — não aumente sem motivo")

    dic = sub.add_parser("dicionario", help="dicionário de contas DCA")
    dic_sub = dic.add_subparsers(dest="acao", required=True)
    val = dic_sub.add_parser(
        "validar", help="Fase 1 — estrutura, cobertura e reconciliação do dicionário"
    )
    val.add_argument("--esfera", choices=["U", "E", "M"], default="U")
    val.add_argument("--anos", type=_intervalo, default=_intervalo("2016-2025"))
    val.add_argument("--tolerancia", type=float, default=0.1,
                     help="diferença máxima aceita por rubrica, em R$ bi")

    calc = sub.add_parser(
        "calcular", help="Fase 2 — agrega, imputa e monta os quadros de um ano"
    )
    calc.add_argument("--anos", type=_intervalo, required=True)

    for nome, fase in FASES_PENDENTES.items():
        sub.add_parser(nome, help=f"[não implementado] {fase}")

    args = parser.parse_args(argv)

    if args.comando in FASES_PENDENTES:
        print(f"`ctb {args.comando}` ainda não existe: {FASES_PENDENTES[args.comando]}.",
              file=sys.stderr)
        return 2

    if args.comando == "fontes" and args.acao == "testar":
        from pipeline.fontes.diagnostico import executar

        executar(args.anos, args.amostra_municipios, args.semente)
        return 0

    if args.comando == "fontes" and args.acao == "varrer-municipios":
        from pipeline.fontes.diagnostico import varrer_municipios

        varrer_municipios(args.anos, args.conexoes)
        return 0

    if args.comando == "dicionario" and args.acao == "validar":
        from pipeline.dominio.validar import validar

        return validar(args.esfera, args.anos, args.tolerancia)

    if args.comando == "calcular":
        from pipeline.dominio.calcular import executar

        for ano in args.anos:
            executar(ano)
        return 0

    parser.error(f"comando não tratado: {args.comando}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
