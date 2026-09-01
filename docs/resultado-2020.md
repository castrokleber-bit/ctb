# Resultado calculado — 2020

Gerado por `uv run ctb calcular --anos 2020` em 2026-09-01. PIB corrente (2026-09-01, SIDRA tabela 1846): R$ 7.609,597 bi. População (SIDRA tabela 6579): 211.755.692.

Este é o produto da Fase 2 — a primeira vez que o pipeline produz um número, não só valida uma estrutura. A reconciliação rubrica a rubrica por esfera já foi feita na Fase 1 (`uv run ctb dicionario validar`); aqui confere-se o agregado.

## Total geral

**R$ 2.551,494 bi — 33,530% do PIB**

| esfera | R$ bi | % do total |
|---|---|---|
| União | 1.649,118 | 64,63% |
| Estados | 699,997 | 27,43% |
| Municípios | 202,379 | 7,93% |

### Por que não fecha exatamente o valor publicado

FGTS e Sistema S (`manual/`, CLAUDE.md §Fontes) estão incluídos desde 2026-09-01 para 2016-2024 — 2025 ainda não tem fonte (ver "O que falta"). O que resta de diferença contra a série antiga vem da decisão 6 (receita líquida em estados e municípios, deliberada, reduz o total frente à metodologia antiga) e de resíduos pequenos já documentados em `docs/divergencias.md`. `docs/revisao-metodologica.md` (`uv run ctb comparar-historico`) tem a comparação ano a ano, linha a linha, com os valores exatos.

## AD ESFERA

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Impostos | 620,816 | 8,158 | 24,331 | 2.931,75 |
| Contribuições Sociais | 585,042 | 7,688 | 22,929 | 2.762,81 |
| Previdência Social | 364,205 | 4,786 | 14,274 | 1.719,93 |
| Demais | 79,056 | 1,039 | 3,098 | 373,33 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 523,005 | 6,873 | 20,498 | 2.469,85 |
| IPVA | 49,398 | 0,649 | 1,936 | 233,28 |
| Demais | 127,594 | 1,677 | 5,001 | 602,55 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 72,831 | 0,957 | 2,854 | 343,94 |
| IPTU | 50,520 | 0,664 | 1,980 | 238,58 |
| Demais | 79,028 | 1,039 | 3,097 | 373,20 |


## byGOVDetalhado

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| IR | 492,142 | 6,467 | 19,288 | 2.324,10 |
| Previdência Social | 364,205 | 4,786 | 14,274 | 1.719,93 |
| Cofins | 228,324 | 3,000 | 8,949 | 1.078,24 |
| FGTS | 127,274 | 1,673 | 4,988 | 601,04 |
| CSLL | 99,872 | 1,312 | 3,914 | 471,64 |
| PIS-PASEP | 66,949 | 0,880 | 2,624 | 316,16 |
| IPI | 59,551 | 0,783 | 2,334 | 281,22 |
| Royalties e Compensações Financeiras | 56,327 | 0,740 | 2,208 | 266,00 |
| Imp. sobre Comércio Exterior | 46,070 | 0,605 | 1,806 | 217,56 |
| Contrib. Seg. Serv. Público | 24,502 | 0,322 | 0,960 | 115,71 |
| IOF | 21,199 | 0,279 | 0,831 | 100,11 |
| Salário Educação | 17,712 | 0,233 | 0,694 | 83,64 |
| Contribuições Econômicas | 16,631 | 0,219 | 0,652 | 78,54 |
| Sistema S | 15,935 | 0,209 | 0,625 | 75,25 |
| Taxas | 6,098 | 0,080 | 0,239 | 28,80 |
| Outras contribuições sociais | 4,467 | 0,059 | 0,175 | 21,09 |
| ITR | 1,830 | 0,024 | 0,072 | 8,64 |
| Outros impostos | 0,023 | 0,000 | 0,001 | 0,11 |
| CPMF | 0,006 | 0,000 | 0,000 | 0,03 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 523,005 | 6,873 | 20,498 | 2.469,85 |
| IPVA | 49,398 | 0,649 | 1,936 | 233,28 |
| IRRF | 49,134 | 0,646 | 1,926 | 232,03 |
| Previ. Estadual | 38,996 | 0,512 | 1,528 | 184,16 |
| TAXAS | 25,778 | 0,339 | 1,010 | 121,73 |
| ITCD | 8,947 | 0,118 | 0,351 | 42,25 |
| Contribuições de Melhoria e Econômicas | 4,428 | 0,058 | 0,174 | 20,91 |
| Royalties e Compensações Financeiras | 0,308 | 0,004 | 0,012 | 1,45 |
| Outros impostos | 0,003 | 0,000 | 0,000 | 0,02 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 72,831 | 0,957 | 2,854 | 343,94 |
| IPTU | 50,520 | 0,664 | 1,980 | 238,58 |
| IRRF | 23,131 | 0,304 | 0,907 | 109,23 |
| Previd. Municipal | 17,289 | 0,227 | 0,678 | 81,65 |
| ITBI | 14,687 | 0,193 | 0,576 | 69,36 |
| TAXAS | 11,576 | 0,152 | 0,454 | 54,67 |
| Contribuições de Melhoria e Econômicas | 10,986 | 0,144 | 0,431 | 51,88 |
| Outros impostos | 0,769 | 0,010 | 0,030 | 3,63 |
| Royalties e Compensações Financeiras | 0,590 | 0,008 | 0,023 | 2,79 |


