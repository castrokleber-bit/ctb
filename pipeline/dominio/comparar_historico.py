"""Fase 4 — compara a série calculada contra `CTB-Resumo.xlsx`, ano a ano e linha a
linha, para sustentar a comunicação da revisão metodológica.

CLAUDE.md: **isto não é um teste que precisa passar.** Toda divergência é medida e
explicada, nunca escondida nem forçada a fechar ajustando a metodologia.

`CTB-Resumo.xlsx` só tem 2000-2024 (sem 2025, que a Fase 3 marca como preliminar) — o
intervalo de comparação é 2016-2024, nove anos.
"""

from __future__ import annotations

from pathlib import Path

import polars as pl

from pipeline.dominio.quadros import ROTULO_ESFERA, bygov_detalhado, total_por_esfera
from pipeline.dominio.rd_esfera import calcular as calcular_rd_esfera
from pipeline.fontes.diagnostico import br
from pipeline.fontes.http import RAIZ
from pipeline.fontes.planilha_resumo import ler_aba
from pipeline.fontes.sidra import pib_corrente, populacao_brasil

CTB_RESUMO = RAIZ / "CTB-Resumo.xlsx"
DIR_INTERMEDIARIO = RAIZ / "dados" / "intermediario"

# (rótulo antigo, rubricas novas que somam pro conceito antigo).
# `[]` = a opção B eliminou essa linha (redistribuída nas rubricas de origem, decisão 1).
# `None` = fonte manual ainda não ingerida (FGTS, Sistema S) — gap conhecido, não erro.
MAPA_UNIAO: list[tuple[str, list[str] | None]] = [
    ("IR", ["IR"]),
    ("IPI", ["IPI"]),
    ("IOF", ["IOF"]),
    ("Imp. Sobre Comércio Exterior", ["Imp. sobre Comércio Exterior"]),
    ("ITR", ["ITR"]),
    ("Taxas", ["Taxas"]),
    ("Previdência (1)", ["Previdência Social"]),
    ("Cofins", ["Cofins"]),
    ("CPMF", ["CPMF"]),
    ("CSLL", ["CSLL"]),
    ("PIS-PASEP", ["PIS-PASEP"]),
    ("Contrib. Seg. Serv. Público (2)", ["Contrib. Seg. Serv. Público"]),
    ("Outras contribuições sociais (3)", ["Outras contribuições sociais"]),
    ("Contribuições Econômicas (5)", ["Contribuições Econômicas", "Royalties e Compensações Financeiras"]),
    ("Salário Educação", ["Salário Educação"]),
    ("Multas e Dívida Ativa", []),
    ("FGTS (4)", ["FGTS"]),
    ("Sistema S (4)", ["Sistema S"]),
]

MAPA_ESTADOS: list[tuple[str, list[str] | None]] = [
    ("ICMS", ["ICMS"]),
    ("IPVA", ["IPVA"]),
    ("ITCD", ["ITCD"]),
    ("IRRF", ["IRRF"]),
    ("TAXAS", ["TAXAS"]),
    ("Previ. Estadual", ["Previ. Estadual"]),
    ("Contribuições de Melhoria e Econômicas", ["Contribuições de Melhoria e Econômicas", "Royalties e Compensações Financeiras"]),
    ("Demais (multas, juros e dívida ativa)", []),
]

MAPA_MUNICIPIOS: list[tuple[str, list[str] | None]] = [
    ("ISS", ["ISS"]),
    ("IPTU", ["IPTU"]),
    ("ITBI", ["ITBI"]),
    ("IRRF", ["IRRF"]),
    ("TAXAS", ["TAXAS"]),
    ("Previd. Municipal", ["Previd. Municipal"]),
    ("Contribuições de Melhoria e Econômicas", ["Contribuições de Melhoria e Econômicas", "Royalties e Compensações Financeiras"]),
    ("Demais (multas, juros e dívida ativa)", []),
]

MAPAS = {"U": MAPA_UNIAO, "E": MAPA_ESTADOS, "M": MAPA_MUNICIPIOS}

ANO_MIN, ANO_MAX = 2016, 2024  # CTB-Resumo.xlsx não tem 2025


class ErroComparacao(RuntimeError):
    pass


