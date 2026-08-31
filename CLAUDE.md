# CLAUDE.md — Projeto CTB

## O que é este projeto

Reprodução automatizada de um cálculo próprio de carga tributária brasileira, hoje feito
em Excel. O produto final é uma página estática com cinco quadros e gráficos. Leia
`PROJETO-CTB.md` antes de qualquer tarefa — ele tem a arquitetura, as fontes, a regra de
imputação municipal e o roadmap por fases.

**Escopo: 2016 a 2025, todos os anos recalculados pela metodologia automatizada.** As
planilhas `CTB2024.xlsx` e `CTB-Resumo.xlsx` são especificação e referência de
comparação, nunca fonte de dados. Divergência contra os números publicados anteriormente
é esperada e aceita — ela precisa ser **medida e explicada**, não evitada.

Contexto institucional: os números são publicados por uma gerência de política econômica
e serão citados publicamente. Erro silencioso aqui custa credibilidade. Isso governa
todas as regras abaixo.

## Regras invioláveis

1. **Nenhum número é digitado no código.** Todo valor vem de API, de um CSV em `manual/`
   com fonte e data declaradas, ou de imputação explicitamente marcada. Se você precisar
   de um número que não tem, pare e pergunte — não estime, não use placeholder, não use
   zero.

2. **Falha alto, nunca silenciosa.** Ano faltando, ente faltando, natureza de receita não
   mapeada: erro explícito com mensagem que diz o que fazer. Nunca `fillna(0)`, nunca
   `try/except: pass`, nunca descartar linhas sem log.

3. **Natureza de receita não reconhecida vira erro, não vira "outros".** O dicionário é a
   fonte da verdade; resíduo é sinal de dicionário desatualizado.

4. **Todo valor imputado é rastreável.** Coluna `imputado` e `metodo_imputacao` em toda
   linha estimada. Um número imputado nunca se mistura a um declarado sem essa marca.

5. **Cache é sagrado.** Downloads vão para `dados/bruto/{fonte}/{ano}/`. Nunca refaça um
   download que já está em disco sem `--force`. As APIs do Tesouro são lentas e públicas.

6. **Mudança de lógica que altera número publicado é reportada explicitamente** na sua
   resposta, com o diff numérico — não enterrada no commit.

## Fontes

Todas as três esferas vêm do **Siconfi DCA**, mesmo endpoint:
`https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca`

- União: **`id_ente=1`** (o cadastro `/tt/entes` traz a União com `cod_ibge=1` e
  `esfera=U`; passar `id_ente=U` devolve HTTP 400 — `U` é o valor da esfera, não do
  identificador)
- Estados: código IBGE de 2 dígitos
- Municípios: código IBGE de 7 dígitos
- Distrito Federal: `id_ente=53`, esfera `D`. Brasília (`5300108`) existe no cadastro
  como município mas **nunca declara** — não há prefeitura. Excluir do universo
  municipal, senão a salvaguarda de município grande ausente dispara todo ano.

O parâmetro do anexo é `no_anexo=DCA-Anexo I-C`. A conta-raiz das receitas muda em 2019:
`TotalReceitas` até 2018, `ReceitasExcetoIntraOrcamentarias` de 2019 em diante. Ler só
uma das duas silencia 2016–2018.

Complementos: transferências constitucionais na **API do Tesouro** —
`https://apiapex.tesouro.gov.br/aria/v1/transferencias_constitucionais/custom/<endpoint>`
(decisão 5, `docs/decisoes-pendentes.md` §5). O segmento `/custom/` é obrigatório e não
está documentado publicamente — sem ele, 404; com o prefixo certo mas endpoint errado,
500 "Endpoint não encontrado". Endpoints: `transferencias` (catálogo, 18 modalidades,
inclui `codigo=12` para royalties de transferência), `estados`, `municipios`,
`por_estados`, `por_estado_municipio`. Sem paginação real e sem filtro efetivo por ano —
cada chamada devolve a série 1997–2026 inteira; filtrar no cliente. PIB e população no
SIDRA/IBGE (tabelas 1846 e 6579); FGTS (CEF) e Sistema S (RFB) só em `manual/`.

## Regras de classificação

**Decisão metodológica de 2026-08-30 (opção B de `docs/decisoes-pendentes.md` §1):** as
três esferas são classificadas pela **conta DCA de 7 níveis**, e o valor de cada rubrica
é a **receita líquida**:

```
valor(conta) = "Receitas Brutas Realizadas" ± "Outras Deduções da Receita"
```

