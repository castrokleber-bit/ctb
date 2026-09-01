# Resultado calculado — 2022

Gerado por `uv run ctb calcular --anos 2022` em 2026-09-01. PIB corrente (2026-09-01, SIDRA tabela 1846): R$ 10.079,676 bi. População (SIDRA tabela 6579): 203.080.756.

Este é o produto da Fase 2 — a primeira vez que o pipeline produz um número, não só valida uma estrutura. A reconciliação rubrica a rubrica por esfera já foi feita na Fase 1 (`uv run ctb dicionario validar`); aqui confere-se o agregado.

## Total geral

**R$ 3.688,283 bi — 36,591% do PIB**

| esfera | R$ bi | % do total |
|---|---|---|
| União | 2.471,036 | 67,00% |
| Estados | 935,245 | 25,36% |
| Municípios | 282,002 | 7,65% |

### Por que não fecha exatamente o valor publicado

FGTS e Sistema S (`manual/`, CLAUDE.md §Fontes) estão incluídos desde 2026-09-01 para 2016-2024 — 2025 ainda não tem fonte (ver "O que falta"). O que resta de diferença contra a série antiga vem da decisão 6 (receita líquida em estados e municípios, deliberada, reduz o total frente à metodologia antiga) e de resíduos pequenos já documentados em `docs/divergencias.md`. `docs/revisao-metodologica.md` (`uv run ctb comparar-historico`) tem a comparação ano a ano, linha a linha, com os valores exatos.

## AD ESFERA

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Impostos | 942,516 | 9,351 | 25,554 | 4.641,09 |
| Contribuições Sociais | 850,239 | 8,435 | 23,052 | 4.186,70 |
| Previdência Social | 483,851 | 4,800 | 13,119 | 2.382,56 |
| Demais | 194,429 | 1,929 | 5,272 | 957,40 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 694,155 | 6,887 | 18,821 | 3.418,12 |
| IPVA | 65,934 | 0,654 | 1,788 | 324,67 |
| Demais | 175,156 | 1,738 | 4,749 | 862,49 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 107,647 | 1,068 | 2,919 | 530,07 |
| IPTU | 65,122 | 0,646 | 1,766 | 320,67 |
| Demais | 109,234 | 1,084 | 2,962 | 537,88 |


## byGOVDetalhado

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| IR | 752,449 | 7,465 | 20,401 | 3.705,17 |
| Previdência Social | 483,851 | 4,800 | 13,119 | 2.382,56 |
| Cofins | 348,105 | 3,454 | 9,438 | 1.714,12 |
| CSLL | 170,891 | 1,695 | 4,633 | 841,49 |
| Royalties e Compensações Financeiras | 164,528 | 1,632 | 4,461 | 810,16 |
| FGTS | 156,298 | 1,551 | 4,238 | 769,63 |
| PIS-PASEP | 93,821 | 0,931 | 2,544 | 461,99 |
| IPI | 69,704 | 0,692 | 1,890 | 343,23 |
| Imp. sobre Comércio Exterior | 59,183 | 0,587 | 1,605 | 291,43 |
| IOF | 58,399 | 0,579 | 1,583 | 287,56 |
| Contrib. Seg. Serv. Público | 26,549 | 0,263 | 0,720 | 130,73 |
| Sistema S | 23,815 | 0,236 | 0,646 | 117,27 |
| Salário Educação | 22,374 | 0,222 | 0,607 | 110,17 |
| Contribuições Econômicas | 21,901 | 0,217 | 0,594 | 107,85 |
| Outras contribuições sociais | 8,367 | 0,083 | 0,227 | 41,20 |
| Taxas | 8,000 | 0,079 | 0,217 | 39,39 |
| ITR | 2,771 | 0,027 | 0,075 | 13,64 |
| CPMF | 0,018 | 0,000 | 0,000 | 0,09 |
| Outros impostos | 0,011 | 0,000 | 0,000 | 0,05 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 694,155 | 6,887 | 18,821 | 3.418,12 |
| IPVA | 65,934 | 0,654 | 1,788 | 324,67 |
| IRRF | 63,028 | 0,625 | 1,709 | 310,36 |
| Previ. Estadual | 51,194 | 0,508 | 1,388 | 252,09 |
| TAXAS | 38,595 | 0,383 | 1,046 | 190,05 |
| ITCD | 13,525 | 0,134 | 0,367 | 66,60 |
| Contribuições de Melhoria e Econômicas | 6,236 | 0,062 | 0,169 | 30,71 |
| Royalties e Compensações Financeiras | 2,549 | 0,025 | 0,069 | 12,55 |
| Outros impostos | 0,028 | 0,000 | 0,001 | 0,14 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 107,647 | 1,068 | 2,919 | 530,07 |
| IPTU | 65,122 | 0,646 | 1,766 | 320,67 |
| IRRF | 32,932 | 0,327 | 0,893 | 162,16 |
| Previd. Municipal | 23,641 | 0,235 | 0,641 | 116,41 |
| ITBI | 19,986 | 0,198 | 0,542 | 98,41 |
| TAXAS | 15,751 | 0,156 | 0,427 | 77,56 |
| Contribuições de Melhoria e Econômicas | 13,913 | 0,138 | 0,377 | 68,51 |
| Royalties e Compensações Financeiras | 1,790 | 0,018 | 0,049 | 8,82 |
| Outros impostos | 1,221 | 0,012 | 0,033 | 6,01 |


