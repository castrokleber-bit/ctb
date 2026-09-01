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
- **2025 não tem fonte ainda** — nem FGTS nem Sistema S. `manual_uniao.py` não inclui
  esse ano; o relatório de 2025 mostra o gap explicitamente em "O que falta".
