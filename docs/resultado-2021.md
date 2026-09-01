# Resultado calculado — 2021

Gerado por `uv run ctb calcular --anos 2021` em 2026-09-01. PIB corrente (2026-09-01, SIDRA tabela 1846): R$ 9.012,142 bi. População (SIDRA tabela 6579): 213.317.639.

Este é o produto da Fase 2 — a primeira vez que o pipeline produz um número, não só valida uma estrutura. A reconciliação rubrica a rubrica por esfera já foi feita na Fase 1 (`uv run ctb dicionario validar`); aqui confere-se o agregado.

## Total geral

**R$ 3.180,329 bi — 35,289% do PIB**

| esfera | R$ bi | % do total |
|---|---|---|
| União | 2.067,137 | 65,00% |
| Estados | 868,349 | 27,30% |
| Municípios | 244,843 | 7,70% |

### Por que não fecha exatamente o valor publicado

FGTS e Sistema S (`manual/`, CLAUDE.md §Fontes) estão incluídos desde 2026-09-01 para 2016-2024 — 2025 ainda não tem fonte (ver "O que falta"). O que resta de diferença contra a série antiga vem da decisão 6 (receita líquida em estados e municípios, deliberada, reduz o total frente à metodologia antiga) e de resíduos pequenos já documentados em `docs/divergencias.md`. `docs/revisao-metodologica.md` (`uv run ctb comparar-historico`) tem a comparação ano a ano, linha a linha, com os valores exatos.

## AD ESFERA

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Impostos | 794,163 | 8,812 | 24,971 | 3.722,91 |
| Contribuições Sociais | 725,482 | 8,050 | 22,812 | 3.400,95 |
| Previdência Social | 419,729 | 4,657 | 13,198 | 1.967,62 |
| Demais | 127,763 | 1,418 | 4,017 | 598,93 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 657,889 | 7,300 | 20,686 | 3.084,08 |
| IPVA | 53,402 | 0,593 | 1,679 | 250,34 |
| Demais | 157,059 | 1,743 | 4,938 | 736,27 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 90,059 | 0,999 | 2,832 | 422,18 |
| IPTU | 58,564 | 0,650 | 1,841 | 274,54 |
| Demais | 96,220 | 1,068 | 3,025 | 451,06 |


## byGOVDetalhado

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| IR | 603,406 | 6,695 | 18,973 | 2.828,68 |
| Previdência Social | 419,729 | 4,657 | 13,198 | 1.967,62 |
| Cofins | 297,350 | 3,299 | 9,350 | 1.393,93 |
| FGTS | 137,161 | 1,522 | 4,313 | 642,99 |
| CSLL | 134,879 | 1,497 | 4,241 | 632,29 |
| Royalties e Compensações Financeiras | 93,714 | 1,040 | 2,947 | 439,32 |
| PIS-PASEP | 83,205 | 0,923 | 2,616 | 390,05 |
| IPI | 78,297 | 0,869 | 2,462 | 367,04 |
| Imp. sobre Comércio Exterior | 62,031 | 0,688 | 1,950 | 290,79 |
| IOF | 48,141 | 0,534 | 1,514 | 225,68 |
| Contrib. Seg. Serv. Público | 26,849 | 0,298 | 0,844 | 125,86 |
| Contribuições Econômicas | 26,762 | 0,297 | 0,841 | 125,46 |
| Salário Educação | 20,825 | 0,231 | 0,655 | 97,63 |
| Sistema S | 20,107 | 0,223 | 0,632 | 94,26 |
| Taxas | 7,287 | 0,081 | 0,229 | 34,16 |
| Outras contribuições sociais | 5,078 | 0,056 | 0,160 | 23,80 |
| ITR | 2,284 | 0,025 | 0,072 | 10,71 |
| CPMF | 0,028 | 0,000 | 0,001 | 0,13 |
| Outros impostos | 0,004 | 0,000 | 0,000 | 0,02 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 657,889 | 7,300 | 20,686 | 3.084,08 |
| IPVA | 53,402 | 0,593 | 1,679 | 250,34 |
| IRRF | 51,076 | 0,567 | 1,606 | 239,44 |
| Previ. Estadual | 45,540 | 0,505 | 1,432 | 213,48 |
| TAXAS | 31,931 | 0,354 | 1,004 | 149,69 |
| ITCD | 12,811 | 0,142 | 0,403 | 60,05 |
| Royalties e Compensações Financeiras | 10,032 | 0,111 | 0,315 | 47,03 |
| Contribuições de Melhoria e Econômicas | 5,657 | 0,063 | 0,178 | 26,52 |
| Outros impostos | 0,011 | 0,000 | 0,000 | 0,05 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 90,059 | 0,999 | 2,832 | 422,18 |
| IPTU | 58,564 | 0,650 | 1,841 | 274,54 |
| IRRF | 24,498 | 0,272 | 0,770 | 114,84 |
| ITBI | 20,964 | 0,233 | 0,659 | 98,28 |
| Previd. Municipal | 19,321 | 0,214 | 0,608 | 90,58 |
| TAXAS | 13,480 | 0,150 | 0,424 | 63,19 |
| Contribuições de Melhoria e Econômicas | 12,329 | 0,137 | 0,388 | 57,80 |
| Royalties e Compensações Financeiras | 5,128 | 0,057 | 0,161 | 24,04 |
| Outros impostos | 0,498 | 0,006 | 0,016 | 2,33 |


