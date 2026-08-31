# Projeto CTB — Carga Tributária Brasileira (cálculo próprio, automatizado)

Documento de estruturação para desenvolvimento no Claude Code.
Base metodológica: `CTB2024.xlsx` (ano-base detalhado) e `CTB-Resumo.xlsx` (série 2000–2024).

**Escopo do projeto: série 2016–2025, integralmente recalculada pela metodologia
automatizada.** A série 2000–2015 das planilhas permanece como acervo histórico e não
é reproduzida.

---

## 1. Diagnóstico do que existe hoje

### 1.1 Os dois arquivos

| Arquivo | Papel | Conteúdo |
|---|---|---|
| `CTB2024.xlsx` | **Máquina de cálculo de um ano** | Abas de trabalho com os microdados (`Impostos`, `Contribuições`, `Patrimoniais`, `Multas` = naturezas de receita da União; `Estados`, `Municipios` = pivôs do Siconfi; `Transferencias`) e as abas de saída |
| `CTB-Resumo.xlsx` | **Série histórica consolidada** | Mesmas abas de saída, com 25 anos lado a lado (2000–2024), 4 métricas por ano (R$ bi, % PIB, % Total, per capita) |

Para este projeto, os dois arquivos servem como **especificação da metodologia e
referência de comparação** — não como fonte de dados. Todo número publicado será
recalculado a partir das APIs.

### 1.2 Os cinco quadros de saída (que a página web precisa reproduzir)

1. **AD ESFERA** — Arrecadação direta por esfera (União/Estados/Municípios, agregado)
2. **byGOVDetalhado** — Arrecadação direta por esfera, aberta por tributo (~35 linhas)
3. **PRINCIPAIS TRIBUTOS** — Ranking dos ~17 tributos + coluna de acumulado
4. **Bases de Incidência** — 8 bases (bens e serviços, salários, renda, patrimônio, comércio exterior, taxas, transações financeiras, demais)
5. **RD ESFERA** — Receita disponível pós-transferências + detalhe das transferências constitucionais (3 blocos: União→Estados, União→Municípios, Estados→Municípios)

Mais a aba `Gráficos`: série da carga em % PIB e a divisão % AD União vs % RD União —
que é o gráfico-síntese do federalismo fiscal.

### 1.3 Por que automatizar (evidências nos próprios arquivos)

- Aba `Estados` do `CTB2024.xlsx` tem o cabeçalho **"ANO 2022"** com dados de 2024 — resíduo de copy/paste.
- `SAL.EDUCAÇÃO` aparece como 21,414 bi em `RD ESFERA` e vazio/zero na aba `Transferencias` do mesmo arquivo.
- Todo o vínculo entre microdado e quadro final está em tabelas dinâmicas e referências de célula não rastreáveis.

Nada disso é erro grave — é o custo normal de uma cadeia em Excel. É exatamente o que
o projeto elimina, e é a razão de o recálculo ser integral e não incremental.

---

## 2. Descoberta central: a metodologia é reproduzível por regra

Esta é a informação mais importante para o projeto. A classificação da arrecadação da
União **não é ad hoc** — ela é uma função do código de natureza de receita (8 dígitos).

**Regra 1 — prefixo (4 primeiros dígitos) define a rubrica:**
`1111` = comércio exterior · `1112` = ITR · `1113` = IR · `1114` = IPI · `1115` = IOF ·
`1119` = outros impostos · `1121`/`1122` = taxas

**Regra 2 — último dígito define se é principal ou acessório:**
`...1` = principal · `...2` multas e juros · `...3` dívida ativa · `...7` multas da DA ·
`...8` juros da DA. Tudo que **não** é principal vai para a linha única
**"Multas e Dívida Ativa"** — **exceto em Taxas**, que retém os próprios acessórios.

**Validação executada contra os valores de 2024 da planilha:**

| Rubrica | Recalculado pela regra | Planilha | Bate? |
|---|---|---|---|
| IR | 764,550 | 764,550 | ✅ |
| IPI | 82,174 | 82,174 | ✅ |
| IOF | 67,402 | 67,402 | ✅ |
| Comércio exterior | 77,507 | 77,507 | ✅ |
| ITR | 3,246 | 3,246 | ✅ |
| Cofins | 353,793 | 353,793 | ✅ |
| Taxas (principal + acessórios) | 9,4437 | 9,4437 | ✅ |
| Multas e Dívida Ativa (acessórios menos os de taxas) | 77,4237 | 77,4237 | ✅ |

