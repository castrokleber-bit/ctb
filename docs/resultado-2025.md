# Resultado calculado — 2025

Gerado por `uv run ctb calcular --anos 2025` em 2026-09-01. PIB corrente (2026-09-01, SIDRA tabela 1846): R$ 12.738,566 bi. População (SIDRA tabela 6579): 213.421.037.

Este é o produto da Fase 2 — a primeira vez que o pipeline produz um número, não só valida uma estrutura. A reconciliação rubrica a rubrica por esfera já foi feita na Fase 1 (`uv run ctb dicionario validar`); aqui confere-se o agregado.

## Total geral

**R$ 4.573,066 bi — 35,899% do PIB**

| esfera | R$ bi | % do total |
|---|---|---|
| União | 2.989,881 | 65,38% |
| Estados | 1.188,315 | 25,99% |
| Municípios | 394,870 | 8,63% |

### Por que não fecha exatamente o valor publicado

FGTS e Sistema S (`manual/`, CLAUDE.md §Fontes) estão incluídos desde 2026-09-01 para 2016-2024 — 2025 ainda não tem fonte (ver "O que falta"). O que resta de diferença contra a série antiga vem da decisão 6 (receita líquida em estados e municípios, deliberada, reduz o total frente à metodologia antiga) e de resíduos pequenos já documentados em `docs/divergencias.md`. `docs/revisao-metodologica.md` (`uv run ctb comparar-historico`) tem a comparação ano a ano, linha a linha, com os valores exatos.

## AD ESFERA

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Impostos | 1.136,666 | 8,923 | 24,856 | 5.325,93 |
| Contribuições Sociais | 992,820 | 7,794 | 21,710 | 4.651,93 |
| Previdência Social | 707,445 | 5,554 | 15,470 | 3.314,78 |
| Demais | 152,950 | 1,201 | 3,345 | 716,66 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 862,873 | 6,774 | 18,869 | 4.043,05 |
| IPVA | 93,969 | 0,738 | 2,055 | 440,30 |
| Demais | 231,474 | 1,817 | 5,062 | 1.084,59 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 158,124 | 1,241 | 3,458 | 740,90 |
| IPTU | 81,802 | 0,642 | 1,789 | 383,29 |
| Demais | 154,944 | 1,216 | 3,388 | 726,00 |


## byGOVDetalhado

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| IR | 867,295 | 6,808 | 18,965 | 4.063,77 |
| Previdência Social | 707,445 | 5,554 | 15,470 | 3.314,78 |
| Cofins | 391,525 | 3,074 | 8,562 | 1.834,52 |
| FGTS | 212,594 | 1,669 | 4,649 | 996,13 |
| CSLL | 177,797 | 1,396 | 3,888 | 833,08 |
| Royalties e Compensações Financeiras | 110,525 | 0,868 | 2,417 | 517,87 |
| PIS-PASEP | 105,881 | 0,831 | 2,315 | 496,11 |
| Imp. sobre Comércio Exterior | 90,395 | 0,710 | 1,977 | 423,55 |
| IPI | 88,363 | 0,694 | 1,932 | 414,03 |
| IOF | 86,380 | 0,678 | 1,889 | 404,74 |
| Salário Educação | 35,981 | 0,282 | 0,787 | 168,59 |
| Contribuições Econômicas | 32,599 | 0,256 | 0,713 | 152,75 |
| Sistema S | 32,385 | 0,254 | 0,708 | 151,74 |
| Contrib. Seg. Serv. Público | 29,173 | 0,229 | 0,638 | 136,69 |
| Taxas | 9,826 | 0,077 | 0,215 | 46,04 |
| Outras contribuições sociais | 6,768 | 0,053 | 0,148 | 31,71 |
| ITR | 4,229 | 0,033 | 0,092 | 19,82 |
| CPMF | 0,716 | 0,006 | 0,016 | 3,36 |
| Outros impostos | 0,004 | 0,000 | 0,000 | 0,02 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 862,873 | 6,774 | 18,869 | 4.043,05 |
| IPVA | 93,969 | 0,738 | 2,055 | 440,30 |
| IRRF | 90,644 | 0,712 | 1,982 | 424,72 |
| Previ. Estadual | 58,942 | 0,463 | 1,289 | 276,18 |
| TAXAS | 51,419 | 0,404 | 1,124 | 240,93 |
| ITCD | 20,168 | 0,158 | 0,441 | 94,50 |
| Contribuições de Melhoria e Econômicas | 7,758 | 0,061 | 0,170 | 36,35 |
| Royalties e Compensações Financeiras | 2,462 | 0,019 | 0,054 | 11,54 |
| Outros impostos | 0,081 | 0,001 | 0,002 | 0,38 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 158,124 | 1,241 | 3,458 | 740,90 |
| IPTU | 81,802 | 0,642 | 1,789 | 383,29 |
| IRRF | 55,092 | 0,432 | 1,205 | 258,14 |
| Previd. Municipal | 31,485 | 0,247 | 0,688 | 147,52 |
| ITBI | 27,446 | 0,215 | 0,600 | 128,60 |
| TAXAS | 21,043 | 0,165 | 0,460 | 98,60 |
| Contribuições de Melhoria e Econômicas | 17,552 | 0,138 | 0,384 | 82,24 |
| Royalties e Compensações Financeiras | 1,673 | 0,013 | 0,037 | 7,84 |
| Outros impostos | 0,654 | 0,005 | 0,014 | 3,06 |


