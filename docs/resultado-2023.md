# Resultado calculado — 2023

Gerado por `uv run ctb calcular --anos 2023` em 2026-09-01. PIB corrente (2026-09-01, SIDRA tabela 1846): R$ 10.943,344 bi. População (SIDRA tabela 6579): 203.080.756.

Este é o produto da Fase 2 — a primeira vez que o pipeline produz um número, não só valida uma estrutura. A reconciliação rubrica a rubrica por esfera já foi feita na Fase 1 (`uv run ctb dicionario validar`); aqui confere-se o agregado.

## Total geral

**R$ 3.842,822 bi — 35,116% do PIB**

| esfera | R$ bi | % do total |
|---|---|---|
| União | 2.548,760 | 66,33% |
| Estados | 975,558 | 25,39% |
| Municípios | 318,503 | 8,29% |

### Por que não fecha exatamente o valor publicado

FGTS e Sistema S (`manual/`, CLAUDE.md §Fontes) estão incluídos desde 2026-09-01 para 2016-2024 — 2025 ainda não tem fonte (ver "O que falta"). O que resta de diferença contra a série antiga vem da decisão 6 (receita líquida em estados e municípios, deliberada, reduz o total frente à metodologia antiga) e de resíduos pequenos já documentados em `docs/divergencias.md`. `docs/revisao-metodologica.md` (`uv run ctb comparar-historico`) tem a comparação ano a ano, linha a linha, com os valores exatos.

## AD ESFERA

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Impostos | 982,831 | 8,981 | 25,576 | 4.839,61 |
| Contribuições Sociais | 904,008 | 8,261 | 23,525 | 4.451,47 |
| Previdência Social | 525,622 | 4,803 | 13,678 | 2.588,24 |
| Demais | 136,300 | 1,246 | 3,547 | 671,16 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 702,788 | 6,422 | 18,288 | 3.460,64 |
| IPVA | 82,112 | 0,750 | 2,137 | 404,33 |
| Demais | 190,658 | 1,742 | 4,961 | 938,83 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 123,175 | 1,126 | 3,205 | 606,53 |
| IPTU | 71,258 | 0,651 | 1,854 | 350,88 |
| Demais | 124,071 | 1,134 | 3,229 | 610,94 |


## byGOVDetalhado

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| IR | 796,493 | 7,278 | 20,727 | 3.922,05 |
| Previdência Social | 525,622 | 4,803 | 13,678 | 2.588,24 |
| Cofins | 377,680 | 3,451 | 9,828 | 1.859,76 |
| FGTS | 176,101 | 1,609 | 4,583 | 867,15 |
| CSLL | 164,636 | 1,504 | 4,284 | 810,69 |
| Royalties e Compensações Financeiras | 108,533 | 0,992 | 2,824 | 534,43 |
| PIS-PASEP | 100,785 | 0,921 | 2,623 | 496,28 |
| IPI | 63,833 | 0,583 | 1,661 | 314,32 |
| IOF | 60,488 | 0,553 | 1,574 | 297,85 |
| Imp. sobre Comércio Exterior | 58,756 | 0,537 | 1,529 | 289,33 |
| Contrib. Seg. Serv. Público | 27,001 | 0,247 | 0,703 | 132,95 |
| Sistema S | 26,919 | 0,246 | 0,700 | 132,55 |
| Salário Educação | 23,939 | 0,219 | 0,623 | 117,88 |
| Contribuições Econômicas | 18,650 | 0,170 | 0,485 | 91,84 |
| Taxas | 9,117 | 0,083 | 0,237 | 44,89 |
| Outras contribuições sociais | 6,942 | 0,063 | 0,181 | 34,18 |
| ITR | 3,260 | 0,030 | 0,085 | 16,05 |
| CPMF | 0,004 | 0,000 | 0,000 | 0,02 |
| Outros impostos | 0,001 | 0,000 | 0,000 | 0,01 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 702,788 | 6,422 | 18,288 | 3.460,64 |
| IPVA | 82,112 | 0,750 | 2,137 | 404,33 |
| IRRF | 73,273 | 0,670 | 1,907 | 360,81 |
| Previ. Estadual | 51,915 | 0,474 | 1,351 | 255,64 |
| TAXAS | 42,834 | 0,391 | 1,115 | 210,92 |
| ITCD | 15,532 | 0,142 | 0,404 | 76,48 |
| Contribuições de Melhoria e Econômicas | 6,615 | 0,060 | 0,172 | 32,57 |
| Royalties e Compensações Financeiras | 0,442 | 0,004 | 0,011 | 2,18 |
| Outros impostos | 0,047 | 0,000 | 0,001 | 0,23 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 123,175 | 1,126 | 3,205 | 606,53 |
| IPTU | 71,258 | 0,651 | 1,854 | 350,88 |
| IRRF | 41,023 | 0,375 | 1,068 | 202,00 |
| Previd. Municipal | 27,010 | 0,247 | 0,703 | 133,00 |
| ITBI | 21,541 | 0,197 | 0,561 | 106,07 |
| TAXAS | 17,760 | 0,162 | 0,462 | 87,45 |
| Contribuições de Melhoria e Econômicas | 15,057 | 0,138 | 0,392 | 74,14 |
| Royalties e Compensações Financeiras | 0,993 | 0,009 | 0,026 | 4,89 |
| Outros impostos | 0,686 | 0,006 | 0,018 | 3,38 |


