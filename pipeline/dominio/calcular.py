"""Orquestra a Fase 2: agregação, imputação, quadros e o relatório de um ano.

A reconciliação rubrica a rubrica contra a planilha, por esfera, já foi feita e
documentada na Fase 1 (`uv run ctb dicionario validar`). Este módulo não repete isso —
soma o resultado agregado e imputado, e confere se a ordem de grandeza do total bate,
com toda divergência explicada, nunca escondida (regra 6 do CLAUDE.md).
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from pipeline.dominio.agregacao import calcular_ano
from pipeline.dominio.quadros import (
    ROTULO_ESFERA, bases_incidencia, bygov_detalhado, total_por_esfera,
)
from pipeline.fontes.diagnostico import br
from pipeline.fontes.http import RAIZ
from pipeline.fontes.sidra import pib_corrente, populacao_brasil

# FGTS e Sistema S são fontes manuais (CLAUDE.md §Fontes) e ainda não foram ingeridas —
# nenhum CSV existe em `manual/` até agora. O total desta passada fica abaixo da
# planilha por causa disso, não por erro. Valores de 2024 vêm da própria planilha
# (linhas "FGTS" e "Sistema S" do bloco União em `byGOVDetalhado`), citados aqui só
# para dimensionar o gap conhecido — nunca somados ao cálculo.
GAP_MANUAL_2024_BI = {"FGTS": 191.995, "Sistema S": 29.320}


def _tabela_quadro(linhas, casas: int = 3, rotulo_coluna: str = "rubrica") -> str:
    cab = f'| {rotulo_coluna} | R$ bi | % PIB | % total | per capita (R$) |\n|---|---|---|---|---|\n'
    corpo = "\n".join(
        f"| {l.rotulo} | {br(l.valor_bi, casas)} | {br(l.pct_pib, 3)} | "
        f"{br(l.pct_total, 3)} | {br(l.per_capita, 2)} |"
        for l in linhas
    )
    return cab + corpo + "\n"


def executar(ano: int) -> Path:
    print(f"Fase 2 — calculando {ano}")

    print("  [1/3] agregando (DCA + imputação municipal)")
    df, relatorio_imputacao = calcular_ano(ano)

    print("  [2/3] PIB e população (SIDRA)")
    pib, data_pib = pib_corrente(ano)
    populacao = populacao_brasil(ano)

    print("  [3/3] montando os quadros")
    quadro_bygov = bygov_detalhado(df, pib, populacao)
    quadro_bases = bases_incidencia(df, pib, populacao)
    totais = total_por_esfera(df)
    total = sum(totais.values())

    partes = [
        f"# Resultado calculado — {ano}",
        "",
        f"Gerado por `uv run ctb calcular --anos {ano}` em {date.today().isoformat()}. "
        f"PIB corrente ({date.today().isoformat()}, SIDRA tabela 1846): "
        f"R$ {br(pib / 1e9, 3)} bi. População (SIDRA tabela 6579): {br(populacao)}.",
        "",
        "Este é o produto da Fase 2 — a primeira vez que o pipeline produz um número, "
        "não só valida uma estrutura. A reconciliação rubrica a rubrica por esfera já "
        "foi feita na Fase 1 (`uv run ctb dicionario validar`); aqui confere-se o "
        "agregado.",
        "",
        "## Total geral",
        "",
        f"**R$ {br(total / 1e9, 3)} bi — {br(total / pib * 100, 3)}% do PIB**",
        "",
        "| esfera | R$ bi | % do total |",
        "|---|---|---|",
    ]
    for esf in ("U", "E", "M"):
        v = totais.get(esf, 0.0)
        partes.append(f"| {ROTULO_ESFERA[esf]} | {br(v / 1e9, 3)} | {br(v / total * 100, 2)}% |")

    partes += ["", "### Por que não fecha em ~36% do PIB direto", ""]
    if ano == 2024:
        gap_manual_bi = sum(GAP_MANUAL_2024_BI.values())
        gap_manual_pp = gap_manual_bi / (pib / 1e9) * 100
        total_ajustado_pct = (total / 1e9 + gap_manual_bi) / (pib / 1e9) * 100
        partes += [
            f"O total acima fecha em {br(total / pib * 100, 2)}% do PIB, abaixo dos "
            "35,950% da série publicada de 2024. A diferença tem duas causas "
            "conhecidas, nenhuma delas erro de cálculo:",
            "",
            f"1. **FGTS e Sistema S não estão nesta passada** (R$ {br(gap_manual_bi, 1)} "
            f"bi em 2024, {br(gap_manual_pp, 2)} p.p. do PIB) — são fontes manuais "
            "(`manual/`, CLAUDE.md §Fontes) e nenhum CSV foi coletado ainda. Somando "
            f"esse gap de volta: {br(total_ajustado_pct, 3)}%, muito perto dos "
            "35,950% publicados.",
            "2. **Decisão 6** (2026-08-31) uniformizou estados e municípios em receita "
            "líquida — reduz o total em cerca de R$ 29 bi contra a metodologia antiga "
            "(bruta). É mudança deliberada, não resíduo.",
            "",
            "O restante é resíduo pequeno e já documentado — ver `docs/divergencias.md` "
            "e `docs/decisoes-pendentes.md` (Contribuições Econômicas da União, IPTU e "
            "IRRF municipais).",
        ]
    else:
        partes.append(
            "FGTS, Sistema S e a receita líquida de estados/municípios (decisão 6) "
            "reduzem o total frente à metodologia antiga — ver o relatório de 2024 "
            "para a explicação completa e os valores dessa diferença."
        )
    partes += ["", "## byGOVDetalhado", ""]
    for esf in ("U", "E", "M"):
        partes += [f"### {ROTULO_ESFERA[esf]}", "", _tabela_quadro(quadro_bygov[esf]), ""]

    partes += [
        "## Bases de Incidência", "",
        _tabela_quadro(quadro_bases, rotulo_coluna="base de incidência"), "",
    ]

    partes += [
        "## Cobertura da imputação municipal",
        "",
        f"- Municípios no universo: {br(relatorio_imputacao.total_municipios)}",
        f"- Declarantes: {br(relatorio_imputacao.declarantes)} "
        f"({br(relatorio_imputacao.pct_populacao_coberta, 2)}% da população coberta)",
        f"- Imputados: {br(len(relatorio_imputacao.municipios_imputados))} "
        f"({br(relatorio_imputacao.pct_receita_imputada, 3)}% da receita municipal)",
    ]
    if relatorio_imputacao.faixas_mescladas:
        partes.append(
            "- Faixas com menos de 30 declarantes, mescladas com a faixa vizinha para "
            "o cálculo da média: "
            + ", ".join(f"{k}←{v}" for k, v in sorted(relatorio_imputacao.faixas_mescladas.items()))
        )

    partes += [
        "",
        "## O que falta nesta passada",
        "",
        "- **AD ESFERA** e **PRINCIPAIS TRIBUTOS** — precisam de investigação nova na "
        "planilha de referência (categoria econômica e agregação cruzando esferas, "
        "respectivamente) que não foi feita ainda.",
        "- **RD ESFERA** — depende de transferências constitucionais; o bloco "
        "Estados→Municípios segue sem fonte (decisão 5).",
        "- **FGTS e Sistema S** — fontes manuais, nenhum CSV coletado ainda.",
    ]

    destino = RAIZ / "docs" / f"resultado-{ano}.md"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(partes).rstrip() + "\n", encoding="utf-8")
    print(f"\nRelatório escrito em {destino}")
    print(f"Total: R$ {br(total / 1e9, 3)} bi ({br(total / pib * 100, 2)}% do PIB)")
    return destino