Todas as rubricas fecham. **A automação é viável e o resultado é auditável.**

> **Atualizado na Fase 0 (2026-08-30).** A versão original deste documento registrava
> Taxas em 9,361 contra 9,444 publicado — diferença de R$ 83 milhões, suposta como "uma
> taxa classificada fora das abas de impostos". Não era: *Taxas* é a única rubrica
> publicada com principal + acessórios. Os mesmos R$ 0,083 bi que faltavam em Taxas
> sobravam em *Multas e Dívida Ativa*. Com a exceção declarada, as duas linhas fecham na
> quarta casa decimal e **não resta nenhuma rubrica ad hoc em 2024**. Demonstração em
> `docs/divergencias.md` §1.

> **⛔ Restrição descoberta na Fase 0 — e a decisão que ela forçou.** A Regra 2 **não é
> aplicável ao Siconfi**: o Anexo I-C agrega a natureza de receita em 7 níveis
> (`1.1.1.3.03.1.0`) e o 8º dígito é sempre `0`. A DCA reproduz o *total* por rubrica ao
> centavo (`receita bruta + Outras Deduções da Receita`), mas não a decomposição
> principal × acessório. Nenhuma fonte pública mapeada expõe os 8 dígitos.
>
> **Em 2026-08-30 foi decidida a opção B:** adotar o conceito do Siconfi. A partir daqui
> as duas regras acima são **história, não metodologia** — ficam neste documento porque
> explicam a série publicada até 2024 e sustentam a Fase 4. A regra de cálculo vigente
> está no `CLAUDE.md` §Regras de classificação: conta DCA de 7 níveis, receita líquida,
> sem linha *Multas e Dívida Ativa*. Impacto numérico completo em
> `docs/decisoes-pendentes.md` §1.

**Consequência de projeto:** o coração do sistema é um **dicionário versionado**, não
código. O código só aplica o dicionário. Com a opção B, ele é chaveado por conta DCA
(`RO1.1.1.3.00.0.0`) e não por natureza de 8 dígitos — o seed
`de_para_naturezas_2024_seed.csv` citado na versão original deste documento não está no
repositório e, de todo modo, tem a chave errada para a metodologia adotada. As 280
naturezas de 8 dígitos das abas de microdado do `CTB2024.xlsx` continuam úteis como
referência de rótulo e para a Fase 4.

**Vigência:** como a série vai de 2016 a 2025, o dicionário precisa de colunas
`vigencia_inicio` / `vigencia_fim` desde o primeiro commit. Códigos de natureza mudam,
e a reforma tributária vai forçar coexistência de rubricas antigas e novas.

---

## 3. Arquitetura proposta

```
ctb/
├─ CLAUDE.md                    # instruções para o Claude Code
├─ pipeline/                    # Python — toda a lógica de cálculo
│  ├─ fontes/                   # 1 módulo por fonte (siconfi, transferencias, ibge, manual)
│  ├─ dominio/                  # classificação, imputação municipal, transferências, receita disponível
│  └─ publicar/                 # escreve os JSON do site
├─ dicionario/                  # ★ o ativo intelectual — CSVs versionados em git
│  ├─ naturezas_uniao.csv
│  ├─ contas_dca_estados.csv
│  ├─ contas_dca_municipios.csv
│  ├─ bases_incidencia.csv
│  └─ faixas_populacionais.csv  # parâmetro da imputação municipal
├─ dados/
│  ├─ bruto/                    # resposta crua das APIs, particionada por ano (cache)
│  ├─ intermediario/            # parquet normalizado
│  └─ publicado/                # JSON servido ao site
├─ manual/                      # fontes sem API (FGTS/CEF, Sistema S/RFB) + procedimento
├─ testes/
│  ├─ invariantes/              # somas fecham, cobertura mínima, sem natureza órfã
│  └─ comparacao_historica/     # ★ diff contra a planilha, para diagnóstico — não é gate
└─ site/                        # front-end estático
```

**Fluxo:** APIs → `bruto/` (cache em disco, nunca refaz download à toa) → normalização
para formato longo → imputação municipal → aplicação do dicionário → agregação →
`publicado/*.json` → site estático lê os JSON. Sem banco de dados, sem backend.

