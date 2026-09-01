# Resultado calculado — 2017

Gerado por `uv run ctb calcular --anos 2017` em 2026-09-01. PIB corrente (2026-09-01, SIDRA tabela 1846): R$ 6.585,479 bi. População (SIDRA tabela 6579): 207.660.929.

Este é o produto da Fase 2 — a primeira vez que o pipeline produz um número, não só valida uma estrutura. A reconciliação rubrica a rubrica por esfera já foi feita na Fase 1 (`uv run ctb dicionario validar`); aqui confere-se o agregado.

## Total geral

**R$ 2.151,019 bi — 32,663% do PIB**

| esfera | R$ bi | % do total |
|---|---|---|
| União | 1.423,767 | 66,19% |
| Estados | 579,417 | 26,94% |
| Municípios | 147,834 | 6,87% |

### Por que não fecha exatamente o valor publicado

FGTS e Sistema S (`manual/`, CLAUDE.md §Fontes) estão incluídos desde 2026-09-01 para 2016-2024 — 2025 ainda não tem fonte (ver "O que falta"). O que resta de diferença contra a série antiga vem da decisão 6 (receita líquida em estados e municípios, deliberada, reduz o total frente à metodologia antiga) e de resíduos pequenos já documentados em `docs/divergencias.md`. `docs/revisao-metodologica.md` (`uv run ctb comparar-historico`) tem a comparação ano a ano, linha a linha, com os valores exatos.

## AD ESFERA

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Impostos | 456,392 | 6,930 | 21,217 | 2.197,78 |
| Contribuições Sociais | 523,735 | 7,953 | 24,348 | 2.522,07 |
| Previdência Social | 359,790 | 5,463 | 16,726 | 1.732,58 |
| Demais | 83,851 | 1,273 | 3,898 | 403,79 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 436,864 | 6,634 | 20,310 | 2.103,74 |
| IPVA | 39,121 | 0,594 | 1,819 | 188,39 |
| Demais | 103,432 | 1,571 | 4,808 | 498,08 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 56,325 | 0,855 | 2,619 | 271,23 |
| IPTU | 34,805 | 0,529 | 1,618 | 167,61 |
| Demais | 56,705 | 0,861 | 2,636 | 273,06 |


## byGOVDetalhado

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| Previdência Social | 359,790 | 5,463 | 16,726 | 1.732,58 |
| IR | 340,018 | 5,163 | 15,807 | 1.637,37 |
| Cofins | 210,496 | 3,196 | 9,786 | 1.013,65 |
| FGTS | 123,535 | 1,876 | 5,743 | 594,89 |
| CSLL | 68,345 | 1,038 | 3,177 | 329,12 |
| Royalties e Compensações Financeiras | 58,542 | 0,889 | 2,722 | 281,91 |
| PIS-PASEP | 56,116 | 0,852 | 2,609 | 270,23 |
| IPI | 48,032 | 0,729 | 2,233 | 231,30 |
| IOF | 34,591 | 0,525 | 1,608 | 166,57 |
| Imp. sobre Comércio Exterior | 32,412 | 0,492 | 1,507 | 156,08 |
| Salário Educação | 20,112 | 0,305 | 0,935 | 96,85 |
| Contribuições Econômicas | 17,201 | 0,261 | 0,800 | 82,83 |
| Contrib. Seg. Serv. Público | 17,115 | 0,260 | 0,796 | 82,42 |
| Sistema S | 16,471 | 0,250 | 0,766 | 79,32 |
| Outras contribuições sociais | 11,486 | 0,174 | 0,534 | 55,31 |
| Taxas | 8,108 | 0,123 | 0,377 | 39,04 |
| ITR | 1,337 | 0,020 | 0,062 | 6,44 |
| CPMF | 0,059 | 0,001 | 0,003 | 0,28 |
| Outros impostos | 0,002 | 0,000 | 0,000 | 0,01 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 436,864 | 6,634 | 20,310 | 2.103,74 |
| IPVA | 39,121 | 0,594 | 1,819 | 188,39 |
| Previ. Estadual | 32,796 | 0,498 | 1,525 | 157,93 |
| IRRF | 32,029 | 0,486 | 1,489 | 154,24 |
| TAXAS | 22,602 | 0,343 | 1,051 | 108,84 |
| Royalties e Compensações Financeiras | 7,163 | 0,109 | 0,333 | 34,49 |
| ITCD | 7,085 | 0,108 | 0,329 | 34,12 |
| Contribuições de Melhoria e Econômicas | 1,758 | 0,027 | 0,082 | 8,46 |
| Outros impostos | 0,000 | 0,000 | 0,000 | 0,00 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 56,325 | 0,855 | 2,619 | 271,23 |
| IPTU | 34,805 | 0,529 | 1,618 | 167,61 |
| IRRF | 16,314 | 0,248 | 0,758 | 78,56 |
| Previd. Municipal | 13,031 | 0,198 | 0,606 | 62,75 |
| ITBI | 10,276 | 0,156 | 0,478 | 49,48 |
| TAXAS | 8,609 | 0,131 | 0,400 | 41,46 |
| Contribuições de Melhoria e Econômicas | 7,964 | 0,121 | 0,370 | 38,35 |
| Royalties e Compensações Financeiras | 0,370 | 0,006 | 0,017 | 1,78 |
| Outros impostos | 0,142 | 0,002 | 0,007 | 0,68 |


