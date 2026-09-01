# Resultado calculado — 2016

Gerado por `uv run ctb calcular --anos 2016` em 2026-09-01. PIB corrente (2026-09-01, SIDRA tabela 1846): R$ 6.269,327 bi. População (SIDRA tabela 6579): 206.081.432.

Este é o produto da Fase 2 — a primeira vez que o pipeline produz um número, não só valida uma estrutura. A reconciliação rubrica a rubrica por esfera já foi feita na Fase 1 (`uv run ctb dicionario validar`); aqui confere-se o agregado.

## Total geral

**R$ 2.040,055 bi — 32,540% do PIB**

| esfera | R$ bi | % do total |
|---|---|---|
| União | 1.364,661 | 66,89% |
| Estados | 537,091 | 26,33% |
| Municípios | 138,303 | 6,78% |

### Por que não fecha exatamente o valor publicado

FGTS e Sistema S (`manual/`, CLAUDE.md §Fontes) estão incluídos desde 2026-09-01 para 2016-2024 — 2025 ainda não tem fonte (ver "O que falta"). O que resta de diferença contra a série antiga vem da decisão 6 (receita líquida em estados e municípios, deliberada, reduz o total frente à metodologia antiga) e de resíduos pequenos já documentados em `docs/divergencias.md`. `docs/revisao-metodologica.md` (`uv run ctb comparar-historico`) tem a comparação ano a ano, linha a linha, com os valores exatos.

## AD ESFERA

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Impostos | 450,184 | 7,181 | 22,067 | 2.184,50 |
| Contribuições Sociais | 508,106 | 8,105 | 24,907 | 2.465,56 |
| Previdência Social | 339,673 | 5,418 | 16,650 | 1.648,25 |
| Demais | 66,697 | 1,064 | 3,269 | 323,65 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 406,257 | 6,480 | 19,914 | 1.971,34 |
| IPVA | 37,515 | 0,598 | 1,839 | 182,04 |
| Demais | 93,319 | 1,489 | 4,574 | 452,83 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 53,999 | 0,861 | 2,647 | 262,03 |
| IPTU | 31,465 | 0,502 | 1,542 | 152,68 |
| Demais | 52,839 | 0,843 | 2,590 | 256,40 |


## byGOVDetalhado

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| IR | 341,370 | 5,445 | 16,733 | 1.656,48 |
| Previdência Social | 339,673 | 5,418 | 16,650 | 1.648,25 |
| Cofins | 204,679 | 3,265 | 10,033 | 993,19 |
| FGTS | 119,089 | 1,900 | 5,838 | 577,87 |
| CSLL | 68,143 | 1,087 | 3,340 | 330,66 |
| PIS-PASEP | 53,895 | 0,860 | 2,642 | 261,52 |
| IPI | 42,294 | 0,675 | 2,073 | 205,23 |
| Royalties e Compensações Financeiras | 41,039 | 0,655 | 2,012 | 199,14 |
| IOF | 33,782 | 0,539 | 1,656 | 163,93 |
| Imp. sobre Comércio Exterior | 31,536 | 0,503 | 1,546 | 153,03 |
| Salário Educação | 19,519 | 0,311 | 0,957 | 94,72 |
| Contribuições Econômicas | 17,120 | 0,273 | 0,839 | 83,07 |
| Sistema S | 15,896 | 0,254 | 0,779 | 77,13 |
| Contrib. Seg. Serv. Público | 15,372 | 0,245 | 0,754 | 74,59 |
| Outras contribuições sociais | 11,512 | 0,184 | 0,564 | 55,86 |
| Taxas | 8,539 | 0,136 | 0,419 | 41,43 |
| ITR | 1,198 | 0,019 | 0,059 | 5,81 |
| Outros impostos | 0,003 | 0,000 | 0,000 | 0,02 |
| CPMF | 0,002 | 0,000 | 0,000 | 0,01 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 406,257 | 6,480 | 19,914 | 1.971,34 |
| IPVA | 37,515 | 0,598 | 1,839 | 182,04 |
| Previ. Estadual | 31,700 | 0,506 | 1,554 | 153,82 |
| IRRF | 29,361 | 0,468 | 1,439 | 142,47 |
| TAXAS | 20,420 | 0,326 | 1,001 | 99,09 |
| ITCD | 7,272 | 0,116 | 0,356 | 35,29 |
| Royalties e Compensações Financeiras | 3,520 | 0,056 | 0,173 | 17,08 |
| Contribuições de Melhoria e Econômicas | 1,045 | 0,017 | 0,051 | 5,07 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 53,999 | 0,861 | 2,647 | 262,03 |
| IPTU | 31,465 | 0,502 | 1,542 | 152,68 |
| IRRF | 14,686 | 0,234 | 0,720 | 71,26 |
| Previd. Municipal | 12,329 | 0,197 | 0,604 | 59,83 |
| ITBI | 9,769 | 0,156 | 0,479 | 47,41 |
| TAXAS | 7,745 | 0,124 | 0,380 | 37,58 |
| Contribuições de Melhoria e Econômicas | 7,695 | 0,123 | 0,377 | 37,34 |
| Royalties e Compensações Financeiras | 0,383 | 0,006 | 0,019 | 1,86 |
| Outros impostos | 0,230 | 0,004 | 0,011 | 1,12 |


