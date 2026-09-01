# Resultado calculado — 2018

Gerado por `uv run ctb calcular --anos 2018` em 2026-09-01. PIB corrente (2026-09-01, SIDRA tabela 1846): R$ 7.004,141 bi. População (SIDRA tabela 6579): 208.494.900.

Este é o produto da Fase 2 — a primeira vez que o pipeline produz um número, não só valida uma estrutura. A reconciliação rubrica a rubrica por esfera já foi feita na Fase 1 (`uv run ctb dicionario validar`); aqui confere-se o agregado.

## Total geral

**R$ 2.380,757 bi — 33,991% do PIB**

| esfera | R$ bi | % do total |
|---|---|---|
| União | 1.566,612 | 65,80% |
| Estados | 639,259 | 26,85% |
| Municípios | 174,886 | 7,35% |

### Por que não fecha exatamente o valor publicado

FGTS e Sistema S (`manual/`, CLAUDE.md §Fontes) estão incluídos desde 2026-09-01 para 2016-2024 — 2025 ainda não tem fonte (ver "O que falta"). O que resta de diferença contra a série antiga vem da decisão 6 (receita líquida em estados e municípios, deliberada, reduz o total frente à metodologia antiga) e de resíduos pequenos já documentados em `docs/divergencias.md`. `docs/revisao-metodologica.md` (`uv run ctb comparar-historico`) tem a comparação ano a ano, linha a linha, com os valores exatos.

## AD ESFERA

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Impostos | 497,565 | 7,104 | 20,899 | 2.386,46 |
| Contribuições Sociais | 584,547 | 8,346 | 24,553 | 2.803,65 |
| Previdência Social | 378,771 | 5,408 | 15,910 | 1.816,69 |
| Demais | 105,728 | 1,510 | 4,441 | 507,10 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 481,231 | 6,871 | 20,213 | 2.308,12 |
| IPVA | 44,238 | 0,632 | 1,858 | 212,18 |
| Demais | 113,789 | 1,625 | 4,780 | 545,76 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 63,781 | 0,911 | 2,679 | 305,91 |
| IPTU | 44,692 | 0,638 | 1,877 | 214,35 |
| Demais | 66,414 | 0,948 | 2,790 | 318,54 |


## byGOVDetalhado

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Previdência Social | 378,771 | 5,408 | 15,910 | 1.816,69 |
| IR | 363,055 | 5,183 | 15,250 | 1.741,31 |
| Cofins | 251,466 | 3,590 | 10,562 | 1.206,10 |
| FGTS | 120,658 | 1,723 | 5,068 | 578,71 |
| CSLL | 78,549 | 1,121 | 3,299 | 376,74 |
| Royalties e Compensações Financeiras | 77,213 | 1,102 | 3,243 | 370,34 |
| PIS-PASEP | 66,125 | 0,944 | 2,777 | 317,15 |
| IPI | 55,427 | 0,791 | 2,328 | 265,84 |
| Imp. sobre Comércio Exterior | 40,812 | 0,583 | 1,714 | 195,75 |
| IOF | 36,786 | 0,525 | 1,545 | 176,44 |
| Salário Educação | 22,048 | 0,315 | 0,926 | 105,75 |
| Contribuições Econômicas | 18,906 | 0,270 | 0,794 | 90,68 |
| Contrib. Seg. Serv. Público | 17,418 | 0,249 | 0,732 | 83,54 |
| Sistema S | 17,083 | 0,244 | 0,718 | 81,93 |
| Outras contribuições sociais | 11,205 | 0,160 | 0,471 | 53,74 |
| Taxas | 9,609 | 0,137 | 0,404 | 46,09 |
| ITR | 1,481 | 0,021 | 0,062 | 7,10 |
| Outros impostos | 0,003 | 0,000 | 0,000 | 0,02 |
| CPMF | -0,004 | -0,000 | -0,000 | -0,02 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 481,231 | 6,871 | 20,213 | 2.308,12 |
| IPVA | 44,238 | 0,632 | 1,858 | 212,18 |
| IRRF | 43,026 | 0,614 | 1,807 | 206,37 |
| Previ. Estadual | 34,825 | 0,497 | 1,463 | 167,03 |
| TAXAS | 24,187 | 0,345 | 1,016 | 116,01 |
| ITCD | 7,729 | 0,110 | 0,325 | 37,07 |
| Contribuições de Melhoria e Econômicas | 3,339 | 0,048 | 0,140 | 16,02 |
| Outros impostos | 0,472 | 0,007 | 0,020 | 2,26 |
| Royalties e Compensações Financeiras | 0,211 | 0,003 | 0,009 | 1,01 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 63,781 | 0,911 | 2,679 | 305,91 |
| IPTU | 44,692 | 0,638 | 1,877 | 214,35 |
| IRRF | 18,297 | 0,261 | 0,769 | 87,76 |
| Previd. Municipal | 13,995 | 0,200 | 0,588 | 67,12 |
| ITBI | 11,497 | 0,164 | 0,483 | 55,14 |
| TAXAS | 10,933 | 0,156 | 0,459 | 52,44 |
| Contribuições de Melhoria e Econômicas | 9,361 | 0,134 | 0,393 | 44,90 |
| Outros impostos | 1,880 | 0,027 | 0,079 | 9,02 |
| Royalties e Compensações Financeiras | 0,453 | 0,006 | 0,019 | 2,17 |