## PRINCIPAIS TRIBUTOS

| tributo | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Imposto de Renda (Global) | 678,981 | 7,534 | 21,349 | 3.182,96 |
| ICMS | 657,889 | 7,300 | 20,686 | 3.084,08 |
| Previdência Social Ampliada | 484,590 | 5,377 | 15,237 | 2.271,68 |
| Cofins | 297,350 | 3,299 | 9,350 | 1.393,93 |
| CSLL | 134,879 | 1,497 | 4,241 | 632,29 |
| ISS | 90,059 | 0,999 | 2,832 | 422,18 |
| PIS-PASEP | 83,205 | 0,923 | 2,616 | 390,05 |
| IPI | 78,297 | 0,869 | 2,462 | 367,04 |
| Comércio Exterior (Importação + Exportação) | 62,031 | 0,688 | 1,950 | 290,79 |
| IPTU | 58,564 | 0,650 | 1,841 | 274,54 |
| IPVA | 53,402 | 0,593 | 1,679 | 250,34 |
| IOF | 48,141 | 0,534 | 1,514 | 225,68 |
| ITBI | 20,964 | 0,233 | 0,659 | 98,28 |
| ITCD | 12,811 | 0,142 | 0,403 | 60,05 |
| ITR | 2,284 | 0,025 | 0,072 | 10,71 |
| CPMF | 0,028 | 0,000 | 0,001 | 0,13 |
| Demais tributos | 416,854 | 4,625 | 13,107 | 1.954,15 |


## Bases de Incidência

| base de incidência | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| bens_servicos | 1.245,289 | 13,818 | 39,156 | 5.837,72 |
| renda | 813,860 | 9,031 | 25,590 | 3.815,25 |
| salarios | 691,773 | 7,676 | 21,752 | 3.242,92 |
| patrimonio | 257,028 | 2,852 | 8,082 | 1.204,91 |
| comercio_exterior | 62,031 | 0,688 | 1,950 | 290,79 |
| taxas | 52,698 | 0,585 | 1,657 | 247,04 |
| transacoes_financeiras | 48,171 | 0,535 | 1,515 | 225,82 |
| demais | 9,479 | 0,105 | 0,298 | 44,44 |


## RD ESFERA

Ajusta AD ESFERA pelas transferências constitucionais entre entes — o total geral não muda (é redistribuição, não dinheiro novo).

| esfera | AD (R$ bi) | RD (R$ bi) | RD % PIB | RD % total |
|---|---|---|---|---|
| União | 2.067,137 | 1.695,920 | 18,818 | 53,33% |
| Estados | 868,349 | 801,629 | 8,895 | 25,21% |
| Municípios | 244,843 | 682,780 | 7,576 | 21,47% |

### União para Estados

| modalidade | R$ bi |
|---|---|
| FPE | 100,424 |
| Royalties e Compensações Financeiras | 28,142 |
| FUNDEB | 25,129 |
| Salário-Educação (quota estadual) | 13,884 |
| IPI-Exp (FPEx) | 5,697 |
| LC176/2020 (Seguro-Receita ICMS) | 3,511 |
| CIDE | 0,334 |
| IOF-Ouro | 0,023 |
| FEX | 0,000 |
| LC87/1996 (Lei Kandir) | 0,000 |
| **Total** | **177,144** |

### União para Municípios

| modalidade | R$ bi |
|---|---|
| FPM | 115,940 |
| FUNDEB | 47,312 |
| Royalties e Compensações Financeiras | 27,764 |
| ITR | 1,547 |
| LC176/2020 (Seguro-Receita ICMS) | 1,345 |
| CIDE | 0,110 |
| IOF-Ouro | 0,054 |
| FEX | 0,000 |
| LC87/1996 (Lei Kandir) | 0,000 |
| **Total** | **194,072** |

### Estados para Municípios

| modalidade | R$ bi |
|---|---|
| ICMS (cota-parte municipal, líq. FUNDEB) | 131,578 |
| FUNDEB | 84,162 |
| IPVA (cota-parte municipal) | 26,701 |
| IPI-Exp (FPEx) (cota-parte municipal) | 1,424 |
| **Total** | **243,865** |

**Sobre a linha ICMS (cota-parte municipal, líq. FUNDEB):** 25% da arrecadação estadual de ICMS, com a retenção de 20% do FUNDEB (art. 212-A CF) aplicada antes do repasse — 25% × 80% = 20% da arrecadação bruta (decisão do usuário em 2026-08-31, `docs/decisoes-pendentes.md` §9 — em 2024 isso reproduz quase exato o valor publicado, R$ 161,631 bi calculado contra R$ 161,083 bi). A cota do IPVA não tem essa retenção (50% flat).

## Cobertura da imputação municipal

- Municípios no universo: 5.569
- Declarantes: 5.562 (99,96% da população coberta)
- Imputados: 7 (0,014% da receita municipal)
- Faixas com menos de 30 declarantes, mescladas com a faixa vizinha para o cálculo da média: 17←[18]

## O que falta