def _tabela_headline(titulo: str, anos: list[int], dados_ant: dict, dados_novo: dict, pib_por_ano: dict) -> list[str]:
    partes = [f"### {titulo}", "", "| ano | antigo (R$ bi) | antigo (% PIB) | novo (R$ bi) | novo (% PIB) | Δ R$ bi | Δ p.p. PIB |",
              "|---|---|---|---|---|---|---|"]
    for ano in anos:
        ant = dados_ant.get(ano, 0.0)
        novo = dados_novo.get(ano, 0.0)
        pib_ant = pib_por_ano[ano]["pib_antigo"]
        pib_novo = pib_por_ano[ano]["pib_novo"]
        dif = novo - ant
        difpp = (novo / pib_novo * 100) - (ant / pib_ant * 100)
        partes.append(
            f"| {ano} | {br(ant, 3)} | {br(ant / pib_ant * 100, 3)} | {br(novo, 3)} | "
            f"{br(novo / pib_novo * 100, 3)} | {('+' if dif >= 0 else '−') + br(abs(dif), 3)} | "
            f"{('+' if difpp >= 0 else '−') + br(abs(difpp), 3)} |"
        )
    partes.append("")
    return partes


def _matriz_rubricas(esfera: str, anos: list[int], por_ano: dict) -> list[str]:
    """Uma tabela por esfera: linhas = rubrica (rótulo antigo), colunas = anos, célula
    = Δ p.p. do PIB (novo − antigo). `>>` marca célula acima de 0,3 p.p., o limiar de
    divergência do CLAUDE.md.
    """
    mapa = MAPAS[esfera]
    cab = f"| rubrica (rótulo antigo) | " + " | ".join(str(a) for a in anos) + " |"
    sep = "|---|" + "---|" * len(anos)
    partes = [cab, sep]
    for rotulo_antigo, novas in mapa:
        celulas = []
        for ano in anos:
            d = por_ano[ano]
            pib_novo = d["pib_novo"]
            if novas is None:
                celulas.append("gap manual")
                continue
            ant = d["antigo"][esfera].get(rotulo_antigo, 0.0)
            novo = sum(d["novo"][esfera].get(r, 0.0) for r in novas)
            difpp = (novo - ant) / pib_novo * 100
            marca = " ⚠️" if abs(difpp) > 0.3 else ""
            sinal = "+" if difpp >= 0 else "−"
            celulas.append(f"{sinal}{br(abs(difpp), 3)}{marca}")
        partes.append(f"| {rotulo_antigo} | " + " | ".join(celulas) + " |")
    partes.append("")
    return partes


def _linhas_novas_sem_correspondente(esfera: str, anos: list[int], por_ano: dict) -> list[str]:
    mapeadas = {r for _, novas in MAPAS[esfera] if novas for r in novas}
    todas_novas: set[str] = set()
    for ano in anos:
        todas_novas |= set(por_ano[ano]["novo"][esfera].keys())
    extras = sorted(todas_novas - mapeadas)
    if not extras:
        return []
    partes = ["**Rubricas novas sem linha antiga correspondente** (R$ bi):", "",
              "| rubrica | " + " | ".join(str(a) for a in anos) + " |", "|---|" + "---|" * len(anos)]
    for r in extras:
        vals = [br(por_ano[ano]["novo"][esfera].get(r, 0.0), 3) for ano in anos]
        partes.append(f"| {r} | " + " | ".join(vals) + " |")
    partes.append("")
    return partes