## PRINCIPAIS TRIBUTOS

| tributo | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 481,231 | 6,871 | 20,213 | 2.308,12 |
| Previdência Social Ampliada | 427,591 | 6,105 | 17,960 | 2.050,85 |
| Imposto de Renda (Global) | 424,378 | 6,059 | 17,825 | 2.035,43 |
| Cofins | 251,466 | 3,590 | 10,562 | 1.206,10 |
| CSLL | 78,549 | 1,121 | 3,299 | 376,74 |
| PIS-PASEP | 66,125 | 0,944 | 2,777 | 317,15 |
| ISS | 63,781 | 0,911 | 2,679 | 305,91 |
| IPI | 55,427 | 0,791 | 2,328 | 265,84 |
| IPTU | 44,692 | 0,638 | 1,877 | 214,35 |
| IPVA | 44,238 | 0,632 | 1,858 | 212,18 |
| Comércio Exterior (Importação + Exportação) | 40,812 | 0,583 | 1,714 | 195,75 |
| IOF | 36,786 | 0,525 | 1,545 | 176,44 |
| ITBI | 11,497 | 0,164 | 0,483 | 55,14 |
| ITCD | 7,729 | 0,110 | 0,325 | 37,07 |
| ITR | 1,481 | 0,021 | 0,062 | 7,10 |
| CPMF | -0,004 | -0,000 | -0,000 | -0,02 |
| Demais tributos | 344,977 | 4,925 | 14,490 | 1.654,60 |


## Bases de Incidência

| base de incidência | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| bens_servicos | 945,611 | 13,501 | 39,719 | 4.535,42 |
| salarios | 612,293 | 8,742 | 25,718 | 2.936,73 |
| renda | 502,927 | 7,180 | 21,125 | 2.412,18 |
| patrimonio | 187,886 | 2,683 | 7,892 | 901,15 |
| taxas | 44,728 | 0,639 | 1,879 | 214,53 |
| comercio_exterior | 40,812 | 0,583 | 1,714 | 195,75 |
| transacoes_financeiras | 36,782 | 0,525 | 1,545 | 176,42 |
| demais | 9,716 | 0,139 | 0,408 | 46,60 |


## RD ESFERA

Ajusta AD ESFERA pelas transferências constitucionais entre entes — o total geral não muda (é redistribuição, não dinheiro novo).

| esfera | AD (R$ bi) | RD (R$ bi) | RD % PIB | RD % total |
|---|---|---|---|---|
| União | 1.566,612 | 1.300,908 | 18,573 | 54,64% |
| Estados | 639,259 | 595,610 | 8,504 | 25,02% |
| Municípios | 174,886 | 484,238 | 6,914 | 20,34% |

### União para Estados

| modalidade | R$ bi |
|---|---|
| FPE | 71,481 |
| Royalties e Compensações Financeiras | 20,375 |
| FUNDEB | 19,145 |
| Salário-Educação (quota estadual) | 14,698 |
| IPI-Exp (FPEx) | 4,453 |
| LC87/1996 (Lei Kandir) | 1,149 |
| CIDE | 1,022 |
| IOF-Ouro | 0,005 |
| LC176/2020 (Seguro-Receita ICMS) | 0,000 |
| FEX | 0,000 |
| **Total** | **132,329** |

### União para Municípios

| modalidade | R$ bi |
|---|---|
| FPM | 83,011 |
| FUNDEB | 33,008 |
| Royalties e Compensações Financeiras | 15,546 |
| ITR | 1,086 |
| LC87/1996 (Lei Kandir) | 0,379 |
| CIDE | 0,334 |
| IOF-Ouro | 0,011 |
| LC176/2020 (Seguro-Receita ICMS) | 0,000 |
| FEX | 0,000 |
| **Total** | **133,375** |

### Estados para Municípios

| modalidade | R$ bi |
|---|---|
| ICMS (cota-parte municipal, líq. FUNDEB) | 96,246 |
| FUNDEB | 56,498 |
| IPVA (cota-parte municipal) | 22,119 |
| IPI-Exp (FPEx) (cota-parte municipal) | 1,113 |
| **Total** | **175,977** |

**Sobre a linha ICMS (cota-parte municipal, líq. FUNDEB):** 25% da arrecadação estadual de ICMS, com a retenção de 20% do FUNDEB (art. 212-A CF) aplicada antes do repasse — 25% × 80% = 20% da arrecadação bruta (decisão do usuário em 2026-08-31, `docs/decisoes-pendentes.md` §9 — em 2024 isso reproduz quase exato o valor publicado, R$ 161,631 bi calculado contra R$ 161,083 bi). A cota do IPVA não tem essa retenção (50% flat).

## Cobertura da imputação municipal

- Municípios no universo: 5.569
- Declarantes: 5.536 (99,77% da população coberta)
- Imputados: 33 (0,098% da receita municipal)
- Faixas com menos de 30 declarantes, mescladas com a faixa vizinha para o cálculo da média: 16←[15], 17←[18]

## O que falta
