# Resultado calculado — 2019

Gerado por `uv run ctb calcular --anos 2019` em 2026-09-01. PIB corrente (2026-09-01, SIDRA tabela 1846): R$ 7.389,131 bi. População (SIDRA tabela 6579): 210.147.125.

Este é o produto da Fase 2 — a primeira vez que o pipeline produz um número, não só valida uma estrutura. A reconciliação rubrica a rubrica por esfera já foi feita na Fase 1 (`uv run ctb dicionario validar`); aqui confere-se o agregado.

## Total geral

**R$ 2.572,402 bi — 34,813% do PIB**

| esfera | R$ bi | % do total |
|---|---|---|
| União | 1.693,993 | 65,85% |
| Estados | 682,102 | 26,52% |
| Municípios | 196,307 | 7,63% |

### Por que não fecha exatamente o valor publicado

FGTS e Sistema S (`manual/`, CLAUDE.md §Fontes) estão incluídos desde 2026-09-01 para 2016-2024 — 2025 ainda não tem fonte (ver "O que falta"). O que resta de diferença contra a série antiga vem da decisão 6 (receita líquida em estados e municípios, deliberada, reduz o total frente à metodologia antiga) e de resíduos pequenos já documentados em `docs/divergencias.md`. `docs/revisao-metodologica.md` (`uv run ctb comparar-historico`) tem a comparação ano a ano, linha a linha, com os valores exatos.

## AD ESFERA

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Impostos | 537,225 | 7,270 | 20,884 | 2.556,42 |
| Contribuições Sociais | 712,206 | 9,639 | 27,686 | 3.389,08 |
| Previdência Social | 271,957 | 3,681 | 10,572 | 1.294,13 |
| Demais | 172,606 | 2,336 | 6,710 | 821,36 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 511,279 | 6,919 | 19,876 | 2.432,96 |
| IPVA | 47,398 | 0,641 | 1,843 | 225,54 |
| Demais | 123,426 | 1,670 | 4,798 | 587,33 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 72,503 | 0,981 | 2,819 | 345,01 |
| IPTU | 50,222 | 0,680 | 1,952 | 238,99 |
| Demais | 73,582 | 0,996 | 2,860 | 350,14 |


## byGOVDetalhado

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| IR | 398,634 | 5,395 | 15,497 | 1.896,93 |
| Previdência Social | 271,957 | 3,681 | 10,572 | 1.294,13 |
| Cofins | 238,696 | 3,230 | 9,279 | 1.135,85 |
| Royalties e Compensações Financeiras | 148,276 | 2,007 | 5,764 | 705,58 |
| Outras contribuições sociais | 140,418 | 1,900 | 5,459 | 668,19 |
| FGTS | 128,710 | 1,742 | 5,003 | 612,48 |
| CSLL | 82,018 | 1,110 | 3,188 | 390,29 |
| PIS-PASEP | 64,751 | 0,876 | 2,517 | 308,12 |
| IPI | 52,686 | 0,713 | 2,048 | 250,71 |
| Imp. sobre Comércio Exterior | 43,133 | 0,584 | 1,677 | 205,25 |
| IOF | 41,044 | 0,555 | 1,596 | 195,31 |
| Salário Educação | 22,105 | 0,299 | 0,859 | 105,19 |
| Sistema S | 17,791 | 0,241 | 0,692 | 84,66 |
| Contrib. Seg. Serv. Público | 17,745 | 0,240 | 0,690 | 84,44 |
| Contribuições Econômicas | 15,745 | 0,213 | 0,612 | 74,93 |
| Taxas | 8,584 | 0,116 | 0,334 | 40,85 |
| ITR | 1,706 | 0,023 | 0,066 | 8,12 |
| Outros impostos | 0,022 | 0,000 | 0,001 | 0,11 |
| CPMF | -0,030 | -0,000 | -0,001 | -0,14 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 511,279 | 6,919 | 19,876 | 2.432,96 |
| IPVA | 47,398 | 0,641 | 1,843 | 225,54 |
| IRRF | 46,741 | 0,633 | 1,817 | 222,42 |
| Previ. Estadual | 35,699 | 0,483 | 1,388 | 169,88 |
| TAXAS | 27,031 | 0,366 | 1,051 | 128,63 |
| ITCD | 8,962 | 0,121 | 0,348 | 42,65 |
| Contribuições de Melhoria e Econômicas | 3,817 | 0,052 | 0,148 | 18,17 |
| Royalties e Compensações Financeiras | 1,095 | 0,015 | 0,043 | 5,21 |
| Outros impostos | 0,080 | 0,001 | 0,003 | 0,38 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 72,503 | 0,981 | 2,819 | 345,01 |
| IPTU | 50,222 | 0,680 | 1,952 | 238,99 |
| IRRF | 20,403 | 0,276 | 0,793 | 97,09 |
| Previd. Municipal | 15,488 | 0,210 | 0,602 | 73,70 |
| ITBI | 12,852 | 0,174 | 0,500 | 61,16 |
| TAXAS | 12,105 | 0,164 | 0,471 | 57,60 |
| Contribuições de Melhoria e Econômicas | 11,175 | 0,151 | 0,434 | 53,18 |
| Outros impostos | 0,996 | 0,013 | 0,039 | 4,74 |
| Royalties e Compensações Financeiras | 0,563 | 0,008 | 0,022 | 2,68 |