## PRINCIPAIS TRIBUTOS

| tributo | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Imposto de Renda (Global) | 1.013,031 | 7,952 | 22,152 | 4.746,63 |
| ICMS | 862,873 | 6,774 | 18,869 | 4.043,05 |
| Previdência Social Ampliada | 797,872 | 6,263 | 17,447 | 3.738,49 |
| Cofins | 391,525 | 3,074 | 8,562 | 1.834,52 |
| CSLL | 177,797 | 1,396 | 3,888 | 833,08 |
| ISS | 158,124 | 1,241 | 3,458 | 740,90 |
| PIS-PASEP | 105,881 | 0,831 | 2,315 | 496,11 |
| IPVA | 93,969 | 0,738 | 2,055 | 440,30 |
| Comércio Exterior (Importação + Exportação) | 90,395 | 0,710 | 1,977 | 423,55 |
| IPI | 88,363 | 0,694 | 1,932 | 414,03 |
| IOF | 86,380 | 0,678 | 1,889 | 404,74 |
| IPTU | 81,802 | 0,642 | 1,789 | 383,29 |
| ITBI | 27,446 | 0,215 | 0,600 | 128,60 |
| ITCD | 20,168 | 0,158 | 0,441 | 94,50 |
| ITR | 4,229 | 0,033 | 0,092 | 19,82 |
| CPMF | 0,716 | 0,006 | 0,016 | 3,36 |
| Demais tributos | 572,497 | 4,494 | 12,519 | 2.682,48 |


## Bases de Incidência

| base de incidência | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| bens_servicos | 1.656,561 | 13,004 | 36,224 | 7.761,94 |
| renda | 1.190,827 | 9,348 | 26,040 | 5.579,71 |
| salarios | 1.111,029 | 8,722 | 24,295 | 5.205,81 |
| patrimonio | 342,334 | 2,687 | 7,486 | 1.604,03 |
| comercio_exterior | 90,395 | 0,710 | 1,977 | 423,55 |
| transacoes_financeiras | 87,097 | 0,684 | 1,905 | 408,10 |
| taxas | 82,287 | 0,646 | 1,799 | 385,56 |
| demais | 12,535 | 0,098 | 0,274 | 58,74 |


## RD ESFERA

Ajusta AD ESFERA pelas transferências constitucionais entre entes — o total geral não muda (é redistribuição, não dinheiro novo).

| esfera | AD (R$ bi) | RD (R$ bi) | RD % PIB | RD % total |
|---|---|---|---|---|
| União | 2.989,881 | 2.375,418 | 18,647 | 51,94% |
| Estados | 1.188,315 | 1.120,956 | 8,800 | 24,51% |
| Municípios | 394,870 | 1.076,692 | 8,452 | 23,54% |

### União para Estados

| modalidade | R$ bi |
|---|---|
| FPE | 163,970 |
| FUNDEB | 40,446 |
| Royalties e Compensações Financeiras | 33,213 |
| Salário-Educação (quota estadual) | 23,987 |
| IPI-Exp (FPEx) | 7,024 |
| LC176/2020 (Seguro-Receita ICMS) | 3,000 |
| CIDE | 0,691 |
| LC201/2023 (Compensação ICMS) | 0,274 |
| IOF-Ouro | 0,011 |
| FEX | 0,000 |
| LC87/1996 (Lei Kandir) | 0,000 |
| **Total** | **272,618** |

### União para Municípios

| modalidade | R$ bi |
|---|---|
| FPM | 198,040 |
| FUNDEB | 102,891 |
| Royalties e Compensações Financeiras | 36,757 |
| ITR | 2,920 |
| LC176/2020 (Seguro-Receita ICMS) | 0,985 |
| CIDE | 0,226 |
| IOF-Ouro | 0,027 |
| FEX | 0,000 |
| LC87/1996 (Lei Kandir) | 0,000 |
| **Total** | **341,846** |

### Estados para Municípios

| modalidade | R$ bi |
|---|---|
| ICMS (cota-parte municipal, líq. FUNDEB) | 172,575 |
| FUNDEB | 118,593 |
| IPVA (cota-parte municipal) | 46,984 |
| IPI-Exp (FPEx) (cota-parte municipal) | 1,756 |
| LC201/2023 (Compensação ICMS) (cota-parte municipal) | 0,069 |
| **Total** | **339,977** |

**Sobre a linha ICMS (cota-parte municipal, líq. FUNDEB):** 25% da arrecadação estadual de ICMS, com a retenção de 20% do FUNDEB (art. 212-A CF) aplicada antes do repasse — 25% × 80% = 20% da arrecadação bruta (decisão do usuário em 2026-08-31, `docs/decisoes-pendentes.md` §9 — em 2024 isso reproduz quase exato o valor publicado, R$ 161,631 bi calculado contra R$ 161,083 bi). A cota do IPVA não tem essa retenção (50% flat).

## Cobertura da imputação municipal

- Municípios no universo: 5.569
- Declarantes: 5.481 (98,86% da população coberta)
- Imputados: 88 (0,943% da receita municipal)
- Faixas com menos de 30 declarantes, mescladas com a faixa vizinha para o cálculo da média: 16←[15], 17←[18]

## O que falta