**Por que estático:** a carga tributária é anual. Um GitHub Action mensal roda o
pipeline e, se algo mudou, abre um PR com o diff dos números — você aprova ou não.
Isso dá controle editorial sobre um número institucionalmente sensível.

### Front-end

Recomendação: **Vite + React + ECharts**. O Claude Code trabalha bem nessa stack, gera
build estático, e o ECharts dá exportação PNG/SVG nativa — importante para reaproveitar
os gráficos em publicações da GPE.

Alternativa: **Observable Framework**, que integra data loaders Python e site num só
projeto. Mais elegante, menos flexível para identidade visual institucional.

---

## 4. Fontes e endpoints

| Bloco | Fonte | Acesso | Situação |
|---|---|---|---|
| Receitas das três esferas (totais por rubrica, receita líquida) | **Siconfi DCA**, `id_ente=1` para a União, código IBGE para estados/DF/municípios | `id_ente=U` devolve HTTP 400 — `U` é o valor da coluna `esfera`, não do identificador. Traz 2016–2025 em 7 níveis. A separação principal × acessório não existe (decisão 1, opção B: não é mais necessária) | ✅ testado, dicionário validado nas três esferas |
| Receitas Estados/Municípios | **Siconfi DCA**, Anexo I-C | `https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca` — params `an_exercicio`, `id_ente`, `no_anexo=DCA-Anexo I-C`; JSON `{items, hasMore}`, sem autenticação. Conta-raiz muda em 2019 | ✅ testado, 2016–2025 |
| Lista de entes e códigos | Siconfi | `/ords/siconfi/tt/entes` — 5.598 entes, com população; União como `cod_ibge=1` | ✅ testado |
| Transferências constitucionais | STN | **API do Tesouro**, `apiapex.tesouro.gov.br/aria/v1/transferencias_constitucionais/custom/<endpoint>` (decisão 5) — catálogo de 18 modalidades, inclui royalties de transferência (código 12) | ✅ testado, 2026-08-31; bloco Estados→Municípios ainda sem fonte |
| PIB corrente | IBGE / Contas Nacionais Trimestrais | SIDRA tabela **1846**, somar os 4 trimestres do ano. Série já cobre 2025 | ✅ testado |
| População (Brasil e municípios) | IBGE / estimativas e projeções | SIDRA tabela **6579** — 5.571 municípios. **Insumo obrigatório da imputação** | ✅ testado |
| FGTS | Caixa Econômica Federal | Sem API — relatório anual | ❌ **manual** |
| Sistema S | Receita Federal | Sem API — planilha de arrecadação | ❌ **manual** |
| Royalties (arrecadação própria de cada esfera) | Siconfi DCA, ramo `RO1.3.4` | Cada esfera declara a própria cota como beneficiária — não é repartição/transferência, é receita patrimonial direta. Linha própria por decisão 4 | ✅ mapeado nas três esferas |

**Nota sobre o ente da União (atualizada na Fase 0):** usar o Siconfi para a União, em
vez do Balanço Geral, tem uma vantagem metodológica além da conveniência — as três
esferas passam a vir da mesma fonte, com o mesmo plano de contas e o mesmo critério de
consolidação. O teste confirmou o acesso (`id_ente=1`, dez anos, inclusive 2025) e
mostrou que a DCA reproduz o total por rubrica **ao centavo**. Mas o Anexo I-C **não**
traz o detalhe de 8 dígitos, e o plano B previsto — o CKAN do Tesouro Transparente —
também não: o pacote `receita-orcamentaria-da-uniao` é agregado por categoria econômica.
A escolha da fonte de 8 dígitos passou a ser uma decisão metodológica aberta, não uma
questão técnica: `docs/decisoes-pendentes.md` §1.

**Decisão de projeto:** não fingir que dá para automatizar 100%. As fontes manuais viram
CSVs em `manual/` com schema validado e um `PROCEDIMENTO.md` de meia página dizendo onde
baixar e o que preencher. O pipeline **falha com mensagem clara** se faltar o ano — nunca
preenche com zero silenciosamente.

---

## 5. Imputação de municípios sem DCA

Nenhum ano tem 100% dos 5.570 municípios entregando a DCA. A regra adotada é
**imputação por receita tributária per capita média da faixa populacional**.

### Procedimento

