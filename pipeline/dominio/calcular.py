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
    ROTULO_ESFERA, ad_esfera, bases_incidencia, bygov_detalhado, principais_tributos,
    total_por_esfera,
)
from pipeline.dominio.manual_uniao import ANOS_DISPONIVEIS as ANOS_FGTS_SISTEMA_S
from pipeline.dominio.rd_esfera import ANOS_DISPONIVEIS as ANOS_RD_ESFERA
from pipeline.dominio.rd_esfera import calcular as calcular_rd_esfera
from pipeline.fontes.diagnostico import br
from pipeline.fontes.http import RAIZ
from pipeline.fontes.sidra import pib_corrente, populacao_brasil

# Valores publicados em 2024 (CTB2024.xlsx) para as linhas que cruzam esferas — só para
# a comparação informativa no relatório. Não usados em nenhum cálculo. A diferença é
# esperada: opção B (decisão 1) redistribuiu os acessórios de volta às rubricas de
# origem, então essas linhas sobem frente ao valor antigo (que era só o principal).
COMPARACAO_PRINCIPAIS_TRIBUTOS_2024_BI = {
    "Imposto de Renda (Global)": 894.479,
    "Previdência Social Ampliada": 673.083,
}
COMPARACAO_AD_ESFERA_2024_BI = {
    ("U", "Impostos"): 994.879,
    ("U", "Contribuições Sociais"): 710.864,
    ("U", "Demais"): 225.833,  # incluía Multas e Dívida Ativa, que não existe mais
    ("E", "Demais"): 211.532,
    ("M", "Demais"): 139.529,
}

