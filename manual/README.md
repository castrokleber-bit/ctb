# Fontes manuais

CLAUDE.md, regra 1: todo CSV aqui precisa de fonte e data declaradas.

## `transferencias_royalties_e_compensacoes_estados.csv` e `..._municipios.csv`

- **Conteúdo:** royalties (ANP, CFEM, CFH, FEP, ITA, PEA), Cessão Onerosa, AFM/AFE,
  LC 173/2020 (PFEC) e LC 201/2023 (Compensação ICMS) — por UF/município e ano,
  2016-2026.
- **Fornecidos por:** o usuário, em 2026-08-31, para uso em `RD ESFERA`
  (`pipeline/dominio/rd_esfera.py`).
- **Fonte original:** Tesouro Nacional — portal "Transferências a Estados e Municípios"
  (https://www.tesourotransparente.gov.br/temas/estados-e-municipios/transferencias-a-estados-e-municipios),
  confirmado pelo usuário em 2026-08-31. Os arquivos originais vieram em CP1252 e sem
  indicação de origem no próprio conteúdo; convertidos para UTF-8 (BOM) nesta pasta,
  mantendo os dados originais intactos.
- **Modalidades que aparecem nestes CSVs mas são ignoradas na leitura** (`rd_esfera.py`,
  `_normalizar_modalidade`): `FEX` e `LC 176/2020 (ADO25)` — já vêm, com o mesmo valor,
  do CKAN `transferencias-obrigatorias-da-uniao` (rótulo `FEX`/`LC176`); somar dos dois
  lados duplicaria a transferência.

## `fundeb_estados.csv` e `fundeb_municipios.csv`

- **Conteúdo:** valor redistribuído pelo FUNDEB a cada UF/município e ano (2016-2026),
  decomposto por modalidade de origem (`FUNDEB - ICMS`, `FUNDEB - FPE`, `FUNDEB - COUN`
  — Complementação da União — etc.), mesmo formato dos CSVs de royalties acima.
- **Fornecidos por:** o usuário, em 2026-09-01, como alternativa à planilha oficial da
  STN (abaixo) depois que o servidor que a hospeda (`thot-arquivos.tesouro.gov.br`)
  ficou fora do ar durante a extensão de `RD ESFERA` para a série 2016-2025. Fonte
  original provavelmente o mesmo portal "Transferências a Estados e Municípios" citado
  acima (mesmo formato/encoding), **não confirmada explicitamente pelo usuário para
  estes dois arquivos especificamente**.
- **Uso:** `pipeline/dominio/rd_esfera.py`, função `_somar_fundeb_manual` — reclassifica
  as modalidades em origem União (tudo, por eliminação) e origem Estados (`ICMS`, `IPVA`,
  `ITCMD` — os únicos tributos próprios que alimentam o pool). Validado contra a
  planilha oficial (abaixo) em 2024: a soma de `ICMS+IPVA+ITCMD` no CSV de municípios
  bate quase exato (R$ 109,830 bi) com "TOTAL ORIGEM ESTADOS" da planilha oficial
  (R$ 109,833 bi).
- **2024 continua vindo da planilha oficial, não deste CSV** — ver abaixo — para
  preservar os números já publicados em `docs/decisoes-pendentes.md` §9. Estes dois
  CSVs são usados só para 2016-2023 e 2025.

## Planilha oficial do FUNDEB (2024)

- **Fonte:** publicação "Transferências ao Fundo de Manutenção e Desenvolvimento da
  Educação Básica (FUNDEB)" do Tesouro Transparente
  (https://www.tesourotransparente.gov.br/publicacoes/transferencias-ao-fundo-de-
  manutencao-e-desenvolvimento-da-educacao-basica-fundeb/2024/114), baixada e
  cacheada em `dados/bruto/fundeb/2024/fundeb.xls` em 2026-08-31.
  `pipeline/fontes/fundeb.py` tem as URLs dos outros nove anos mapeadas, mas o
  servidor ficou fora do ar antes de baixá-las — por isso os CSVs acima cobrem esses
  anos em vez da planilha oficial.

## `FGTS.xlsx`, `Sistema S.xlsx`, `fgts_sistema_s.csv`

Fecha o maior gap conhecido do projeto (CLAUDE.md §Fontes: "FGTS (CEF) e Sistema S (RFB)
só em `manual/`"). `fgts_sistema_s.csv` é o que o pipeline lê
(`pipeline/dominio/manual_uniao.py`); os `.xlsx` e PDFs abaixo são os originais, mantidos
para conferência.

- **`Sistema S.xlsx`** — fornecido pelo usuário em 2026-09-01. Fonte declarada no
  próprio arquivo: "Cetad/RFB" (Centro de Estudos Tributários e Aduaneiros da Receita
  Federal). Total anual 2000-2023 numa coluna, e detalhe por entidade (SEBRAE, SENAC,
  SENAI, SENAR, SENAT, SESC, SESCOOP, SESI, SEST) para 2021-2024 — é dessa segunda
  tabela que sai o total de 2024 (R$ 29,320 bi), ausente da coluna simples.
- **`FGTS.xlsx`** — fornecido pelo usuário em 2026-09-01. A aba `Plan1` tem detalhe
  anual por tipo de arrecadação (Depósito/JAM/Multa × GFIP/GRFP/GRDE) de 1997 a 2016,
  mas os anos 2017-2019 dessa mesma aba têm valores claramente errados (ordem de
  grandeza ~1000× menor que o esperado — R$ 63 milhões contra os ~R$ 120 bi de anos
  vizinhos) e **não foram usados**. Em vez disso, 2016-2023 vêm do PDF mensal oficial
  da Caixa (abaixo), que é consistente ano a ano.
- **`Arrecadacao_Bruta_FGTS_2000_a_2024_Jan.pdf`** — baixado de
  https://www.caixa.gov.br/Downloads/fgts-informacoes-diversas/Arrecadacao_Bruta_2000_a_2024_Jan.pdf
  em 2026-09-01 (Caixa Econômica Federal, fonte "SUFUG - SN Fundo de Garantia"). Série
  mensal 2000-2024, mas só até janeiro/2024 — a Caixa parou de atualizar esse arquivo
  mensal específico depois disso. Usado para 2016-2023 (soma dos 12 meses).
- **`Demonstracoes_Financeiras_FGTS_2024.pdf`** — baixado de
  https://www.fgts.gov.br/Paginas/downloads/relatorios/demonstracoes_financeiras/Demosntracores_financeiras_FGTS-2024_V3.pdf
  em 2026-09-01. Demonstrações contábeis auditadas do FGTS; linha "Arrecadação Recebida
  em depósitos vinculados do FGTS" (Fluxo de Caixa das Atividades de Financiamento) dá
  2023 = R$ 176,101 bi e 2024 = R$ 192,547 bi. Usado para 2023 e 2024 **em vez do PDF
  mensal** — é a fonte auditada, mais autoritativa que a soma mensal (que dá R$ 175,433
  bi para 2023, 0,4% abaixo do valor auditado — diferença de reconhecimento contábil,
  não erro).
- **`Demonstracoes_Financeiras_FGTS_2025.pdf`** — baixado de
  https://www.fgts.gov.br/Paginas/downloads/relatorios/demonstracoes_financeiras/Demonstracao_Financeira_FGTS_2025.pdf
  em 2026-09-01 (achado navegando fgts.gov.br → Transparência e Prestação de Contas →
  Demonstrações Financeiras — a URL do documento de 2024 tinha um typo,
  "Demosntracores", que o de 2025 corrigiu para "Demonstracao", não é um padrão
  previsível). Mesma linha "Arrecadação Recebida em depósitos vinculados do FGTS" dá
  2025 = R$ 212,594 bi (auditado) — bate com a notícia do próprio site do FGTS
  ("arrecadação bruta do Fundo atingiu o recorde de R$ 212,6 bilhões, crescimento de
  10,4%"). Usado para 2025.
- **`repasses_arrecadacao_federal_outras_entidades.csv`** — fornecido pelo usuário em
  2026-09-02. Fonte: RFB, dataset "Repasses da Arrecadação Federal"
  (https://dados.gov.br/dados/conjuntos-dados/repasses-da-arrecadacao-federal), recurso
  "Repasse da arrecadação destinada a outras entidades e fundos". Série mensal desde
  jan/2015, por entidade (inclui as 9 do Sistema S — SEBRAE, SENAC, SENAI, SENAR,
  SENAT, SESC, SESCOOP, SESI, SEST — e outras não relacionadas ao Sistema S: FNDE,
  INCRA, EMBRATUR, DPC, ANAC, SDR, APEX-BR, ABDI, que não entram na soma). Somando as 9
  entidades do Sistema S para 2022-2024 reproduz exatamente os valores já usados
  (23,815 / 26,919 / 29,320 bi, vindos do `Sistema S.xlsx`) — mesma fonte primária,
  cruzamento perfeito. Usado para 2025 (R$ 32,385 bi), ano que `Sistema S.xlsx` não
  cobria.

## `ctb_resumo_*.csv` (2000-2015)

**Única exceção deliberada à regra de escopo do CLAUDE.md** ("`CTB-Resumo.xlsx` é
especificação e referência de comparação, nunca fonte de dados") — pedido explícito do
usuário em 2026-09-02: estender a série pra trás de 2016 **sem** recalcular pela
metodologia automatizada (que exigiria reconstruir o dicionário de classificação pra
pelo menos mais duas eras do plano de contas da DCA anteriores a 2016, trabalho não
solicitado). Em vez disso, os cinco quadros de 2000-2015 são extraídos direto de
`CTB-Resumo.xlsx` (fornecido pelo usuário no início do projeto), que já traz a série
2000-2024 pronta pela **metodologia antiga** — a mesma que os quadros de 2016-2025
substituíram (ver `docs/divergencias.md` §1 e `docs/revisao-metodologica.md`).

**Isso é uma fonte de dados fundamentalmente diferente das outras em `manual/`**: não é
um complemento a um cálculo já feito pelo dicionário (como FGTS/Sistema S), é a
**publicação inteira** de cada ano 2000-2015 — nenhum desses anos passa pelo
Siconfi/DCA nem pelo dicionário de classificação. `pipeline/dominio/publicar_legado.py`
lê estes CSVs e monta o mesmo formato JSON dos anos 2016+, mas marca
`"fonte_dados": "ctb_resumo_legado"` em vez de `"siconfi_dca"` — o site sinaliza a
diferença, não esconde.

**Consequência que aparece nos quadros**: a linha "Multas e Dívida Ativa" (União) e
"Demais (multas, juros e dívida ativa)" (Estados/Municípios) existem em 2000-2015 e
desaparecem em 2016 — não é erro, é a mudança de metodologia (decisão 1,
`docs/decisoes-pendentes.md`): o valor não some, é redistribuído nas rubricas de
origem a partir de 2016. Uma comparação de tributo por tributo atravessando essa
fronteira (aba Variação da Carga) vai mostrar esse degrau.

Extraído com um script pontual (não versionado, não faz parte do pipeline) que leu as
cinco abas de `CTB-Resumo.xlsx`
(`byGOVDetalhado`, `AD ESFERA`, `PRINCIPAIS TRIBUTOS`, `Bases de Incidência`,
`RD ESFERA`) e voltou os valores de R$ bilhões (como a planilha guarda) pra R$ reais.
Rótulos de rubrica só foram normalizados onde o conceito é exatamente o mesmo do
dicionário novo (remoção de nota de rodapé tipo "Previdência (1)" → "Previdência
Social"; "PATRIMONIAIS" → "Patrimônio" pra bater com a mesma decisão já tomada pro
rótulo de Bases de Incidência de 2016+) — nunca forçando equivalência que não existe
(as linhas de multas/dívida ativa ficam como estão, sem tentar redistribuir sem o
detalhe original que permitiria fazer isso direito).

- **`ctb_resumo_pib_populacao.csv`** — PIB e população 2000-2015, colunas `PIB` e
  `População` das próprias abas da planilha (mesmo valor em todas as cinco, só extraído
  uma vez).
- **`ctb_resumo_bygov_detalhado.csv`** — `ano;esfera;rubrica;valor_reais`, da aba
  `byGOVDetalhado` (34 rubricas: 18 União, 8 Estados, 8 Municípios).
- **`ctb_resumo_ad_esfera.csv`** — `ano;esfera;categoria;valor_reais`, da aba
  `AD ESFERA` (categorias agregadas: Impostos/Contribuições Sociais/Previdência
  Social/FGTS/Demais na União; ICMS/IPVA/Demais em Estados; ISS/IPTU/Demais em
  Municípios).
- **`ctb_resumo_principais_tributos.csv`** — `ano;tributo;valor_reais`, da aba
  `PRINCIPAIS TRIBUTOS`. Lista de tributos não é idêntica à de 2016+ (ex.: tem uma
  linha "FGTS" própria que a metodologia nova não replica nesse quadro) — mantida como
  a planilha original define, sem forçar paridade.
- **`ctb_resumo_bases_incidencia.csv`** — `ano;base_incidencia;valor_reais`, da aba
  `Bases de Incidência`, rótulos já normalizados pro mesmo Title Case de
  `dicionario/bases_incidencia.csv`.
- **`ctb_resumo_rd_esfera.csv`** — `ano;esfera;valor_reais`, totais de receita
  disponível por esfera, da aba `RD ESFERA`.
- **`ctb_resumo_rd_transferencias.csv`** — `ano;bloco_origem;bloco_destino;modalidade;
  valor_reais`, os três blocos de transferência (União→Estados, União→Municípios,
  Estados→Municípios) com detalhe por modalidade (FPE, FPM, FUNDEF/FUNDEB, Royalties
  etc.) da mesma aba `RD ESFERA`.

Conferido: soma de `ctb_resumo_bygov_detalhado.csv` bate exato, ano a ano, com a soma
de `ctb_resumo_rd_esfera.csv` (a AD e a RD têm que somar o mesmo total — é
redistribuição, não dinheiro novo) — testado em 2000, 2008 e 2015, diferença zero.