1. Montar o universo do ano: todos os municípios com sua população estimada (IBGE).
2. Identificar os declarantes (DCA Anexo I-C entregue e válida para o ano).
3. Classificar todos — declarantes e faltantes — em faixas populacionais.
4. Para cada faixa e **para cada rubrica** (ISS, IPTU, ITBI, IRRF, taxas, contribuições,
   COSIP, Royalties e Compensações Financeiras — a lista final é a das rubricas do
   dicionário municipal, `dicionario/contas_dca_municipios.csv`), calcular a receita per
   capita média dos declarantes da faixa.
5. Para cada município faltante: `valor_imputado(rubrica) = per_capita_médio(faixa, rubrica) × população_do_município`.
6. Marcar cada linha imputada com `imputado = true` e `metodo_imputacao`.

A imputação é feita **por rubrica, não sobre o total**. Imputar só o agregado
distorceria a composição tributária municipal, que é uma das saídas do quadro
`byGOVDetalhado`.

### Faixas (decisão 3, 2026-08-31 — parametrizáveis em `dicionario/faixas_populacionais.csv`)

**Não são um corte arbitrário.** São as 18 faixas oficiais do FPM Interior, do
Decreto-Lei nº 1.881/1981 — o mesmo critério que o TCU usa todo ano para ratear o Fundo
de Participação dos Municípios:

| Faixa | População | Faixa | População |
|---|---|---|---|
| 1 | até 10.188 | 10 | 61.129 a 71.316 |
| 2 | 10.189 a 13.584 | 11 | 71.317 a 81.504 |
| 3 | 13.585 a 16.980 | 12 | 81.505 a 91.692 |
| 4 | 16.981 a 23.772 | 13 | 91.693 a 101.880 |
| 5 | 23.773 a 30.564 | 14 | 101.881 a 115.464 |
| 6 | 30.565 a 37.356 | 15 | 115.465 a 129.048 |
| 7 | 37.357 a 44.148 | 16 | 129.049 a 142.632 |
| 8 | 44.149 a 50.940 | 17 | 142.633 a 156.216 |
| 9 | 50.941 a 61.128 | 18 | acima de 156.216 |

Checado contra o censo completo de 2024: as faixas 16 e 17 têm 29 e 18 declarantes,
abaixo do mínimo de 30 — é onde a salvaguarda abaixo entra em ação. As outras dezesseis
têm folga (40 a 2.478 declarantes). Detalhes em `docs/decisoes-pendentes.md` §3.

### Salvaguardas obrigatórias

- **Faixa com poucos declarantes:** se uma faixa tiver menos de um número mínimo de
  declarantes (sugestão: 30), o pipeline avisa e usa a faixa vizinha. As faixas 16 e 17
  são as de risco confirmado — ver acima.
- **Municípios grandes ausentes:** se uma capital ou município com mais de 500 mil
  habitantes não declarou, o pipeline **para e reporta**. Imputar São Paulo pela média
  da faixa é inaceitável — nesse caso a decisão é sua (buscar o dado na fonte do próprio
  município, ou repetir o ano anterior corrigido).
- **Sensibilidade:** rodar também com mediana em vez de média e registrar a diferença em
  `docs/sensibilidade-imputacao.md`. A média é sensível a outliers (municípios com
  royalties altos, por exemplo), e vale saber o tamanho do efeito antes de publicar.
- **Transparência:** a página publica, por ano, o número de municípios declarantes, o
  percentual da população coberta e o **percentual da receita municipal que é imputado**.
  Se esse último número passar de um patamar razoável em algum ano, isso precisa aparecer
  como nota, não ficar escondido.

### Detalhe conhecido: Distrito Federal ✅ resolvido pela decisão 2

O DF acumula competências estaduais e municipais. A regra (decisão 2,
`docs/decisoes-pendentes.md` §2): **ISS, IPTU, ITBI e COSIP** do DF vão para o bloco
Municípios; todo o resto — ICMS, IPVA, ITCD, IRRF, taxas, demais contribuições — fica no
bloco Estados. Implementada na coluna `bloco` de `dicionario/contas_dca_estados.csv`.
Confirmado no censo de 2024 que só o DF lança COSIP entre os 27 entes de esfera E/D —
nenhum estado real tem essa competência.

**Detalhe do cadastro, verificado na Fase 0:** o DF aparece duas vezes em
`/tt/entes` — como ente de esfera `D` (`cod_ibge=53`), que é quem entrega a DCA, e como
município Brasília (`cod_ibge=5300108`), que **nunca entrega**, porque não existe
prefeitura de Brasília. Brasília precisa ser excluída do universo municipal: contá-la
como faltante dispara a salvaguarda de município grande ausente nos dez anos por uma
razão errada.