## PRINCIPAIS TRIBUTOS

| tributo | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Imposto de Renda (Global) | 910,789 | 8,323 | 23,701 | 4.484,86 |
| ICMS | 702,788 | 6,422 | 18,288 | 3.460,64 |
| Previdência Social Ampliada | 604,547 | 5,524 | 15,732 | 2.976,88 |
| Cofins | 377,680 | 3,451 | 9,828 | 1.859,76 |
| CSLL | 164,636 | 1,504 | 4,284 | 810,69 |
| ISS | 123,175 | 1,126 | 3,205 | 606,53 |
| PIS-PASEP | 100,785 | 0,921 | 2,623 | 496,28 |
| IPVA | 82,112 | 0,750 | 2,137 | 404,33 |
| IPTU | 71,258 | 0,651 | 1,854 | 350,88 |
| IPI | 63,833 | 0,583 | 1,661 | 314,32 |
| IOF | 60,488 | 0,553 | 1,574 | 297,85 |
| Comércio Exterior (Importação + Exportação) | 58,756 | 0,537 | 1,529 | 289,33 |
| ITBI | 21,541 | 0,197 | 0,561 | 106,07 |
| ITCD | 15,532 | 0,142 | 0,404 | 76,48 |
| ITR | 3,260 | 0,030 | 0,085 | 16,05 |
| CPMF | 0,004 | 0,000 | 0,000 | 0,02 |
| Demais tributos | 481,638 | 4,401 | 12,533 | 2.371,66 |


## Bases de Incidência

| base de incidência | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| bens_servicos | 1.401,599 | 12,808 | 36,473 | 6.901,68 |
| renda | 1.075,425 | 9,827 | 27,985 | 5.295,55 |
| salarios | 861,257 | 7,870 | 22,412 | 4.240,96 |
| patrimonio | 303,987 | 2,778 | 7,911 | 1.496,88 |
| taxas | 69,711 | 0,637 | 1,814 | 343,27 |
| transacoes_financeiras | 60,492 | 0,553 | 1,574 | 297,87 |
| comercio_exterior | 58,756 | 0,537 | 1,529 | 289,33 |
| demais | 11,595 | 0,106 | 0,302 | 57,10 |


## RD ESFERA

Ajusta AD ESFERA pelas transferências constitucionais entre entes — o total geral não muda (é redistribuição, não dinheiro novo).

| esfera | AD (R$ bi) | RD (R$ bi) | RD % PIB | RD % total |
|---|---|---|---|---|
| União | 2.548,760 | 2.055,305 | 18,781 | 53,48% |
| Estados | 975,558 | 924,869 | 8,451 | 24,07% |
| Municípios | 318,503 | 862,647 | 7,883 | 22,45% |

### União para Estados

| modalidade | R$ bi |
|---|---|
| FPE | 129,258 |
| Royalties e Compensações Financeiras | 32,866 |
| FUNDEB | 31,997 |
| Salário-Educação (quota estadual) | 15,960 |
| LC201/2023 (Compensação ICMS) | 9,526 |
| IPI-Exp (FPEx) | 4,683 |
| LC176/2020 (Seguro-Receita ICMS) | 3,000 |
| AFM/AFE | 2,004 |
| CIDE | 0,105 |
| IOF-Ouro | 0,013 |
| FEX | 0,000 |
| LC87/1996 (Lei Kandir) | 0,000 |
| **Total** | **229,411** |

### União para Municípios

| modalidade | R$ bi |
|---|---|
| FPM | 152,044 |
| FUNDEB | 71,782 |
| Royalties e Compensações Financeiras | 32,714 |
| AFM/AFE | 4,171 |
| ITR | 2,281 |
| LC176/2020 (Seguro-Receita ICMS) | 0,987 |
| CIDE | 0,034 |
| IOF-Ouro | 0,031 |
| FEX | 0,000 |
| LC87/1996 (Lei Kandir) | 0,000 |
| **Total** | **264,044** |

### Estados para Municípios

| modalidade | R$ bi |
|---|---|
| ICMS (cota-parte municipal, líq. FUNDEB) | 140,558 |
| FUNDEB | 94,934 |
| IPVA (cota-parte municipal) | 41,056 |
| LC201/2023 (Compensação ICMS) (cota-parte municipal) | 2,382 |
| IPI-Exp (FPEx) (cota-parte municipal) | 1,171 |
| **Total** | **280,100** |

**Sobre a linha ICMS (cota-parte municipal, líq. FUNDEB):** 25% da arrecadação estadual de ICMS, com a retenção de 20% do FUNDEB (art. 212-A CF) aplicada antes do repasse — 25% × 80% = 20% da arrecadação bruta (decisão do usuário em 2026-08-31, `docs/decisoes-pendentes.md` §9 — em 2024 isso reproduz quase exato o valor publicado, R$ 161,631 bi calculado contra R$ 161,083 bi). A cota do IPVA não tem essa retenção (50% flat).

## Cobertura da imputação municipal

- Municípios no universo: 5.569
- Declarantes: 5.556 (99,92% da população coberta)
- Imputados: 13 (0,038% da receita municipal)
- Faixas com menos de 30 declarantes, mescladas com a faixa vizinha para o cálculo da média: 16←[15], 17←[18]

## O que falta