**O sinal da operação muda por esfera — está em `dicionario/politica_colunas.csv`, não
no código.** Na União a coluna de deduções já vem assinada (restituições negativas):
soma. Em estados, DF e municípios ela vem como magnitude, sem sinal: subtrai (decisão 6,
`docs/decisoes-pendentes.md` §6, 2026-08-31 — antes disso estados e municípios usavam
receita bruta). `pipeline/dominio/dicionario.py` implementa três operações —
`somar`, `subtrair`, `ignorar` (FUNDEB e transferências constitucionais são repartição,
não redução de arrecadação: sempre `ignorar`).

Consequências que valem para todo o código:

- **Não existe linha "Multas e Dívida Ativa".** Multas, juros e dívida ativa ficam na
  rubrica de origem. Quem procurar essa linha nos quadros não vai achar — é intencional.
- **A regra do último dígito não se aplica.** O Anexo I-C agrega em 7 níveis
  (`1.1.1.3.03.1.0`) e o 8º dígito é sempre `0`. Nenhum código deve tentar ler tipo de
  lançamento da conta DCA.
- **O dicionário é chaveado por `cod_conta`** (`RO1.1.1.3.00.0.0`), não por natureza de
  8 dígitos. A árvore de contas é hierárquica: somar pai e filho conta duas vezes.
  Cada linha do dicionário declara se a conta é **folha de agregação** para a rubrica.
- A coluna `tipo_lancamento` do modelo de dados perde sentido para dados de API. Manter
  no schema apenas para linhas vindas de `manual/`, onde a fonte separa.
- **Royalties têm rubrica própria** — *Royalties e Compensações Financeiras*, ramo
  `RO1.3.4` (decisão 4). O resto do ramo patrimonial (`RO1.3.1` aluguéis, `RO1.3.2`
  valores mobiliários, `RO1.3.3` delegação de serviços, `RO1.3.5` patrimônio intangível,
  `RO1.3.6` cessão de direitos — majoritariamente loterias —, `RO1.3.9` demais) fica
  **fora do escopo de arrecadação** de propósito: não é carga tributária, nunca esteve
  nos quadros publicados. `RAMOS_ARRECADACAO` em `pipeline/dominio/dicionario.py`
  restringe o que entra no loop de classificação — contas fora dele nunca viram órfãs.
- **A COSIP do Distrito Federal vai para o bloco Municípios** (decisão 2), coerente com a
  COSIP municipal — assim como ISS, IPTU e ITBI do DF. O resto do DF (ICMS, IPVA, ITCD,
  IRRF, taxas, demais contribuições) fica no bloco Estados. A coluna `bloco` do
  dicionário de estados carrega essa regra; só o DF lança COSIP entre os 27 entes de
  esfera E/D — nenhum estado real tem essa competência (art. 149-A da CF).
- **IRPF e IRPJ lançados por estado ou município são reclassificados para IRRF**
  (decisão 7) — nenhuma das duas esferas tem competência para os dois primeiros
  impostos. Nos estados a evidência é inequívoca (IRRF zerado no mesmo ano); nos
  municípios é parcial, mas a mesma regra vale para as duas esferas por consistência.

O que a metodologia antiga fazia — publicar só o principal, com a linha *Multas e Dívida
Ativa* à parte e a exceção de Taxas — está preservado em `docs/divergencias.md` §1. É
conhecimento histórico: explica a série publicada até 2024 e sustenta a Fase 4. **Não é
mais a regra de cálculo.**

Prefixos úteis para leitura (a rubrica vem do dicionário, não daqui): `1.1.1.1` comércio
exterior · `1.1.1.2` patrimônio · `1.1.1.3` renda · `1.1.1.4` produção e circulação ·
`1.1.2` taxas · `1.2.1` contribuições sociais · `1.2.2` contribuições econômicas ·
`1.3` patrimoniais.

O dicionário tem `vigencia_inicio` / `vigencia_fim`. Ao processar 2016, aplique a versão
vigente em 2016 — nunca a de 2024. Lembre que a conta-raiz muda em 2019
(`TotalReceitas` → `ReceitasExcetoIntraOrcamentarias`).

**Três eras de plano de contas, e elas não coincidem entre esferas:**