## PRINCIPAIS TRIBUTOS

| tributo | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 511,279 | 6,919 | 19,876 | 2.432,96 |
| Imposto de Renda (Global) | 465,777 | 6,304 | 18,107 | 2.216,44 |
| Previdência Social Ampliada | 323,145 | 4,373 | 12,562 | 1.537,71 |
| Cofins | 238,696 | 3,230 | 9,279 | 1.135,85 |
| CSLL | 82,018 | 1,110 | 3,188 | 390,29 |
| ISS | 72,503 | 0,981 | 2,819 | 345,01 |
| PIS-PASEP | 64,751 | 0,876 | 2,517 | 308,12 |
| IPI | 52,686 | 0,713 | 2,048 | 250,71 |
| IPTU | 50,222 | 0,680 | 1,952 | 238,99 |
| IPVA | 47,398 | 0,641 | 1,843 | 225,54 |
| Comércio Exterior (Importação + Exportação) | 43,133 | 0,584 | 1,677 | 205,25 |
| IOF | 41,044 | 0,555 | 1,596 | 195,31 |
| ITBI | 12,852 | 0,174 | 0,500 | 61,16 |
| ITCD | 8,962 | 0,121 | 0,348 | 42,65 |
| ITR | 1,706 | 0,023 | 0,066 | 8,12 |
| CPMF | -0,030 | -0,000 | -0,001 | -0,14 |
| Demais tributos | 556,261 | 7,528 | 21,624 | 2.647,01 |


## Bases de Incidência

| base de incidência | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| bens_servicos | 966,045 | 13,074 | 37,554 | 4.596,99 |
| renda | 547,796 | 7,414 | 21,295 | 2.606,73 |
| salarios | 516,628 | 6,992 | 20,083 | 2.458,41 |
| patrimonio | 271,291 | 3,671 | 10,546 | 1.290,96 |
| demais | 138,775 | 1,878 | 5,395 | 660,37 |
| taxas | 47,721 | 0,646 | 1,855 | 227,08 |
| comercio_exterior | 43,133 | 0,584 | 1,677 | 205,25 |
| transacoes_financeiras | 41,014 | 0,555 | 1,594 | 195,17 |


## RD ESFERA

Ajusta AD ESFERA pelas transferências constitucionais entre entes — o total geral não muda (é redistribuição, não dinheiro novo).

| esfera | AD (R$ bi) | RD (R$ bi) | RD % PIB | RD % total |
|---|---|---|---|---|
| União | 1.693,993 | 1.397,291 | 18,910 | 54,32% |
| Estados | 682,102 | 637,048 | 8,621 | 24,76% |
| Municípios | 196,307 | 538,064 | 7,282 | 20,92% |

### União para Estados

| modalidade | R$ bi |
|---|---|
| FPE | 77,950 |
| Royalties e Compensações Financeiras | 21,141 |
| FUNDEB | 20,414 |
| Salário-Educação (quota estadual) | 14,736 |
| Cessão Onerosa | 6,398 |
| IPI-Exp (FPEx) | 4,281 |
| CIDE | 0,619 |
| IOF-Ouro | 0,008 |
| LC176/2020 (Seguro-Receita ICMS) | 0,000 |
| FEX | 0,000 |
| LC87/1996 (Lei Kandir) | 0,000 |
| **Total** | **145,548** |

### União para Municípios

| modalidade | R$ bi |
|---|---|
| FPM | 90,409 |
| FUNDEB | 36,422 |
| Royalties e Compensações Financeiras | 17,643 |
| Cessão Onerosa | 5,332 |
| ITR | 1,127 |
| CIDE | 0,202 |
| IOF-Ouro | 0,018 |
| LC176/2020 (Seguro-Receita ICMS) | 0,000 |
| FEX | 0,000 |
| LC87/1996 (Lei Kandir) | 0,000 |
| **Total** | **151,154** |

### Estados para Municípios

| modalidade | R$ bi |
|---|---|
| ICMS (cota-parte municipal, líq. FUNDEB) | 102,256 |
| FUNDEB | 63,577 |
| IPVA (cota-parte municipal) | 23,699 |
| IPI-Exp (FPEx) (cota-parte municipal) | 1,070 |
| **Total** | **190,602** |

**Sobre a linha ICMS (cota-parte municipal, líq. FUNDEB):** 25% da arrecadação estadual de ICMS, com a retenção de 20% do FUNDEB (art. 212-A CF) aplicada antes do repasse — 25% × 80% = 20% da arrecadação bruta (decisão do usuário em 2026-08-31, `docs/decisoes-pendentes.md` §9 — em 2024 isso reproduz quase exato o valor publicado, R$ 161,631 bi calculado contra R$ 161,083 bi). A cota do IPVA não tem essa retenção (50% flat).

## Cobertura da imputação municipal

- Municípios no universo: 5.569
- Declarantes: 5.553 (99,90% da população coberta)
- Imputados: 16 (0,049% da receita municipal)
- Faixas com menos de 30 declarantes, mescladas com a faixa vizinha para o cálculo da média: 16←[15], 17←[18]

## O que falta