## PRINCIPAIS TRIBUTOS

| tributo | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Imposto de Renda (Global) | 848,409 | 8,417 | 23,003 | 4.177,69 |
| ICMS | 694,155 | 6,887 | 18,821 | 3.418,12 |
| Previdência Social Ampliada | 558,687 | 5,543 | 15,148 | 2.751,06 |
| Cofins | 348,105 | 3,454 | 9,438 | 1.714,12 |
| CSLL | 170,891 | 1,695 | 4,633 | 841,49 |
| ISS | 107,647 | 1,068 | 2,919 | 530,07 |
| PIS-PASEP | 93,821 | 0,931 | 2,544 | 461,99 |
| IPI | 69,704 | 0,692 | 1,890 | 343,23 |
| IPVA | 65,934 | 0,654 | 1,788 | 324,67 |
| IPTU | 65,122 | 0,646 | 1,766 | 320,67 |
| Comércio Exterior (Importação + Exportação) | 59,183 | 0,587 | 1,605 | 291,43 |
| IOF | 58,399 | 0,579 | 1,583 | 287,56 |
| ITBI | 19,986 | 0,198 | 0,542 | 98,41 |
| ITCD | 13,525 | 0,134 | 0,367 | 66,60 |
| ITR | 2,771 | 0,027 | 0,075 | 13,64 |
| CPMF | 0,018 | 0,000 | 0,000 | 0,09 |
| Demais tributos | 511,927 | 5,079 | 13,880 | 2.520,80 |


## Bases de Incidência

| base de incidência | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| bens_servicos | 1.348,852 | 13,382 | 36,571 | 6.641,95 |
| renda | 1.019,300 | 10,112 | 27,636 | 5.019,19 |
| salarios | 792,204 | 7,859 | 21,479 | 3.900,93 |
| patrimonio | 336,710 | 3,340 | 9,129 | 1.658,01 |
| taxas | 62,346 | 0,619 | 1,690 | 307,00 |
| comercio_exterior | 59,183 | 0,587 | 1,605 | 291,43 |
| transacoes_financeiras | 58,417 | 0,580 | 1,584 | 287,65 |
| demais | 11,270 | 0,112 | 0,306 | 55,49 |


## RD ESFERA

Ajusta AD ESFERA pelas transferências constitucionais entre entes — o total geral não muda (é redistribuição, não dinheiro novo).

| esfera | AD (R$ bi) | RD (R$ bi) | RD % PIB | RD % total |
|---|---|---|---|---|
| União | 2.471,036 | 1.988,343 | 19,726 | 53,91% |
| Estados | 935,245 | 901,006 | 8,939 | 24,43% |
| Municípios | 282,002 | 798,934 | 7,926 | 21,66% |

### União para Estados

| modalidade | R$ bi |
|---|---|
| FPE | 125,341 |
| Royalties e Compensações Financeiras | 41,062 |
| FUNDEB | 31,373 |
| Salário-Educação (quota estadual) | 14,916 |
| Cessão Onerosa | 5,005 |
| IPI-Exp (FPEx) | 4,903 |
| LC176/2020 (Seguro-Receita ICMS) | 3,000 |
| AFM/AFE | 2,894 |
| CIDE | 0,520 |
| IOF-Ouro | 0,022 |
| FEX | 0,000 |
| LC87/1996 (Lei Kandir) | 0,000 |
| **Total** | **229,038** |

### União para Municípios

| modalidade | R$ bi |
|---|---|
| FPM | 146,330 |
| FUNDEB | 65,090 |
| Royalties e Compensações Financeiras | 36,447 |
| Cessão Onerosa | 2,659 |
| ITR | 1,919 |
| LC176/2020 (Seguro-Receita ICMS) | 0,988 |
| CIDE | 0,170 |
| IOF-Ouro | 0,052 |
| FEX | 0,000 |
| LC87/1996 (Lei Kandir) | 0,000 |
| **Total** | **253,655** |

### Estados para Municípios

| modalidade | R$ bi |
|---|---|
| ICMS (cota-parte municipal, líq. FUNDEB) | 138,831 |
| FUNDEB | 90,253 |
| IPVA (cota-parte municipal) | 32,967 |
| IPI-Exp (FPEx) (cota-parte municipal) | 1,226 |
| **Total** | **263,277** |

**Sobre a linha ICMS (cota-parte municipal, líq. FUNDEB):** 25% da arrecadação estadual de ICMS, com a retenção de 20% do FUNDEB (art. 212-A CF) aplicada antes do repasse — 25% × 80% = 20% da arrecadação bruta (decisão do usuário em 2026-08-31, `docs/decisoes-pendentes.md` §9 — em 2024 isso reproduz quase exato o valor publicado, R$ 161,631 bi calculado contra R$ 161,083 bi). A cota do IPVA não tem essa retenção (50% flat).

## Cobertura da imputação municipal

- Municípios no universo: 5.569
- Declarantes: 5.556 (99,95% da população coberta)
- Imputados: 13 (0,021% da receita municipal)
- Faixas com menos de 30 declarantes, mescladas com a faixa vizinha para o cálculo da média: 16←[15], 17←[18]

## O que falta