## PRINCIPAIS TRIBUTOS

| tributo | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 406,257 | 6,480 | 19,914 | 1.971,34 |
| Imposto de Renda (Global) | 385,418 | 6,148 | 18,893 | 1.870,22 |
| Previdência Social Ampliada | 383,702 | 6,120 | 18,808 | 1.861,90 |
| Cofins | 204,679 | 3,265 | 10,033 | 993,19 |
| CSLL | 68,143 | 1,087 | 3,340 | 330,66 |
| ISS | 53,999 | 0,861 | 2,647 | 262,03 |
| PIS-PASEP | 53,895 | 0,860 | 2,642 | 261,52 |
| IPI | 42,294 | 0,675 | 2,073 | 205,23 |
| IPVA | 37,515 | 0,598 | 1,839 | 182,04 |
| IOF | 33,782 | 0,539 | 1,656 | 163,93 |
| Comércio Exterior (Importação + Exportação) | 31,536 | 0,503 | 1,546 | 153,03 |
| IPTU | 31,465 | 0,502 | 1,542 | 152,68 |
| ITBI | 9,769 | 0,156 | 0,479 | 47,41 |
| ITCD | 7,272 | 0,116 | 0,356 | 35,29 |
| ITR | 1,198 | 0,019 | 0,059 | 5,81 |
| CPMF | 0,002 | 0,000 | 0,000 | 0,01 |
| Demais tributos | 289,129 | 4,612 | 14,173 | 1.402,98 |


## Bases de Incidência

| base de incidência | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| bens_servicos | 783,789 | 12,502 | 38,420 | 3.803,30 |
| salarios | 561,950 | 8,963 | 27,546 | 2.726,83 |
| renda | 453,561 | 7,235 | 22,233 | 2.200,88 |
| patrimonio | 132,393 | 2,112 | 6,490 | 642,43 |
| taxas | 36,704 | 0,585 | 1,799 | 178,10 |
| transacoes_financeiras | 33,784 | 0,539 | 1,656 | 163,94 |
| comercio_exterior | 31,536 | 0,503 | 1,546 | 153,03 |
| demais | 6,338 | 0,101 | 0,311 | 30,76 |


## RD ESFERA

Ajusta AD ESFERA pelas transferências constitucionais entre entes — o total geral não muda (é redistribuição, não dinheiro novo).

| esfera | AD (R$ bi) | RD (R$ bi) | RD % PIB | RD % total |
|---|---|---|---|---|
| União | 1.364,661 | 1.124,565 | 17,938 | 55,12% |
| Estados | 537,091 | 504,166 | 8,042 | 24,71% |
| Municípios | 138,303 | 411,324 | 6,561 | 20,16% |

### União para Estados

| modalidade | R$ bi |
|---|---|
| FPE | 69,911 |
| FUNDEB | 18,924 |
| Salário-Educação (quota estadual) | 13,013 |
| Royalties e Compensações Financeiras | 7,573 |
| IPI-Exp (FPEx) | 3,408 |
| FEX | 2,925 |
| LC87/1996 (Lei Kandir) | 1,173 |
| CIDE | 0,934 |
| IOF-Ouro | 0,009 |
| LC176/2020 (Seguro-Receita ICMS) | 0,000 |
| **Total** | **117,870** |

### União para Municípios

| modalidade | R$ bi |
|---|---|
| FPM | 79,911 |
| FUNDEB | 31,985 |
| Royalties e Compensações Financeiras | 7,745 |
| FEX | 0,975 |
| ITR | 0,897 |
| LC87/1996 (Lei Kandir) | 0,387 |
| CIDE | 0,305 |
| IOF-Ouro | 0,021 |
| LC176/2020 (Seguro-Receita ICMS) | 0,000 |
| **Total** | **122,226** |

### Estados para Municípios

| modalidade | R$ bi |
|---|---|
| ICMS (cota-parte municipal, líq. FUNDEB) | 81,251 |
| FUNDEB | 49,934 |
| IPVA (cota-parte municipal) | 18,757 |
| IPI-Exp (FPEx) (cota-parte municipal) | 0,852 |
| **Total** | **150,795** |

**Sobre a linha ICMS (cota-parte municipal, líq. FUNDEB):** 25% da arrecadação estadual de ICMS, com a retenção de 20% do FUNDEB (art. 212-A CF) aplicada antes do repasse — 25% × 80% = 20% da arrecadação bruta (decisão do usuário em 2026-08-31, `docs/decisoes-pendentes.md` §9 — em 2024 isso reproduz quase exato o valor publicado, R$ 161,631 bi calculado contra R$ 161,083 bi). A cota do IPVA não tem essa retenção (50% flat).

## Cobertura da imputação municipal

- Municípios no universo: 5.569
- Declarantes: 5.442 (98,65% da população coberta)
- Imputados: 127 (0,659% da receita municipal)
- Faixas com menos de 30 declarantes, mescladas com a faixa vizinha para o cálculo da média: 16←[15], 17←[18]

## O que falta