## PRINCIPAIS TRIBUTOS

| tributo | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 436,864 | 6,634 | 20,310 | 2.103,74 |
| Previdência Social Ampliada | 405,616 | 6,159 | 18,857 | 1.953,26 |
| Imposto de Renda (Global) | 388,361 | 5,897 | 18,055 | 1.870,17 |
| Cofins | 210,496 | 3,196 | 9,786 | 1.013,65 |
| CSLL | 68,345 | 1,038 | 3,177 | 329,12 |
| ISS | 56,325 | 0,855 | 2,619 | 271,23 |
| PIS-PASEP | 56,116 | 0,852 | 2,609 | 270,23 |
| IPI | 48,032 | 0,729 | 2,233 | 231,30 |
| IPVA | 39,121 | 0,594 | 1,819 | 188,39 |
| IPTU | 34,805 | 0,529 | 1,618 | 167,61 |
| IOF | 34,591 | 0,525 | 1,608 | 166,57 |
| Comércio Exterior (Importação + Exportação) | 32,412 | 0,492 | 1,507 | 156,08 |
| ITBI | 10,276 | 0,156 | 0,478 | 49,48 |
| ITCD | 7,085 | 0,108 | 0,329 | 34,12 |
| ITR | 1,337 | 0,020 | 0,062 | 6,44 |
| CPMF | 0,059 | 0,001 | 0,003 | 0,28 |
| Demais tributos | 321,179 | 4,877 | 14,931 | 1.546,65 |


## Bases de Incidência

| base de incidência | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| bens_servicos | 831,071 | 12,620 | 38,636 | 4.002,06 |
| salarios | 590,818 | 8,972 | 27,467 | 2.845,11 |
| renda | 456,706 | 6,935 | 21,232 | 2.199,29 |
| patrimonio | 158,840 | 2,412 | 7,384 | 764,90 |
| taxas | 39,319 | 0,597 | 1,828 | 189,34 |
| transacoes_financeiras | 34,649 | 0,526 | 1,611 | 166,86 |
| comercio_exterior | 32,412 | 0,492 | 1,507 | 156,08 |
| demais | 7,204 | 0,109 | 0,335 | 34,69 |


## RD ESFERA

Ajusta AD ESFERA pelas transferências constitucionais entre entes — o total geral não muda (é redistribuição, não dinheiro novo).

| esfera | AD (R$ bi) | RD (R$ bi) | RD % PIB | RD % total |
|---|---|---|---|---|
| União | 1.423,767 | 1.185,214 | 17,997 | 55,10% |
| Estados | 579,417 | 536,838 | 8,152 | 24,96% |
| Municípios | 147,834 | 428,967 | 6,514 | 19,94% |

### União para Estados

| modalidade | R$ bi |
|---|---|
| FPE | 66,658 |
| FUNDEB | 18,417 |
| Salário-Educação (quota estadual) | 13,408 |
| Royalties e Compensações Financeiras | 12,155 |
| IPI-Exp (FPEx) | 3,781 |
| FEX | 1,433 |
| CIDE | 1,280 |
| LC87/1996 (Lei Kandir) | 1,173 |
| IOF-Ouro | 0,005 |
| LC176/2020 (Seguro-Receita ICMS) | 0,000 |
| **Total** | **118,311** |

### União para Municípios

| modalidade | R$ bi |
|---|---|
| FPM | 77,635 |
| FUNDEB | 30,339 |
| Royalties e Compensações Financeiras | 9,989 |
| ITR | 0,984 |
| FEX | 0,478 |
| CIDE | 0,419 |
| LC87/1996 (Lei Kandir) | 0,387 |
| IOF-Ouro | 0,012 |
| LC176/2020 (Seguro-Receita ICMS) | 0,000 |
| **Total** | **120,242** |

### Estados para Municípios

| modalidade | R$ bi |
|---|---|
| ICMS (cota-parte municipal, líq. FUNDEB) | 87,373 |
| FUNDEB | 53,011 |
| IPVA (cota-parte municipal) | 19,561 |
| IPI-Exp (FPEx) (cota-parte municipal) | 0,945 |
| **Total** | **160,890** |

**Sobre a linha ICMS (cota-parte municipal, líq. FUNDEB):** 25% da arrecadação estadual de ICMS, com a retenção de 20% do FUNDEB (art. 212-A CF) aplicada antes do repasse — 25% × 80% = 20% da arrecadação bruta (decisão do usuário em 2026-08-31, `docs/decisoes-pendentes.md` §9 — em 2024 isso reproduz quase exato o valor publicado, R$ 161,631 bi calculado contra R$ 161,083 bi). A cota do IPVA não tem essa retenção (50% flat).

## Cobertura da imputação municipal

- Municípios no universo: 5.569
- Declarantes: 5.556 (99,93% da população coberta)
- Imputados: 13 (0,025% da receita municipal)
- Faixas com menos de 30 declarantes, mescladas com a faixa vizinha para o cálculo da média: 16←[15], 17←[18]

## O que falta
