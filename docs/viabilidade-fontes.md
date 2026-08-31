# Viabilidade das fontes — Fase 0

Gerado por `uv run ctb fontes testar` em 2026-08-31. Série testada: 2016–2025.

Este documento responde se cada fonte da seção 4 do `PROJETO-CTB.md` existe, o que ela entrega e a que custo. Ele **não** valida números de carga tributária — isso é Fase 2. Reproduza-o a qualquer momento com o comando acima; ele lê do cache em `dados/bruto/` e só vai à rede para o que ainda não baixou.

## Resumo

|  | bloco | pergunta |
|---|---|---|
| ✅ | Cadastro de entes | `/tt/entes` responde e identifica a União? |
| ⚠️ | União (Siconfi DCA) | `id_ente` da União traz o Anexo I-C de 2016 a 2025? |
| ❌ | União (Siconfi DCA) | A DCA expõe a natureza de receita em 8 dígitos? |
| ✅ | Reconciliação União 2024 | A DCA reproduz os totais por rubrica do Balanço Geral da União? |
| ❌ | Reconciliação União 2024 | Dá para separar principal de acessório usando só a DCA? |
| ✅ | Reconciliação União 2024 | A Regra 2 (só o principal) vale para todas as rubricas? |
| ✅ | Estados e DF (Siconfi DCA) | Os 26 estados e o DF entregaram o Anexo I-C em todos os anos? |
| ✅ | Cobertura municipal (Siconfi DCA) | Quantos municípios entregaram a DCA em cada ano? |
| ✅ | Cobertura municipal (Siconfi DCA) | Algum município acima de 500.000 habitantes faltou? |
| ⚠️ | Transferências constitucionais | O endpoint `apiapex.tesouro.gov.br/aria/v1/` do PROJETO-CTB funciona? |
| ✅ | IBGE / SIDRA | PIB corrente e população estão disponíveis para toda a série? |
| ⚠️ | Fontes sem API | O que precisa entrar por `manual/`? |


## Correções à especificação

Três afirmações do `CLAUDE.md` e do `PROJETO-CTB.md` não se confirmaram no teste. **Os dois documentos já foram corrigidos em 2026-08-30**; a tabela abaixo fica como registro, porque a versão errada circulou e pode estar em cópias antigas.

| documento | afirmava | na verdade |
|---|---|---|
| `CLAUDE.md` §Fontes<br>`PROJETO-CTB.md` §4 | União: `id_ente=U` (código não numérico) | `id_ente=1`. O código `U` devolve **400**; `U` é o valor da coluna `esfera`, não do `id_ente` |
| `PROJETO-CTB.md` §4 | transferências em `apiapex.tesouro.gov.br/aria/v1/` | todas as rotas testadas devolvem **404**. O caminho viável é o CKAN do Tesouro Transparente, em CSV mensal |
| `CLAUDE.md` §Regras de classificação | Taxas fica R$ 0,083 bi abaixo — divergência não resolvida | **resolvida**: *Taxas* é a única rubrica publicada com principal + acessórios. Ver `docs/divergencias.md` §1 |


## Cadastro de entes

### ✅ `/tt/entes` responde e identifica a União?

O cadastro traz 5598 entes. A União aparece com `cod_ibge=1` e nome 'União' — **não** com o código `U` suposto no PROJETO-CTB. O Distrito Federal tem esfera própria `D`, o que confirma que a regra do DF precisa ser explícita no dicionário.

| esfera | entes |
|---|---|
| D | 1 |
| E | 26 |
| M | 5570 |
| U | 1 |


## União (Siconfi DCA)

### ⚠️ `id_ente` da União traz o Anexo I-C de 2016 a 2025?

Todos os dez anos respondem. Há **quebra de layout**: até 2018 a conta-raiz é `TotalReceitas` e o demonstrativo tem ~345 linhas; de 2019 em diante é `ReceitasExcetoIntraOrcamentarias`, com o dobro de linhas. O pipeline precisa reconhecer as duas raízes; usar só uma delas silenciaria 2016–2018.

| ano | linhas | conta-raiz | receita bruta (R$ bi) |
|---|---|---|---|
| 2016 | 343 | TotalReceitas | 2.881,6 |
| 2017 | 346 | TotalReceitas | 2.614,2 |
| 2018 | 348 | TotalReceitas | 2.971,0 |
| 2019 | 707 | ReceitasExcetoIntraOrcamentarias | 3.062,7 |
| 2020 | 703 | ReceitasExcetoIntraOrcamentarias | 3.722,0 |
| 2021 | 707 | ReceitasExcetoIntraOrcamentarias | 4.339,5 |
| 2022 | 821 | ReceitasExcetoIntraOrcamentarias | 4.424,4 |
| 2023 | 811 | ReceitasExcetoIntraOrcamentarias | 4.460,8 |
| 2024 | 824 | ReceitasExcetoIntraOrcamentarias | 4.958,4 |
| 2025 | 851 | ReceitasExcetoIntraOrcamentarias | 5.842,4 |


