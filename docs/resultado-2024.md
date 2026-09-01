# Resultado calculado — 2024

Gerado por `uv run ctb calcular --anos 2024` em 2026-09-01. PIB corrente (2026-09-01, SIDRA tabela 1846): R$ 11.779,251 bi. População (SIDRA tabela 6579): 212.583.750.

Este é o produto da Fase 2 — a primeira vez que o pipeline produz um número, não só valida uma estrutura. A reconciliação rubrica a rubrica por esfera já foi feita na Fase 1 (`uv run ctb dicionario validar`); aqui confere-se o agregado.

## Total geral

**R$ 4.203,383 bi — 35,685% do PIB**

| esfera | R$ bi | % do total |
|---|---|---|
| União | 2.737,373 | 65,12% |
| Estados | 1.106,954 | 26,33% |
| Municípios | 359,056 | 8,54% |

### Por que não fecha exatamente o valor publicado

FGTS e Sistema S (`manual/`, CLAUDE.md §Fontes) estão incluídos desde 2026-09-01 para 2016-2024 — 2025 ainda não tem fonte (ver "O que falta"). O que resta de diferença contra a série antiga vem da decisão 6 (receita líquida em estados e municípios, deliberada, reduz o total frente à metodologia antiga) e de resíduos pequenos já documentados em `docs/divergencias.md`. `docs/revisao-metodologica.md` (`uv run ctb comparar-historico`) tem a comparação ano a ano, linha a linha, com os valores exatos.

## AD ESFERA

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Impostos | 1.018,529 | 8,647 | 24,231 | 4.791,19 |
| Contribuições Sociais | 927,970 | 7,878 | 22,077 | 4.365,20 |
| Previdência Social | 636,975 | 5,408 | 15,154 | 2.996,35 |
| Demais | 153,898 | 1,307 | 3,661 | 723,94 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 808,157 | 6,861 | 19,226 | 3.801,59 |
| IPVA | 87,053 | 0,739 | 2,071 | 409,50 |
| Demais | 211,744 | 1,798 | 5,037 | 996,05 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 142,091 | 1,206 | 3,380 | 668,40 |
| IPTU | 74,042 | 0,629 | 1,761 | 348,29 |
| Demais | 142,923 | 1,213 | 3,400 | 672,31 |


**Contra o valor publicado em 2024** (informativo — a diferença é esperada: opção B redistribuiu os acessórios de volta às rubricas de origem):

| esfera | categoria | calculado | publicado 2024 | diferença |
|---|---|---|---|---|
| União | Impostos | 1.018,529 | 994,879 | +23,650 |
| União | Contribuições Sociais | 927,970 | 710,864 | +217,106 |
| União | Demais | 153,898 | 225,833 | −71,935 |
| Estados | Demais | 211,744 | 211,532 | +0,212 |
| Municípios | Demais | 142,923 | 139,529 | +3,394 |