---

## 6. Modelo de dados

Uma única tabela longa em `intermediario/`, da qual todos os quadros derivam por
agregação:

```
ano | esfera | id_ente | co_natureza | no_natureza | rubrica | tributo |
base_incidencia | tipo_lancamento | valor_reais | imputado | metodo_imputacao |
fonte | versao_dicionario
```

E um arquivo de denominadores:

```
ano | pib_corrente_reais | populacao | data_extracao_pib
```

Os quatro indicadores (R$ bi, % PIB, % total, per capita) **nunca são armazenados** —
são calculados na publicação. Isso elimina a classe inteira de erros em que uma célula
de % ficou apontando para o ano errado.

**Regra de ouro:** nenhum número no repositório é digitado. Ou vem de API, ou vem de
`manual/` com fonte declarada, ou é resultado de imputação explicitamente marcada.

---

## 7. Roadmap

### Fase 0 — Reconhecimento ✅ **concluída em 2026-08-30**
Script que testa cada endpoint da seção 4 para os anos 2016–2025 e reporta cobertura,
tempo de resposta e formato. Prioridades: (a) o Siconfi traz o detalhe de 8 dígitos?
(b) quantos municípios declararam em cada ano?
**Entregável:** `docs/viabilidade-fontes.md`, gerado por `uv run ctb fontes testar` e
reexecutável a partir do cache.

Respostas: **(a) não** — a DCA agrega em 7 níveis; ela reproduz o total por rubrica ao
centavo, mas não a decomposição principal × acessório. **(b)** entre 96,7% e 100,0% dos
municípios por ano (amostra de 300, ±2,0 p.p. no pior ano), com a salvaguarda de
município grande ausente não disparando em nenhum ano. A imputação é marginal em toda a
série. Estados e DF: 27/27 nos dez anos.

### Fase 1 — Dicionário ✅ **concluída em 2026-08-31, todas as oito decisões tomadas**
Mapear as contas DCA das três esferas para rubrica, tributo e base de incidência, com
`vigencia_inicio`/`vigencia_fim`. Chave: `cod_conta`.

Situação, por `uv run ctb dicionario validar`:

| esfera | contas | rubricas | estrutura | cobertura | continuidade | reconciliação 2024 |
|---|---|---|---|---|---|---|
| União | 47 | 17 | ✅ | ✅ sem órfãs | ✅ | ✅ exata (Taxas +0,067; royalties dentro da tolerância documentada) |
| Estados e DF | 43 | 12 | ✅ | ✅ sem órfãs | ✅ | ✅ exata (estrutural, receita bruta) |
| Municípios | 48 | 9 | ✅ | ✅ sem órfãs | ✅ | ⚠️ 2 resíduos (IPTU, IRRF) — ver `docs/divergencias.md` §5 |

Cobertura e continuidade valem para os **dez anos**, sobre o censo completo dos 5.569
municípios em toda a série (2,18 GB de cache, 55.986 respostas).

A checagem de continuidade não é decorativa: foi ela que achou os dois casos de tributo
lançado em conta sem competência do ente (`docs/divergencias.md` §6), que os totais de um
ano isolado não revelariam.

**As oito decisões de `docs/decisoes-pendentes.md` estão todas tomadas** (2026-08-31):
opção B para a separação principal × acessório (1), COSIP do DF no bloco Municípios (2),
faixas do FPM (3), royalties com linha própria (4), API do Tesouro para transferências
(5), receita líquida uniforme nas três esferas (6), reclassificação de IRPF/IRPJ mantida
(7), site público (8). Os efeitos numéricos de cada uma estão documentados na respectiva
seção, medidos contra o censo completo, não estimados.

**Critério de aceite (revisado pela opção B):** o alvo **não é mais** reproduzir
`byGOVDetalhado` diretamente — a metodologia mudou em três frentes (opção B, royalties
com linha própria, receita líquida em E/M). O validador separa duas checagens: a
**estrutural** (receita bruta contra `byGOVDetalhado`, que ainda tem que fechar — prova
que as contas estão mapeadas certo) e o **efeito das decisões** (informativo, mostra a
receita líquida que será de fato publicada). Nenhuma conta de arrecadação pode ficar sem
rubrica (natureza órfã é erro, não "outros"); os ramos patrimoniais que não são royalties
ficam deliberadamente fora do escopo, não pendentes.