### ❌ A DCA expõe a natureza de receita em 8 dígitos?

**Não.** A DCA agrega a natureza de receita em 7 níveis (`1.1.1.3.03.1.0`): o último dígito é sempre `0`. O 8º dígito — o que distingue principal (`1`) de multas e juros (`2`), dívida ativa (`3`) e acessórios (`7`, `8`) — **não é publicado no Anexo I-C**. A Regra 2 do PROJETO-CTB não é aplicável a esta fonte.

| último dígito do código | ocorrências |
|---|---|
| 0 | 845 |


## Reconciliação União 2024

### ✅ A DCA reproduz os totais por rubrica do Balanço Geral da União?

**Sim, ao centavo.** `receita bruta + Outras Deduções da Receita` da DCA iguala o total da planilha (principal + acessórios) em 10 das 11 rubricas. A única exceção é *Taxas — poder de polícia*, que é exatamente a divergência de Taxas já registrada em `docs/divergencias.md`. Ou seja: a diferença entre as duas fontes **não é de cobertura, é de conceito** — a planilha publica o principal, a DCA publica bruto e dedução.

| rubrica | planilha: principal | planilha: total | DCA líquida | DCA − planilha |
|---|---|---|---|---|
| Comércio exterior | 77,507 | 77,762 | 77,762 | +0,000 |
| ITR / patrimônio | 3,246 | 3,493 | 3,493 | −0,000 |
| Imposto de Renda | 764,550 | 785,151 | 785,151 | +0,000 |
| IPI | 82,174 | 84,373 | 84,373 | −0,000 |
| IOF | 67,402 | 67,748 | 67,748 | +0,000 |
| Taxas — poder de polícia | 7,907 | 7,988 | 8,056 | +0,067 |
| Taxas — prestação de serviços | 1,453 | 1,455 | 1,455 | +0,000 |
| Cofins | 353,793 | 367,242 | 367,242 | +0,000 |
| PIS/Pasep | 99,843 | 103,824 | 103,824 | +0,000 |
| CSLL | 160,607 | 166,760 | 166,760 | +0,000 |
| RGPS | 611,642 | 636,975 | 636,975 | +0,000 |


### ❌ Dá para separar principal de acessório usando só a DCA?

**Não.** Os acessórios (multas, juros e dívida ativa) somam **R$ 77,507 bi** em 2024 na planilha, e é exatamente essa massa que a DCA embute nos totais sem separar. A linha *Multas e Dívida Ativa* dos quadros — e os valores de IR, IPI, Cofins etc. que hoje são publicados **só com o principal** — não podem ser reproduzidos a partir do Siconfi. Esta é a decisão metodológica bloqueante da Fase 1.

| 8º dígito (tipo) | R$ bi em 2024 |
|---|---|
| 1 | 2.436,392 |
| 2 | 25,118 |
| 3 | 28,537 |
| 4 | 5,493 |
| 5 | 2,969 |
| 6 | 5,424 |
| 7 | 2,645 |
| 8 | 7,321 |


### ✅ A Regra 2 (só o principal) vale para todas as rubricas?

**Não — e a exceção é a divergência de R$ 0,083 bi do CLAUDE.md.** *Taxas* é a única rubrica publicada com `principal + acessórios`; as demais usam só o principal. Os R$ 0,0830 bi de acessórios de taxas explicam ao mesmo tempo por que a linha *Taxas* ficava alta e por que *Multas e Dívida Ativa* ficava baixa: são os mesmos reais, contados de um lado só. Com essa exceção declarada, a classificação da União fica **100% reproduzível por regra** em 2024. A exceção pertence ao dicionário (coluna por rubrica), não ao código. Ver `docs/divergencias.md` §1.

| hipótese | calculado (R$ bi) | publicado (R$ bi) | diferença |
|---|---|---|---|
| Taxas: só o principal (Regra 2 literal) | 9,3607 | 9,4437 | +0,0830 |
| Taxas: principal + acessórios | 9,4437 | 9,4437 | +0,0000 |
| Multas e DA: todos os acessórios | 77,5067 | 77,4237 | −0,0830 |
| Multas e DA: menos os de taxas | 77,4237 | 77,4237 | −0,0000 |


## Estados e DF (Siconfi DCA)

### ✅ Os 26 estados e o DF entregaram o Anexo I-C em todos os anos?

Cobertura integral: nenhuma imputação é necessária na esfera estadual.

| ano | declarantes | ausentes |
|---|---|---|
| 2016 | 27/27 | — |
| 2017 | 27/27 | — |
| 2018 | 27/27 | — |
| 2019 | 27/27 | — |
| 2020 | 27/27 | — |
| 2021 | 27/27 | — |
| 2022 | 27/27 | — |
| 2023 | 27/27 | — |
| 2024 | 27/27 | — |
| 2025 | 27/27 | — |


