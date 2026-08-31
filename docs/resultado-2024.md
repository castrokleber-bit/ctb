# Resultado calculado — 2024

Gerado por `uv run ctb calcular --anos 2024` em 2026-08-31. PIB corrente (2026-08-31, SIDRA tabela 1846): R$ 11.779,251 bi. População (SIDRA tabela 6579): 212.583.750.

Este é o produto da Fase 2 — a primeira vez que o pipeline produz um número, não só valida uma estrutura. A reconciliação rubrica a rubrica por esfera já foi feita na Fase 1 (`uv run ctb dicionario validar`); aqui confere-se o agregado.

## Total geral

**R$ 3.981,516 bi — 33,801% do PIB**

| esfera | R$ bi | % do total |
|---|---|---|
| União | 2.515,506 | 63,18% |
| Estados | 1.106,954 | 27,80% |
| Municípios | 359,056 | 9,02% |

### Por que não fecha em ~36% do PIB direto

O total acima fecha em 33,80% do PIB, abaixo dos 35,950% da série publicada de 2024. A diferença tem duas causas conhecidas, nenhuma delas erro de cálculo:

1. **FGTS e Sistema S não estão nesta passada** (R$ 221,3 bi em 2024, 1,88 p.p. do PIB) — são fontes manuais (`manual/`, CLAUDE.md §Fontes) e nenhum CSV foi coletado ainda. Somando esse gap de volta: 35,680%, muito perto dos 35,950% publicados.
2. **Decisão 6** (2026-08-31) uniformizou estados e municípios em receita líquida — reduz o total em cerca de R$ 29 bi contra a metodologia antiga (bruta). É mudança deliberada, não resíduo.

O restante é resíduo pequeno e já documentado — ver `docs/divergencias.md` e `docs/decisoes-pendentes.md` (Contribuições Econômicas da União, IPTU e IRRF municipais).

## byGOVDetalhado

### União

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| IR | 785,151 | 6,666 | 19,720 | 3.693,37 |
| Previdência Social | 636,975 | 5,408 | 15,998 | 2.996,35 |
| Cofins | 367,242 | 3,118 | 9,224 | 1.727,52 |
| CSLL | 166,760 | 1,416 | 4,188 | 784,44 |
| Royalties e Compensações Financeiras | 109,985 | 0,934 | 2,762 | 517,37 |
| PIS-PASEP | 103,824 | 0,881 | 2,608 | 488,39 |
| IPI | 84,373 | 0,716 | 2,119 | 396,89 |
| Imp. sobre Comércio Exterior | 77,762 | 0,660 | 1,953 | 365,80 |
| IOF | 67,748 | 0,575 | 1,702 | 318,69 |
| Contribuições Econômicas | 34,403 | 0,292 | 0,864 | 161,83 |
| Salário Educação | 33,078 | 0,281 | 0,831 | 155,60 |
| Contrib. Seg. Serv. Público | 28,422 | 0,241 | 0,714 | 133,70 |
| Taxas | 9,511 | 0,081 | 0,239 | 44,74 |
| Outras contribuições sociais | 6,794 | 0,058 | 0,171 | 31,96 |
| ITR | 3,493 | 0,030 | 0,088 | 16,43 |
| Outros impostos | 0,001 | 0,000 | 0,000 | 0,01 |
| CPMF | -0,017 | -0,000 | -0,000 | -0,08 |


### Estados

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ICMS | 808,157 | 6,861 | 20,298 | 3.801,59 |
| IPVA | 87,053 | 0,739 | 2,186 | 409,50 |
| IRRF | 81,068 | 0,688 | 2,036 | 381,35 |
| Previ. Estadual | 55,255 | 0,469 | 1,388 | 259,92 |
| TAXAS | 46,690 | 0,396 | 1,173 | 219,63 |
| ITCD | 18,425 | 0,156 | 0,463 | 86,67 |
| Contribuições de Melhoria e Econômicas | 7,449 | 0,063 | 0,187 | 35,04 |
| Royalties e Compensações Financeiras | 2,810 | 0,024 | 0,071 | 13,22 |
| Outros impostos | 0,047 | 0,000 | 0,001 | 0,22 |


### Municípios

| rubrica | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| ISS | 142,091 | 1,206 | 3,569 | 668,40 |
| IPTU | 74,042 | 0,629 | 1,860 | 348,29 |
| IRRF | 49,765 | 0,422 | 1,250 | 234,10 |
| Previd. Municipal | 29,330 | 0,249 | 0,737 | 137,97 |
| ITBI | 25,083 | 0,213 | 0,630 | 117,99 |
| TAXAS | 19,386 | 0,165 | 0,487 | 91,19 |
| Contribuições de Melhoria e Econômicas | 16,810 | 0,143 | 0,422 | 79,07 |
| Royalties e Compensações Financeiras | 2,037 | 0,017 | 0,051 | 9,58 |
| Outros impostos | 0,511 | 0,004 | 0,013 | 2,41 |


## Bases de Incidência

| base de incidência | R$ bi | % PIB | % total | per capita (R$) |
|---|---|---|---|---|
| bens_servicos | 1.556,434 | 13,213 | 39,091 | 7.321,51 |
| renda | 1.082,744 | 9,192 | 27,194 | 5.093,26 |
| salarios | 785,455 | 6,668 | 19,728 | 3.694,80 |
| patrimonio | 323,019 | 2,742 | 8,113 | 1.519,49 |
| comercio_exterior | 77,762 | 0,660 | 1,953 | 365,80 |
| taxas | 75,588 | 0,642 | 1,898 | 355,57 |
| transacoes_financeiras | 67,731 | 0,575 | 1,701 | 318,61 |
| demais | 12,782 | 0,109 | 0,321 | 60,13 |


## Cobertura da imputação municipal

- Municípios no universo: 5.569
- Declarantes: 5.544 (99,82% da população coberta)
- Imputados: 25 (0,095% da receita municipal)
- Faixas com menos de 30 declarantes, mescladas com a faixa vizinha para o cálculo da média: 16←[15], 17←[18]

## O que falta nesta passada

- **AD ESFERA** e **PRINCIPAIS TRIBUTOS** — precisam de investigação nova na planilha de referência (categoria econômica e agregação cruzando esferas, respectivamente) que não foi feita ainda.
- **RD ESFERA** — depende de transferências constitucionais; o bloco Estados→Municípios segue sem fonte (decisão 5).
- **FGTS e Sistema S** — fontes manuais, nenhum CSV coletado ainda.