## PRINCIPAIS TRIBUTOS

| tributo | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Imposto de Renda (Global) | 564,407 | 7,417 | 22,121 | 2.665,37 |
| ICMS | 523,005 | 6,873 | 20,498 | 2.469,85 |
| Previdência Social Ampliada | 420,490 | 5,526 | 16,480 | 1.985,73 |
| Cofins | 228,324 | 3,000 | 8,949 | 1.078,24 |
| CSLL | 99,872 | 1,312 | 3,914 | 471,64 |
| ISS | 72,831 | 0,957 | 2,854 | 343,94 |
| PIS-PASEP | 66,949 | 0,880 | 2,624 | 316,16 |
| IPI | 59,551 | 0,783 | 2,334 | 281,22 |
| IPTU | 50,520 | 0,664 | 1,980 | 238,58 |
| IPVA | 49,398 | 0,649 | 1,936 | 233,28 |
| Comércio Exterior (Importação + Exportação) | 46,070 | 0,605 | 1,806 | 217,56 |
| IOF | 21,199 | 0,279 | 0,831 | 100,11 |
| ITBI | 14,687 | 0,193 | 0,576 | 69,36 |
| ITCD | 8,947 | 0,118 | 0,351 | 42,25 |
| ITR | 1,830 | 0,024 | 0,072 | 8,64 |
| CPMF | 0,006 | 0,000 | 0,000 | 0,03 |
| Demais tributos | 323,406 | 4,250 | 12,675 | 1.527,26 |


## Bases de Incidência

| base de incidência | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| bens_servicos | 977,923 | 12,851 | 38,327 | 4.618,17 |
| renda | 664,279 | 8,729 | 26,035 | 3.137,01 |
| salarios | 607,782 | 7,987 | 23,821 | 2.870,20 |
| patrimonio | 182,845 | 2,403 | 7,166 | 863,47 |
| comercio_exterior | 46,070 | 0,605 | 1,806 | 217,56 |
| taxas | 43,451 | 0,571 | 1,703 | 205,19 |
| transacoes_financeiras | 21,206 | 0,279 | 0,831 | 100,14 |
| demais | 7,938 | 0,104 | 0,311 | 37,48 |


## RD ESFERA

Ajusta AD ESFERA pelas transferências constitucionais entre entes — o total geral não muda (é redistribuição, não dinheiro novo).

| esfera | AD (R$ bi) | RD (R$ bi) | RD % PIB | RD % total |
|---|---|---|---|---|
| União | 1.649,118 | 1.301,511 | 17,104 | 51,01% |
| Estados | 699,997 | 677,036 | 8,897 | 26,53% |
| Municípios | 202,379 | 572,948 | 7,529 | 22,46% |

### União para Estados

| modalidade | R$ bi |
|---|---|
| FPE | 74,422 |
| LC173/2020 (PFEC) | 37,000 |
| FUNDEB | 18,953 |
| Royalties e Compensações Financeiras | 17,431 |
| Salário-Educação (quota estadual) | 11,808 |
| AFM/AFE | 7,359 |
| IPI-Exp (FPEx) | 4,378 |
| LC176/2020 (Seguro-Receita ICMS) | 2,489 |
| CIDE | 0,520 |
| IOF-Ouro | 0,019 |
| FEX | 0,000 |
| LC87/1996 (Lei Kandir) | 0,000 |
| **Total** | **174,378** |

### União para Municípios

| modalidade | R$ bi |
|---|---|
| FPM | 86,655 |
| FUNDEB | 35,415 |
| LC173/2020 (PFEC) | 23,149 |
| Royalties e Compensações Financeiras | 18,169 |
| AFM/AFE | 7,739 |
| ITR | 1,259 |
| LC176/2020 (Seguro-Receita ICMS) | 0,630 |
| CIDE | 0,170 |
| IOF-Ouro | 0,043 |
| FEX | 0,000 |
| LC87/1996 (Lei Kandir) | 0,000 |
| **Total** | **173,229** |

### Estados para Municípios

| modalidade | R$ bi |
|---|---|
| ICMS (cota-parte municipal, líq. FUNDEB) | 104,601 |
| FUNDEB | 66,945 |
| IPVA (cota-parte municipal) | 24,699 |
| IPI-Exp (FPEx) (cota-parte municipal) | 1,094 |
| **Total** | **197,339** |

**Sobre a linha ICMS (cota-parte municipal, líq. FUNDEB):** 25% da arrecadação estadual de ICMS, com a retenção de 20% do FUNDEB (art. 212-A CF) aplicada antes do repasse — 25% × 80% = 20% da arrecadação bruta (decisão do usuário em 2026-08-31, `docs/decisoes-pendentes.md` §9 — em 2024 isso reproduz quase exato o valor publicado, R$ 161,631 bi calculado contra R$ 161,083 bi). A cota do IPVA não tem essa retenção (50% flat).

## Cobertura da imputação municipal

- Municípios no universo: 5.569
- Declarantes: 5.559 (99,90% da população coberta)
- Imputados: 10 (0,050% da receita municipal)
- Faixas com menos de 30 declarantes, mescladas com a faixa vizinha para o cálculo da média: 17←[18]

## O que falta