## byGOVDetalhado

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| IR | 785,151 | 6,666 | 18,679 | 3.693,37 |
| Previdência Social | 636,975 | 5,408 | 15,154 | 2.996,35 |
| Cofins | 367,242 | 3,118 | 8,737 | 1.727,52 |
| FGTS | 192,547 | 1,635 | 4,581 | 905,75 |
| CSLL | 166,760 | 1,416 | 3,967 | 784,44 |
| Royalties e Compensações Financeiras | 109,985 | 0,934 | 2,617 | 517,37 |
| PIS-PASEP | 103,824 | 0,881 | 2,470 | 488,39 |
| IPI | 84,373 | 0,716 | 2,007 | 396,89 |
| Imp. sobre Comércio Exterior | 77,762 | 0,660 | 1,850 | 365,80 |
| IOF | 67,748 | 0,575 | 1,612 | 318,69 |
| Contribuições Econômicas | 34,403 | 0,292 | 0,818 | 161,83 |
| Salário Educação | 33,078 | 0,281 | 0,787 | 155,60 |
| Sistema S | 29,320 | 0,249 | 0,698 | 137,92 |
| Contrib. Seg. Serv. Público | 28,422 | 0,241 | 0,676 | 133,70 |
| Taxas | 9,511 | 0,081 | 0,226 | 44,74 |
| Outras contribuições sociais | 6,794 | 0,058 | 0,162 | 31,96 |
| ITR | 3,493 | 0,030 | 0,083 | 16,43 |
| Outros impostos | 0,001 | 0,000 | 0,000 | 0,01 |
| CPMF | -0,017 | -0,000 | -0,000 | -0,08 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 808,157 | 6,861 | 19,226 | 3.801,59 |
| IPVA | 87,053 | 0,739 | 2,071 | 409,50 |
| IRRF | 81,068 | 0,688 | 1,929 | 381,35 |
| Previ. Estadual | 55,255 | 0,469 | 1,315 | 259,92 |
| TAXAS | 46,690 | 0,396 | 1,111 | 219,63 |
| ITCD | 18,425 | 0,156 | 0,438 | 86,67 |
| Contribuições de Melhoria e Econômicas | 7,449 | 0,063 | 0,177 | 35,04 |
| Royalties e Compensações Financeiras | 2,810 | 0,024 | 0,067 | 13,22 |
| Outros impostos | 0,047 | 0,000 | 0,001 | 0,22 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 142,091 | 1,206 | 3,380 | 668,40 |
| IPTU | 74,042 | 0,629 | 1,761 | 348,29 |
| IRRF | 49,765 | 0,422 | 1,184 | 234,10 |
| Previd. Municipal | 29,330 | 0,249 | 0,698 | 137,97 |
| ITBI | 25,083 | 0,213 | 0,597 | 117,99 |
| TAXAS | 19,386 | 0,165 | 0,461 | 91,19 |
| Contribuições de Melhoria e Econômicas | 16,810 | 0,143 | 0,400 | 79,07 |
| Royalties e Compensações Financeiras | 2,037 | 0,017 | 0,048 | 9,58 |
| Outros impostos | 0,511 | 0,004 | 0,012 | 2,41 |


## PRINCIPAIS TRIBUTOS

| tributo | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Imposto de Renda (Global) | 915,984 | 7,776 | 21,792 | 4.308,81 |
| ICMS | 808,157 | 6,861 | 19,226 | 3.801,59 |
| Previdência Social Ampliada | 721,560 | 6,126 | 17,166 | 3.394,24 |
| Cofins | 367,242 | 3,118 | 8,737 | 1.727,52 |
| CSLL | 166,760 | 1,416 | 3,967 | 784,44 |
| ISS | 142,091 | 1,206 | 3,380 | 668,40 |
| PIS-PASEP | 103,824 | 0,881 | 2,470 | 488,39 |
| IPVA | 87,053 | 0,739 | 2,071 | 409,50 |
| IPI | 84,373 | 0,716 | 2,007 | 396,89 |
| Comércio Exterior (Importação + Exportação) | 77,762 | 0,660 | 1,850 | 365,80 |
| IPTU | 74,042 | 0,629 | 1,761 | 348,29 |
| IOF | 67,748 | 0,575 | 1,612 | 318,69 |
| ITBI | 25,083 | 0,213 | 0,597 | 117,99 |
| ITCD | 18,425 | 0,156 | 0,438 | 86,67 |
| ITR | 3,493 | 0,030 | 0,083 | 16,43 |
| CPMF | -0,017 | -0,000 | -0,000 | -0,08 |
| Demais tributos | 539,803 | 4,583 | 12,842 | 2.539,25 |


**Contra o valor publicado em 2024** (informativo, mesma ressalva da opção B acima):

| tributo | calculado | publicado 2024 | diferença |
|---|---|---|---|
| Imposto de Renda (Global) | 915,984 | 894,479 | +21,505 |
| Previdência Social Ampliada | 721,560 | 673,083 | +48,477 |

## Bases de Incidência

| base de incidência | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| bens_servicos | 1.556,434 | 13,213 | 37,028 | 7.321,51 |
| renda | 1.082,744 | 9,192 | 25,759 | 5.093,26 |
| salarios | 1.007,322 | 8,552 | 23,965 | 4.738,47 |
| patrimonio | 323,019 | 2,742 | 7,685 | 1.519,49 |
| comercio_exterior | 77,762 | 0,660 | 1,850 | 365,80 |
| taxas | 75,588 | 0,642 | 1,798 | 355,57 |
| transacoes_financeiras | 67,731 | 0,575 | 1,611 | 318,61 |
| demais | 12,782 | 0,109 | 0,304 | 60,13 |