O ponto de atenção específico da opção B: a árvore de contas da DCA é hierárquica —
`RO1.1.1.0.00.0.0` já contém `RO1.1.1.3.00.0.0`. Somar pai e filho conta duas vezes. O
dicionário precisa declarar, por rubrica, qual é o nível de agregação.

### Fase 2 — Ingestão e cálculo de um ano ✅ **quatro dos cinco quadros, 2026-08-31**
Módulos de fonte com cache e retry. Reconstruir 2024 **inteiramente a partir das APIs**,
sem tocar no Excel, incluindo a imputação municipal.
**Critério de aceite:** o total de 2024 sai coerente com a ordem de grandeza conhecida
(~36% do PIB) e toda divergência contra a planilha tem causa identificada.

`uv run ctb calcular --anos 2024` roda de ponta a ponta e escreve
`docs/resultado-2024.md`. Total calculado: **R$ 3.981,516 bi (33,80% do PIB)**. Fecha o
critério de aceite: somando de volta o gap conhecido de FGTS + Sistema S (fontes
manuais, ainda não ingeridas — R$ 221,3 bi, 1,88 p.p.), o total sobe para **35,68%**,
muito perto dos 35,950% publicados; o resíduo final (~0,27 p.p.) é o efeito deliberado
da decisão 6 (receita líquida em estados/municípios) somado aos resíduos pequenos já
documentados em `docs/divergencias.md`.

Imputação municipal: 5.544 declarantes + 25 imputados = 5.569 municípios, 99,82% da
população coberta, 0,095% da receita municipal imputada. As faixas 16 e 17 (as de menos
de 30 declarantes, previstas na decisão 3) mesclaram com a faixa vizinha, como
projetado.

**Segunda passada (mesmo dia):** `AD ESFERA` e `PRINCIPAIS TRIBUTOS`. A composição de
cada um foi reverso-engenheirada do `CTB2024.xlsx` com casamento exato contra os
valores publicados — não é mais incógnita:

- `AD ESFERA` não é uma categoria econômica uniforme — é "os 2 a 4 maiores itens de
  cada esfera, nomeados, resto em Demais". União: Impostos (IR+IPI+IOF+ITR+Comércio
  Exterior), Contribuições Sociais (Cofins+CSLL+PIS-PASEP+CPMF+Contrib.Seg.Serv.
  Público+Outras contrib. sociais+Salário Educação+Sistema S), Previdência Social,
  Demais. Estados: ICMS, IPVA, Demais. Municípios: ISS, IPTU, Demais. Confirmado exato
  contra 2024 em `pipeline/dominio/quadros.py`.
- `PRINCIPAIS TRIBUTOS`: a maioria é uma rubrica de esfera só (confere exato). Três
  cruzam esferas: "Imposto de Renda (Global)" = IR da União + IRRF de estados +
  IRRF de municípios (confere exato: 894,479 na metodologia antiga); "Previdência
  Social Ampliada" = RGPS + Previ. Estadual + Previd. Municipal (aproxima, não fecha
  ao centavo — reportado sem forçar). Desvio deliberado: a linha "Comércio Exterior"
  fica combinada (importação + exportação), porque o dicionário da União agrega os
  dois numa conta só.

Ambos calculados sem dado novo, a partir da mesma tabela intermediária. Fica para uma
passada seguinte: `RD ESFERA`, que depende de transferências constitucionais — a fonte
da decisão 5 cobre a maior parte, mas a planilha mostra duas modalidades sem código
correspondente (Salário-Educação, Seguro-Receita ICMS), além do bloco
Estados→Municípios, que continua sem fonte.

Módulos novos: `pipeline/fontes/sidra.py` (PIB e população), `pipeline/fontes/cache.py`
e `pipeline/fontes/planilha_referencia.py` (extraídos de `validar.py`/`diagnostico.py`
para reaproveitar sem duplicar), `pipeline/dominio/imputacao.py`,
`pipeline/dominio/agregacao.py`, `pipeline/dominio/quadros.py` e
`pipeline/dominio/calcular.py` (orquestrador). `classificar()` em `dicionario.py` ganhou
o parâmetro `com_base`, porque rubrica não determina base de incidência univocamente
(rubricas residuais como "Outros impostos" agregam contas de bases diferentes).