## Cobertura municipal (Siconfi DCA)

### ✅ Quantos municípios entregaram a DCA em cada ano?

Censo completo dos 47 municípios acima de 500.000 habitantes (a salvaguarda de parada do PROJETO-CTB §5) mais amostra aleatória de 300 dos 5.522 demais, semente 20260830. A varredura exaustiva dos 5.570 municípios custa ~15 min por ano com 6 conexões e é feita uma única vez na Fase 2, ficando em cache. A amostra aqui serve só para dimensionar a imputação.

**Brasília foi excluída do universo municipal**: o Distrito Federal entrega a DCA como ente de esfera `D`, e não existe prefeitura declarante. Contá-la como faltante dispararia a salvaguarda de parada todo ano por uma razão errada. As receitas tipicamente municipais do DF entram pela regra do DF, que precisa estar declarada no dicionário — ver `docs/decisoes-pendentes.md`.

| ano | grandes declarantes | cobertura estimada (amostra) | população coberta (amostra) | grandes ausentes |
|---|---|---|---|---|
| 2016 | 47/47 | 98,3% ± 1,4 p.p. | 97,8% | 0 |
| 2017 | 47/47 | 99,7% ± 0,7 p.p. | 99,7% | 0 |
| 2018 | 47/47 | 99,3% ± 0,9 p.p. | 99,6% | 0 |
| 2019 | 47/47 | 100,0% ± 0,0 p.p. | 100,0% | 0 |
| 2020 | 47/47 | 100,0% ± 0,0 p.p. | 100,0% | 0 |
| 2021 | 47/47 | 100,0% ± 0,0 p.p. | 100,0% | 0 |
| 2022 | 47/47 | 99,3% ± 0,9 p.p. | 99,8% | 0 |
| 2023 | 47/47 | 99,7% ± 0,7 p.p. | 99,3% | 0 |
| 2024 | 47/47 | 99,0% ± 1,1 p.p. | 99,0% | 0 |
| 2025 | 47/47 | 96,7% ± 2,0 p.p. | 97,1% | 0 |


### ✅ Algum município acima de 500.000 habitantes faltou?

Nenhum. A salvaguarda de parada não dispara em nenhum ano da série.

| ano | município | UF | população |
|---|---|---|---|
| — | — | — | — |


## Transferências constitucionais

### ⚠️ O endpoint `apiapex.tesouro.gov.br/aria/v1/` do PROJETO-CTB funciona?

**Não** — todos os caminhos testados retornam 404; o host responde, a rota do documento está errada. O caminho viável é o CKAN do Tesouro Transparente, que publica os repasses em CSV mensal por bloco (União→Estados e União→Municípios). São ~120 arquivos por bloco na série 2016–2025, todos cacheáveis. O bloco Estados→Municípios (cota-parte do ICMS e do IPVA) **não está aqui** e precisa vir da própria DCA estadual ou de fonte separada — item aberto da Fase 2.

| recurso | status / nº de CSVs |
|---|---|
| `aria/v1/transferencias_constitucionais/` | 404 |
| `aria/v1/transferencias-constitucionais/anexos` | 404 |
| `aria/v1/transferencias` | 404 |
| `transferencias-constitucionais-para-estados` | 155 |
| `transferencias-constitucionais-para-municipios` | 143 |


## IBGE / SIDRA

### ✅ PIB corrente e população estão disponíveis para toda a série?

O SIDRA responde sem autenticação e em menos de um segundo. O PIB da tabela 1846 é trimestral: o denominador anual é a soma dos quatro trimestres, e a série já cobre 2025. A tabela 6579 (estimativas) traz população por município, insumo obrigatório da imputação. Registrar `data_extracao_pib` desde a primeira rodada — revisão do PIB pelo IBGE altera toda a série de % do PIB.

| consulta | status | retorno |
|---|---|---|
| PIB corrente, tabela 1846 | 200 | 40 valores |
| População residente, tabela 6579 | 200 | 6 valores |
| População municipal, tabela 6579 | 200 | 5571 valores |


## Fontes sem API

### ⚠️ O que precisa entrar por `manual/`?

FGTS (Caixa) e Sistema S (Receita Federal) não têm API e entram como CSV em `manual/`, com fonte e data declaradas. Nenhum dos dois foi coletado ainda — o pipeline deve falhar com mensagem clara enquanto faltarem, nunca preencher com zero. Pelos quadros da planilha, FGTS e Sistema S pesam na base *salários e mão-de-obra*, que responde por cerca de um quarto da arrecadação: não é resíduo desprezível.

| bloco | fonte | formato | situação |
|---|---|---|---|
| FGTS | Caixa Econômica Federal | relatório anual | pendente |
| Sistema S | Receita Federal | planilha de arrecadação | pendente |