| esfera | 2016–2017 | 2018–2021 | 2022–2025 |
|---|---|---|---|
| União | plano novo, 7 níveis, exceto contribuições sociais em `1.2.1.0.XX` até 2017 | `1.2.1.X.YY` a partir de 2018 | idem |
| Estados, DF e municípios | plano de **8 níveis** (`1.1.1.2.05.00.00`), com patrimônio e renda no mesmo ramo | tributos de estados e municípios em **`1.1.1.8`** | `1.1.1.2.5X` e `1.1.1.4.5X` |

Uma conta agregadora é a que tem **cauda de zeros**; um totalizador nunca é somado. Ver
`pipeline/dominio/dicionario.py`, que recusa dicionário com pai e filho mapeados ao mesmo
tempo e trata conta órfã como erro.

## Imputação municipal

Municípios sem DCA no ano são estimados pela **receita tributária per capita média da
faixa populacional**, calculada **por rubrica** (ISS, IPTU, ITBI, IRRF, taxas,
contribuições, COSIP) e nunca sobre o total agregado.

```
valor_imputado(mun, rubrica) = per_capita_medio(faixa_do_mun, rubrica) × populacao(mun)
```

Faixas em `dicionario/faixas_populacionais.csv` (parâmetro, não constante no código) —
**as 18 faixas oficiais do FPM Interior** (Decreto-Lei 1.881/1981, decisão 3,
`docs/decisoes-pendentes.md` §3), não um corte arbitrário. Duas faixas (129.049–142.632 e
142.633–156.216) têm menos de 30 declarantes no censo de 2024 — é onde a salvaguarda
abaixo dispara com mais frequência.

Salvaguardas obrigatórias, todas com efeito de parada ou aviso:

- Faixa com menos de 30 declarantes → avisa e usa faixa vizinha
- Município com mais de 500 mil habitantes ausente → **para e reporta**; não imputa
- Toda rodada produz relatório: nº de declarantes, % da população coberta, % da receita
  municipal imputada, por ano

## Convenções

- Python, `uv` para dependências, `polars` ou `pandas` (escolha uma e mantenha)
- Formato longo em todo o `intermediario/`; os quatro indicadores (R$ bi, % PIB,
  % total, per capita) são **calculados na publicação**, nunca armazenados
- Nomes de colunas em português, snake_case, alinhados ao vocabulário do Siconfi
  (`co_natureza`, `no_natureza`, `an_exercicio`, `id_ente`)
- Dicionários em CSV com `;` e UTF-8 BOM, para abrirem direto no Excel
- Commits em português, no imperativo

## Comandos

```bash
uv run ctb fontes testar                  # Fase 0 — diagnóstico de endpoints
uv run ctb fontes varrer-municipios --anos 2024   # censo dos 5.569 municípios (~15 min/ano)
uv run ctb dicionario validar --esfera U  # Fase 1 — estrutura, cobertura e reconciliação
uv run ctb ingerir --anos 2016-2025       # baixa e cacheia
uv run ctb calcular --anos 2016-2025      # imputa, aplica dicionário, agrega
uv run ctb cobertura                      # relatório de declarantes e imputação
uv run ctb publicar                       # gera dados/publicado/*.json
uv run pytest testes/invariantes          # somas fecham, sem natureza órfã
uv run ctb comparar-historico             # diff contra CTB-Resumo.xlsx (diagnóstico)
```

`comparar-historico` **não é um teste que precisa passar.** Ele alimenta
`docs/revisao-metodologica.md`, que é o documento que sustenta publicamente a mudança de
série. Nunca ajuste a metodologia para fazer o diff diminuir.

## O que perguntar em vez de decidir sozinho

- Qualquer escolha metodológica nova que mude um número publicado (as que já foram
  identificadas — tratamento de royalties, faixas populacionais, regra do Distrito
  Federal, receita bruta/líquida, reclassificação de IRPF/IRPJ, fonte de transferências,
  público/interno — já estão decididas em `docs/decisoes-pendentes.md`; não reabra
  nenhuma delas sem o usuário pedir)
- O que entra em "receita disponível" no quadro `RD ESFERA` — ainda não decidido
- Município grande ausente na DCA de algum ano
- Quebra de série que você não conseguiu explicar em 15 minutos
- Divergência contra a série antiga acima de 0,3 p.p. do PIB em qualquer ano

Nesses casos, apresente o trade-off com os números dos dois lados e espere a decisão.

`docs/decisoes-pendentes.md` tem o histórico completo de cada decisão já tomada — a
alternativa descartada, os números dos dois lados, e o efeito medido depois de
implementada. Leia antes de propor qualquer coisa que dependa delas.