Achado de dados durante a construção: um município (Boa Esperança do Norte-MT) não tem
estimativa de população na tabela do SIDRA usada; o pipeline usa o cadastro de entes do
Siconfi como respaldo e avisa — sem isso, o município seria excluído do universo de
imputação em silêncio.

### Fase 3 — Série 2016–2025
Rodar os dez anos. Aqui aparecem as quebras de série: mudanças de codificação de
natureza, alterações no Anexo I-C, Fundeb novo (2021), variação da cobertura municipal.
**Critério de aceite:** os dez anos rodam sem erro, com relatório de cobertura e de
participação de valores imputados por ano.

O insumo pesado já está feito: o **censo municipal dos dez anos está em cache**, com a
contagem exata de declarantes por ano.

| ano | declarantes | % dos 5.569 |
|---|---|---|
| 2016 | 5.442 | 97,7% |
| 2017 | 5.556 | 99,8% |
| 2018 | 5.536 | 99,4% |
| 2019 | 5.553 | 99,7% |
| 2020 | 5.559 | 99,8% |
| 2021 | 5.562 | 99,9% |
| 2022 | 5.556 | 99,8% |
| 2023 | 5.556 | 99,8% |
| 2024 | 5.544 | 99,6% |
| 2025 | 5.481 | 98,4% |

**A imputação é marginal em toda a série** — no pior ano faltam 127 municípios, todos
pequenos (nenhum acima de 500 mil habitantes falta em ano nenhum). Isso reduz muito o peso
das decisões sobre faixas populacionais e média vs. mediana.

### Fase 4 — Diagnóstico da revisão
Comparar a nova série contra `CTB-Resumo.xlsx` ano a ano e linha a linha. **Isto não é
um teste que precisa passar** — é o material que vai sustentar a comunicação da revisão.
**Entregável:** `docs/revisao-metodologica.md`, com a tabela de diferenças em pontos
percentuais do PIB e a explicação de cada uma. Para uma publicação institucional, ter
esse documento pronto antes de divulgar vale mais que a própria automação.

### Fase 5 — Site
Os cinco quadros + gráficos, com seletor de ano e de unidade (R$ bi / % PIB / % total /
per capita), exportação CSV por tabela e PNG por gráfico. Nota de cobertura municipal
visível. Página de metodologia gerada a partir do próprio dicionário.

### Fase 6 — Automação
GitHub Action mensal: roda o pipeline e, se algum número mudou, abre PR com o diff.
Publicação só após aprovação.

---

## 8. Riscos

| Risco | Mitigação |
|---|---|
| ~~`id_ente=U` não trazer detalhe de 8 dígitos~~ **materializou-se** | Confirmado na Fase 0: nenhuma fonte pública mapeada expõe os 8 dígitos, e o plano B (CKAN) também não serve. Virou decisão metodológica, não risco: `docs/decisoes-pendentes.md` §1 |
| **Quebra de layout da DCA em 2019** (descoberta na Fase 0) | Conta-raiz muda de `TotalReceitas` para `ReceitasExcetoIntraOrcamentarias`; o pipeline lê as duas. Ler só uma silencia 2016–2018 |
| Mudança de codificação de natureza entre 2016 e 2025 | Dicionário com `vigencia_inicio`/`vigencia_fim` desde o início; natureza órfã é erro, não "outros" |
| Imputação distorcer anos de baixa cobertura | Reporte obrigatório do % imputado; teste de sensibilidade média vs. mediana; parada obrigatória se município grande faltar |
| **Reforma tributária (CBS/IBS)** em teste a partir de 2026 | Prever no dicionário desde já; ICMS/ISS/PIS/Cofins vão coexistir com as novas rubricas por anos |
| Revisão do PIB pelo IBGE altera toda a série de % PIB | Registrar `data_extracao_pib`; o site declara a data de referência da série de PIB |
| DCA 2025 ainda incompleta | É o ano com maior peso de imputação; tratar como preliminar e sinalizar na página |
| A nova série divergir da publicada anteriormente | Fase 4 produz a documentação da revisão antes da divulgação |

**Decisões metodológicas.** Todas as oito estão tomadas — histórico completo, com os
números dos dois lados e o efeito medido depois de implementada, em
`docs/decisoes-pendentes.md`:

1. ✅ Separação principal × acessório da União → **opção B**, conceito do Siconfi.
   *Multas e Dívida Ativa* (0,659 p.p. do PIB) deixa de existir.
2. ✅ Regra do DF → ISS, IPTU, ITBI **e COSIP** no bloco Municípios; resto em Estados.
3. ✅ Faixas populacionais → as 18 faixas oficiais do FPM (Decreto-Lei 1.881/1981), não
   um corte arbitrário.
4. ✅ Royalties → linha própria, *Royalties e Compensações Financeiras*, nas três
   esferas.
5. ✅ Fonte das transferências constitucionais → API do Tesouro,
   `apiapex.tesouro.gov.br/aria/v1/transferencias_constitucionais/custom/<endpoint>`.
   O bloco Estados→Municípios (cota-parte do ICMS/IPVA) continua sem fonte — não é
   coberto por essa API.
6. ✅ Receita bruta ou líquida em estados e municípios → **líquida**, uniforme com a
   União.
7. ✅ IRPF/IRPJ lançados por município → mantida a reclassificação para IRRF.
8. ✅ Site público ou interno → **público**.

O que ainda não tem decisão: o que entra em "receita disponível" no quadro `RD ESFERA`,
e a fonte do bloco Estados→Municípios das transferências (item 5 acima).

---

## 9. Estado atual do repositório

Fases 0 e 1 concluídas; Fase 2 com a primeira passada feita (2024, dois dos cinco
quadros). O que existe:

```
pipeline/fontes/http.py              cache em disco + retry; nunca refaz download
                                      sem --force
pipeline/fontes/cache.py             leitura do cache DCA já baixado (esferas dos
                                      entes, itens por esfera/ano)
pipeline/fontes/sidra.py             PIB corrente e população — SIDRA/IBGE
pipeline/fontes/planilha_referencia.py  leitura da aba byGOVDetalhado do CTB2024.xlsx,
                                      só para comparação
pipeline/fontes/diagnostico.py       Fase 0, reexecutável
pipeline/dominio/dicionario.py       carrega e aplica o dicionário — 3 operações de
                                      coluna, `com_base` para não perder a base de
                                      incidência de rubricas residuais, dupla
                                      contagem e conta órfã são erro
pipeline/dominio/validar.py          Fase 1 — estrutura, cobertura, continuidade,
                                      reconciliação
pipeline/dominio/imputacao.py        imputação municipal por faixa do FPM, com as
                                      duas salvaguardas do CLAUDE.md
pipeline/dominio/agregacao.py        monta a tabela intermediária de um ano
                                      (dados/intermediario/{ano}.parquet)
pipeline/dominio/quadros.py          4 dos 5 quadros a partir da tabela
                                      intermediária: byGOVDetalhado, Bases de
                                      Incidência, AD ESFERA, PRINCIPAIS TRIBUTOS
pipeline/dominio/calcular.py         orquestra a Fase 2, escreve
                                      docs/resultado-{ano}.md
pipeline/cli.py                      `ctb fontes testar/varrer-municipios`,
                                      `ctb dicionario validar`, `ctb calcular`; as
                                      demais fases recusam-se a rodar
docs/viabilidade-fontes.md           entregável da Fase 0 (gerado)
docs/resultado-2024.md               entregável da Fase 2 até agora (gerado)
docs/divergencias.md                 8 itens: 4 resolvidas, 4 abertas mas não urgentes
docs/decisoes-pendentes.md           8 decisões, todas tomadas, com números e efeito
                                      medido
dicionario/                          6 CSVs — contas das 3 esferas, política de
                                      colunas, bases de incidência, faixas
                                      populacionais (FPM)
dados/bruto/                         cache do Siconfi + SIDRA, fora do git
dados/intermediario/                 parquet por ano, fora do git (reproduzível do
                                      cache)
```

```bash
uv sync
uv run ctb fontes testar --anos 2016-2025           # regenera o relatório a partir do cache
uv run ctb dicionario validar --esfera U            # idem, U/E/M
uv run ctb calcular --anos 2024                     # gera docs/resultado-2024.md
```

**Próximo passo:** `RD ESFERA` (precisa do módulo de transferências constitucionais —
fonte identificada na decisão 5, mas ainda não escrito, mais resolver duas modalidades
sem código na API e o bloco Estados→Municípios) e/ou avançar para a Fase 3 (rodar os
dez anos com os quatro quadros já prontos).