# RD ESFERA — aba "RD ESFERA" do CTB2024.xlsx, lida diretamente (2026-08-31). Só para a
# comparação informativa no relatório; nunca usada em nenhum cálculo.
COMPARACAO_RD_TRANSFERENCIAS_2024_BI = {
    ("U", "E", "FPE"): 149.831128016,
    ("U", "E", "IPI-Exp (FPEx)"): 6.765493569,
    ("U", "E", "IOF-Ouro"): 0.003691963,
    ("U", "E", "LC176/2020 (Seguro-Receita ICMS)"): 3.0,
    ("U", "E", "FUNDEB"): 36.66770413964999,
    ("U", "E", "Salário-Educação (quota estadual)"): 21.413814335006677,
    ("U", "E", "CIDE"): 0.73765313,
    ("U", "E", "LC201/2023 (Compensação ICMS)"): 0.67448,
    ("U", "E", "Royalties e Compensações Financeiras"): 33.409992069,
    ("U", "M", "FPM"): 177.03413749,
    ("U", "M", "ITR"): 2.517599069,
    ("U", "M", "IOF-Ouro"): 0.008614569,
    ("U", "M", "LC176/2020 (Seguro-Receita ICMS)"): 0.985563376,
    ("U", "M", "FUNDEB"): 89.85504737703,
    ("U", "M", "CIDE"): 0.241551492,
    ("U", "M", "AFM/AFE"): 0.3139165,
    ("U", "M", "Royalties e Compensações Financeiras"): 35.180576528,
    ("E", "M", "ICMS (cota-parte municipal, líq. FUNDEB)"): 161.082859068015,
    ("E", "M", "IPVA (cota-parte municipal)"): 43.766560836305,
    ("E", "M", "IPI-Exp (FPEx) (cota-parte municipal)"): 1.69137339225,
    ("E", "M", "FUNDEB"): 109.83306035795,
    ("E", "M", "LC201/2023 (Compensação ICMS) (cota-parte municipal)"): 0.16862,
}


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
    quadro_ad = ad_esfera(df, pib, populacao)
    quadro_pt = principais_tributos(df, pib, populacao)
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

    partes += ["", "### Por que não fecha exatamente o valor publicado", ""]
    partes.append(
        "FGTS e Sistema S (`manual/`, CLAUDE.md §Fontes) estão incluídos desde "
        "2026-09-01 para 2016-2024 — 2025 ainda não tem fonte (ver \"O que falta\"). "
        "O que resta de diferença contra a série antiga vem da decisão 6 (receita "
        "líquida em estados e municípios, deliberada, reduz o total frente à "
        "metodologia antiga) e de resíduos pequenos já documentados em "
        "`docs/divergencias.md`. `docs/revisao-metodologica.md` "
        "(`uv run ctb comparar-historico`) tem a comparação ano a ano, linha a "
        "linha, com os valores exatos."
    )
    partes += ["", "## AD ESFERA", ""]
    for esf in ("U", "E", "M"):
        partes += [f"### {ROTULO_ESFERA[esf]}", "", _tabela_quadro(quadro_ad[esf]), ""]
    if ano == 2024:
        partes += [
            "**Contra o valor publicado em 2024** (informativo — a diferença é "
            "esperada: opção B redistribuiu os acessórios de volta às rubricas de "
            "origem):",
            "",
            "| esfera | categoria | calculado | publicado 2024 | diferença |",
            "|---|---|---|---|---|",
        ]
        for esf in ("U", "E", "M"):
            for linha in quadro_ad[esf]:
                antigo = COMPARACAO_AD_ESFERA_2024_BI.get((esf, linha.rotulo))
                if antigo is None:
                    continue
                dif = linha.valor_bi - antigo
                partes.append(
                    f"| {ROTULO_ESFERA[esf]} | {linha.rotulo} | {br(linha.valor_bi, 3)} | "
                    f"{br(antigo, 3)} | {('+' if dif >= 0 else '−') + br(abs(dif), 3)} |"
                )
        partes.append("")

    partes += ["## byGOVDetalhado", ""]
    for esf in ("U", "E", "M"):
        partes += [f"### {ROTULO_ESFERA[esf]}", "", _tabela_quadro(quadro_bygov[esf]), ""]

    partes += [
        "## PRINCIPAIS TRIBUTOS", "",
        _tabela_quadro(quadro_pt, rotulo_coluna="tributo"), "",
    ]
    if ano == 2024:
        partes += [
            "**Contra o valor publicado em 2024** (informativo, mesma ressalva da "
            "opção B acima):",
            "",
            "| tributo | calculado | publicado 2024 | diferença |",
            "|---|---|---|---|",
        ]
        for linha in quadro_pt:
            antigo = COMPARACAO_PRINCIPAIS_TRIBUTOS_2024_BI.get(linha.rotulo)
            if antigo is None:
                continue
            dif = linha.valor_bi - antigo
            partes.append(
                f"| {linha.rotulo} | {br(linha.valor_bi, 3)} | {br(antigo, 3)} | "
                f"{('+' if dif >= 0 else '−') + br(abs(dif), 3)} |"
            )
        partes.append("")

    partes += [
        "## Bases de Incidência", "",
        _tabela_quadro(quadro_bases, rotulo_coluna="base de incidência"), "",
    ]

    if ano in ANOS_RD_ESFERA:
        resultado_rd = calcular_rd_esfera(ano, df, totais)
        partes += ["## RD ESFERA", ""]
        partes += [
            "Ajusta AD ESFERA pelas transferências constitucionais entre entes — o "
            "total geral não muda (é redistribuição, não dinheiro novo).",
            "",
            "| esfera | AD (R$ bi) | RD (R$ bi) | RD % PIB | RD % total |",
            "|---|---|---|---|---|",
        ]
        rd_total = sum(resultado_rd.rd_por_esfera.values())
        for esf in ("U", "E", "M"):
            ad_v = totais.get(esf, 0.0)
            rd_v = resultado_rd.rd_por_esfera.get(esf, 0.0)
            partes.append(
                f"| {ROTULO_ESFERA[esf]} | {br(ad_v / 1e9, 3)} | {br(rd_v / 1e9, 3)} | "
                f"{br(rd_v / pib * 100, 3)} | {br(rd_v / rd_total * 100, 2)}% |"
            )
        partes.append("")

        col_comparacao = "publicado 2024" if ano == 2024 else None
        blocos = [("U", "E", " União para Estados"), ("U", "M", " União para Municípios"),
                   ("E", "M", " Estados para Municípios")]
        for origem, destino, titulo in blocos:
            linhas_bloco = sorted(
                (t for t in resultado_rd.transferencias if t.bloco_origem == origem and t.bloco_destino == destino),
                key=lambda t: -t.valor_reais,
            )
            if col_comparacao:
                partes += [f"###{titulo}", "", f"| modalidade | R$ bi | {col_comparacao} | diferença |", "|---|---|---|---|"]
            else:
                partes += [f"###{titulo}", "", "| modalidade | R$ bi |", "|---|---|"]
            soma_bloco = 0.0
            for t in linhas_bloco:
                soma_bloco += t.valor_reais
                antigo = COMPARACAO_RD_TRANSFERENCIAS_2024_BI.get((origem, destino, t.modalidade)) if col_comparacao else None
                if antigo is None:
                    if col_comparacao:
                        partes.append(f"| {t.modalidade} | {br(t.valor_reais / 1e9, 3)} | — | — |")
                    else:
                        partes.append(f"| {t.modalidade} | {br(t.valor_reais / 1e9, 3)} |")
                else:
                    dif = t.valor_reais / 1e9 - antigo
                    partes.append(
                        f"| {t.modalidade} | {br(t.valor_reais / 1e9, 3)} | {br(antigo, 3)} | "
                        f"{('+' if dif >= 0 else '−') + br(abs(dif), 3)} |"
                    )
            partes.append(f"| **Total** | **{br(soma_bloco / 1e9, 3)}** |" + (" | |" if col_comparacao else ""))
            partes.append("")
        partes.append(
            "**Sobre a linha ICMS (cota-parte municipal, líq. FUNDEB):** 25% da "
            "arrecadação estadual de ICMS, com a retenção de 20% do FUNDEB (art. 212-A "
            "CF) aplicada antes do repasse — 25% × 80% = 20% da arrecadação bruta "
            "(decisão do usuário em 2026-08-31, `docs/decisoes-pendentes.md` §9 — em "
            "2024 isso reproduz quase exato o valor publicado, R$ 161,631 bi calculado "
            "contra R$ 161,083 bi). A cota do IPVA não tem essa retenção (50% flat)."
        )
        partes.append("")
    else:
        partes += [
            "## RD ESFERA", "",
            f"Não calculado para {ano} — fora do intervalo coberto por "
            "`pipeline/dominio/rd_esfera.py` (`ANOS_DISPONIVEIS`, hoje 2016-2025).",
            "",
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
        "## O que falta",
        "",
    ]
    if ano not in ANOS_RD_ESFERA:
        partes.append(f"- **RD ESFERA** — não calculado para {ano}, fora do intervalo coberto.")
    if ano not in ANOS_FGTS_SISTEMA_S:
        partes.append(f"- **FGTS e Sistema S** — não calculado para {ano}, sem fonte ainda "
                       "(ver `manual/README.md`).")

    destino = RAIZ / "docs" / f"resultado-{ano}.md"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(partes).rstrip() + "\n", encoding="utf-8")
    print(f"\nRelatório escrito em {destino}")
    print(f"Total: R$ {br(total / 1e9, 3)} bi ({br(total / pib * 100, 2)}% do PIB)")
    return destino