## RD ESFERA

Ajusta AD ESFERA pelas transferências constitucionais entre entes — o total geral não muda (é redistribuição, não dinheiro novo).

| esfera | AD (R$ bi) | RD (R$ bi) | RD % PIB | RD % total |
|---|---|---|---|---|
| União | 2.737,373 | 2.178,093 | 18,491 | 51,82% |
| Estados | 1.106,954 | 1.043,246 | 8,857 | 24,82% |
| Municípios | 359,056 | 982,044 | 8,337 | 23,36% |

### União para Estados

| modalidade | R$ bi | publicado 2024 | diferença |
|---|---|---|---|
| FPE | 149,831 | 149,831 | +0,000 |
| FUNDEB | 36,668 | 36,668 | +0,000 |
| Royalties e Compensações Financeiras | 33,410 | 33,410 | +0,000 |
| Salário-Educação (quota estadual) | 22,052 | 21,414 | +0,638 |
| IPI-Exp (FPEx) | 6,765 | 6,765 | −0,000 |
| LC176/2020 (Seguro-Receita ICMS) | 3,000 | 3,000 | −0,000 |
| CIDE | 0,738 | 0,738 | +0,000 |
| LC201/2023 (Compensação ICMS) | 0,674 | 0,674 | +0,000 |
| IOF-Ouro | 0,004 | 0,004 | +0,000 |
| FEX | 0,000 | — | — |
| LC87/1996 (Lei Kandir) | 0,000 | — | — |
| **Total** | **253,142** | | |

### União para Municípios

| modalidade | R$ bi | publicado 2024 | diferença |
|---|---|---|---|
| FPM | 177,034 | 177,034 | −0,000 |
| FUNDEB | 89,855 | 89,855 | +0,000 |
| Royalties e Compensações Financeiras | 35,181 | 35,181 | −0,000 |
| ITR | 2,518 | 2,518 | +0,000 |
| LC176/2020 (Seguro-Receita ICMS) | 0,986 | 0,986 | −0,000 |
| AFM/AFE | 0,314 | 0,314 | +0,000 |
| CIDE | 0,242 | 0,242 | −0,000 |
| IOF-Ouro | 0,009 | 0,009 | −0,000 |
| FEX | 0,000 | — | — |
| LC87/1996 (Lei Kandir) | 0,000 | — | — |
| **Total** | **306,137** | | |

### Estados para Municípios

| modalidade | R$ bi | publicado 2024 | diferença |
|---|---|---|---|
| ICMS (cota-parte municipal, líq. FUNDEB) | 161,631 | 161,083 | +0,549 |
| FUNDEB | 109,833 | 109,833 | +0,000 |
| IPVA (cota-parte municipal) | 43,526 | 43,767 | −0,240 |
| IPI-Exp (FPEx) (cota-parte municipal) | 1,691 | 1,691 | −0,000 |
| LC201/2023 (Compensação ICMS) (cota-parte municipal) | 0,169 | 0,169 | +0,000 |
| **Total** | **316,851** | | |

**Sobre a linha ICMS (cota-parte municipal, líq. FUNDEB):** 25% da arrecadação estadual de ICMS, com a retenção de 20% do FUNDEB (art. 212-A CF) aplicada antes do repasse — 25% × 80% = 20% da arrecadação bruta (decisão do usuário em 2026-08-31, `docs/decisoes-pendentes.md` §9 — em 2024 isso reproduz quase exato o valor publicado, R$ 161,631 bi calculado contra R$ 161,083 bi). A cota do IPVA não tem essa retenção (50% flat).

## Cobertura da imputação municipal

- Municípios no universo: 5.569
- Declarantes: 5.544 (99,82% da população coberta)
- Imputados: 25 (0,095% da receita municipal)
- Faixas com menos de 30 declarantes, mescladas com a faixa vizinha para o cálculo da média: 16←[15], 17←[18]

## O que falta