def executar() -> Path:
    print("Fase 4 — comparando contra CTB-Resumo.xlsx")
    dados_bygov_antigo = ler_aba(CTB_RESUMO, "byGOVDetalhado")
    dados_rd_antigo = ler_aba(CTB_RESUMO, "RD ESFERA")

    anos_disponiveis = sorted(a for a in dados_bygov_antigo if ANO_MIN <= a <= ANO_MAX)
    faltando_parquet = [a for a in anos_disponiveis if not (DIR_INTERMEDIARIO / f"{a}.parquet").exists()]
    if faltando_parquet:
        raise ErroComparacao(
            f"anos sem dados/intermediario/{{ano}}.parquet: {faltando_parquet} — "
            f"rode `uv run ctb calcular --anos {ANO_MIN}-{ANO_MAX}` primeiro."
        )

    total_geral_antigo: dict[int, float] = {}
    total_geral_novo: dict[int, float] = {}
    ad_por_esfera_antigo: dict[str, dict[int, float]] = {"U": {}, "E": {}, "M": {}}
    ad_por_esfera_novo: dict[str, dict[int, float]] = {"U": {}, "E": {}, "M": {}}
    rd_por_esfera_antigo: dict[str, dict[int, float]] = {"U": {}, "E": {}, "M": {}}
    rd_por_esfera_novo: dict[str, dict[int, float]] = {"U": {}, "E": {}, "M": {}}
    pib_por_ano: dict[int, dict[str, float]] = {}
    por_ano: dict[int, dict] = {}

    for ano in anos_disponiveis:
        print(f"  {ano}...")
        df = pl.read_parquet(DIR_INTERMEDIARIO / f"{ano}.parquet")
        pib_novo, _ = pib_corrente(ano)
        pib_novo_bi = pib_novo / 1e9
        populacao_novo = populacao_brasil(ano)

        quadro_bygov = bygov_detalhado(df, pib_novo, populacao_novo)
        novo_bygov = {esf: {l.rotulo: l.valor_bi for l in linhas} for esf, linhas in quadro_bygov.items()}
        ad_totais = total_por_esfera(df)

        resultado_rd = calcular_rd_esfera(ano, df, ad_totais)

        total_geral_antigo[ano] = dados_bygov_antigo[ano]["total"]
        total_geral_novo[ano] = sum(ad_totais.values()) / 1e9
        pib_por_ano[ano] = {"pib_antigo": dados_bygov_antigo[ano]["pib"], "pib_novo": pib_novo_bi}

        for esf in ("U", "E", "M"):
            ad_por_esfera_antigo[esf][ano] = dados_bygov_antigo[ano]["blocos"][esf].get("_total") or sum(
                v for k, v in dados_bygov_antigo[ano]["blocos"][esf].items() if k != "_total"
            )
            ad_por_esfera_novo[esf][ano] = ad_totais.get(esf, 0.0) / 1e9
            rd_por_esfera_antigo[esf][ano] = dados_rd_antigo[ano]["blocos"][esf].get("_total", 0.0)
            rd_por_esfera_novo[esf][ano] = resultado_rd.rd_por_esfera.get(esf, 0.0) / 1e9

        por_ano[ano] = {
            "antigo": {esf: dados_bygov_antigo[ano]["blocos"][esf] for esf in ("U", "E", "M")},
            "novo": novo_bygov,
            "pib_novo": pib_novo_bi,
        }

    partes = [
        "# Revisão metodológica — comparação contra a série histórica",
        "",
        f"Gerado por `uv run ctb comparar-historico`. Compara `dados/intermediario/{{ano}}.parquet` "
        f"({ANO_MIN}-{ANO_MAX}, os anos em comum com `CTB-Resumo.xlsx`, que não tem 2025) contra a "
        "série publicada. **Isto não é um teste que precisa passar** (CLAUDE.md) — é o material que "
        "sustenta a comunicação da revisão. Nenhuma divergência aqui foi corrigida ajustando a "
        "metodologia para o diff diminuir.",
        "",
        "## Por que a série diverge — mecanismos, não erros",
        "",
        "Quatro mudanças deliberadas explicam a maior parte da diferença que resta, todas já "
        "decididas e documentadas em `docs/decisoes-pendentes.md` — FGTS e Sistema S (o antigo "
        "maior gap do total geral) passaram a ser incluídos a partir de 2016 (fonte em "
        "`manual/README.md`), o que já fechou a maior parte da diferença sozinho:",
        "",
        "1. **Opção B (decisão 1):** cada rubrica passa a ser receita líquida da DCA "
        "(bruta + Outras Deduções), não mais só o \"principal\". *Multas e Dívida Ativa* deixa de "
        "existir como linha própria — o valor volta para as rubricas de origem. Isso não muda o "
        "total da União, só a composição.",
        "2. **Royalties (decisão 4):** ganham linha própria (*Royalties e Compensações "
        "Financeiras*) nas três esferas, separada de *Contribuições Econômicas*/*Contribuições de "
        "Melhoria e Econômicas*. Na tabela abaixo, somamos as duas rubricas novas para comparar com "
        "a linha antiga combinada.",
        "3. **Receita líquida em estados e municípios (decisão 6):** uniformiza com a União — reduz "
        "o total de Estados e Municípios frente à bruta que a série antiga publicava.",
        "4. **IRPF/IRPJ reclassificado para IRRF (decisão 7):** em estados e municípios, afasta um "
        "pouco o IRRF calculado do publicado (o publicado tratava esses lançamentos como \"Outros "
        "impostos\").",
        "",
        "## Total geral",
        "",
    ]
    partes += _tabela_headline("Brasil", anos_disponiveis, total_geral_antigo, total_geral_novo, pib_por_ano)

    partes += ["## Arrecadação Direta (AD ESFERA) — por esfera", ""]
    for esf in ("U", "E", "M"):
        partes += _tabela_headline(ROTULO_ESFERA[esf], anos_disponiveis, ad_por_esfera_antigo[esf], ad_por_esfera_novo[esf], pib_por_ano)

    partes += ["## Receita Disponível (RD ESFERA) — por esfera", ""]
    for esf in ("U", "E", "M"):
        partes += _tabela_headline(ROTULO_ESFERA[esf], anos_disponiveis, rd_por_esfera_antigo[esf], rd_por_esfera_novo[esf], pib_por_ano)

    partes += [
        "## Achados que pedem atenção", "",
        "Três divergências na tabela abaixo saem muito do padrão normal de ruído da opção B "
        "(que fica tipicamente abaixo de 0,3 p.p.) e foram investigadas até a causa raiz ou até o "
        "limite razoável desta passada:", "",
        "1. **União, 2019 — Previdência Social despenca, Outras contribuições sociais dispara "
        "(−1,664 p.p. e +1,771 p.p.).** Causa identificada: a conta `RO1.2.1.9.99.2.0 - Demais "
        "Contribuições Sociais - Parcelamento` sozinha soma R$ 132,875 bi em 2019 — um "
        "parcelamento (provavelmente REFIS/renegociação de dívida previdenciária) que a própria "
        "DCA classificou dentro do ramo genérico \"Outras Contribuições Sociais\" "
        "(`1.2.1.9`) em vez do ramo específico do RGPS (`1.2.1.4`). O dicionário segue "
        "corretamente o código que a DCA usa — o gap é a granularidade que a opção B perdeu (o "
        "8º dígito que separaria \"parcelamento de dívida do RGPS\" de \"outras contribuições "
        "genuínas\"), não um erro de mapeamento. R$ 132,875 bi explica quase toda a diferença "
        "combinada das duas linhas nesse ano.",
        "2. **Estados e Municípios, 2018 em diante — a linha \"Demais (multas, juros e dívida "
        "ativa)\" da série antiga é exatamente R$ 0,00 todo ano.** Não é um artefato desta "
        "leitura: `CTB-Resumo.xlsx` já publicava zero para essa linha em Estados e Municípios a "
        "partir de 2018 (em 2016-2017 tinha valor: R$ 13,7 bi e R$ 13,0 bi em 2016). A série "
        "antiga bateu no mesmo limite que motivou a decisão 1 (o 8º dígito da natureza de "
        "receita, que separa principal de acessório, deixa de estar disponível) e simplesmente "
        "zerou a linha em vez de estimá-la — subestimando o total de Estados e Municípios nesses "
        "anos. A opção B, que redistribui esse valor de volta às rubricas de origem em vez de "
        "descartá-lo, é mais completa para 2018 em diante, ao custo de comparabilidade direta "
        "contra 2016-2017.",
        "3. **União, IR, 2020-2023 — diferença 5 a 9× maior que o efeito normal da opção B "
        "(até +1,541 p.p. em 2020, contra +0,175 p.p. em 2024).** Causa localizada, não "
        "totalmente explicada: a conta `RO1.1.1.3.02.0.0` (IRPJ líquido) tem, na coluna "
        "\"Outras Deduções da Receita\", valor **positivo** em 2020-2023 (+46,9 / +33,6 / +28,6 "
        "/ +38,2 bi) — nos outros oito anos da série (2016-2019 e 2024) essa mesma coluna é "
        "sempre **negativa** (ex.: −39,5 bi em 2024), como se espera de uma coluna de "
        "restituições. É essa inversão de sinal, isolada nessas quatro contas do IRPJ, que "
        "explica o salto: sob a opção B (líquida = bruta + Outras Deduções), um valor positivo "
        "nessa coluna soma à receita em vez de subtrair. O porquê da STN reportar essa conta "
        "assim especificamente em 2020-2023 não foi determinado — hipótese mais provável é a "
        "dinâmica de estimativa mensal vs. ajuste anual do IRPJ (o imposto é pago por "
        "estimativa ao longo do ano e ajustado depois) amplificada pela recessão de 2020 e por "
        "programas de renegociação de dívida tributária do período, mas isso não foi verificado "
        "linha a linha. Fica registrado para investigação futura, não decidido nem corrigido "
        "nesta passada.",
        "",
        "Fora esses três, as células acima de 0,3 p.p. na matriz abaixo seguem os mecanismos já "
        "listados (opção B, royalties, receita líquida, reclassificação de IRPF/IRPJ) sem achado "
        "adicional que justifique investigação linha a linha.",
        "",
        "## byGOVDetalhado — linha a linha, por esfera", "",
        "Célula = diferença em pontos percentuais do PIB (novo − antigo, calculado com o PIB "
        "corrente de cada ano). `⚠️` marca acima de 0,3 p.p., o limiar de divergência do CLAUDE.md "
        "que exigiria decisão do usuário se fosse uma escolha metodológica nova — aqui é resíduo "
        "medido, não decisão pendente.", "",
    ]
    for esf in ("U", "E", "M"):
        partes += [f"### {ROTULO_ESFERA[esf]}", ""]
        partes += _matriz_rubricas(esf, anos_disponiveis, por_ano)
        partes += _linhas_novas_sem_correspondente(esf, anos_disponiveis, por_ano)

    destino = RAIZ / "docs" / "revisao-metodologica.md"
    destino.write_text("\n".join(partes).rstrip() + "\n", encoding="utf-8")
    print(f"\nRelatório escrito em {destino}")
    return destino
