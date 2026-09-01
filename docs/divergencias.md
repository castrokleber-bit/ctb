# Divergências conhecidas

Registro das diferenças entre o que a metodologia automatizada calcula e o que as
planilhas de referência publicam. Uma divergência só sai desta lista quando tem causa
identificada — nunca quando o número "melhora".

---

## 1. Taxas da União — R$ 0,083 bi ✅ **RESOLVIDA em 2026-08-30**

**Sintoma registrado no `CLAUDE.md`:** aplicando a Regra 2 (só o principal, último
dígito `1`) aos prefixos `1121` e `1122`, Taxas fecha em R$ 9,361 bi contra os
R$ 9,444 bi publicados em `byGOVDetalhado`. Seis das sete rubricas testadas batiam na
terceira casa; Taxas ficava R$ 0,083 bi abaixo.

**Causa:** a linha *Taxas* é a **única exceção à Regra 2**. Ela é publicada com
`principal + acessórios`, enquanto todas as demais rubricas (IR, IPI, IOF, comércio
exterior, ITR, Cofins…) usam apenas o principal.

Decomposição dos microdados de 2024 (abas `Impostos`/`Contribuições` do `CTB2024.xlsx`):

| natureza | tipo | R$ bi |
|---|---|---|
| `1121...1` | principal | 7,9074 |
| `1121...2` | multas e juros | 0,0021 |
| `1121...3` | dívida ativa | 0,0787 |
| `1121...4` | multas e juros da DA | 0,0002 |
| `1122...1` | principal | 1,4532 |
| `1122...2` | multas e juros | 0,0000 |
| `1122...3` | dívida ativa | 0,0018 |
| `1122...4` | multas e juros da DA | 0,0003 |

| agregação | R$ bi |
|---|---|
| só principal (`...1`) | 9,3607 |
| principal + acessórios | **9,4437** |
| publicado em `byGOVDetalhado` | **9,4437** |

A diferença é **zero na quarta casa decimal**. Os R$ 0,083 bi são exatamente os
acessórios de taxas (0,0021 + 0,0787 + 0,0002 + 0,0000 + 0,0018 + 0,0003 = 0,0830).

**Confirmação cruzada pela linha *Multas e Dívida Ativa*:** se os acessórios de taxas
ficam na linha Taxas, eles não podem estar também em Multas e Dívida Ativa. E não estão:

| | R$ bi |
|---|---|
| soma de **todos** os acessórios de 2024 (`...2`,`3`,`4`,`5`,`6`,`7`,`8`) | 77,507 |
| menos os acessórios de taxas | −0,083 |
| = | **77,424** |
| publicado em `byGOVDetalhado` na linha *Multas e Dívida Ativa* | **77,424** |

As duas anomalias são a mesma regra vista de dois lados, e ambas fecham exato.

**Consequência para o dicionário:** a Regra 2 precisa de uma coluna de exceção por
rubrica, não de um `if` no código. Rubricas com `acessorios_na_propria_linha = true`
(hoje: apenas Taxas) retêm seus acessórios; as demais os enviam para *Multas e Dívida
Ativa*. Com isso, a classificação da União passa a ser **100% reproduzível por regra**
— não resta nenhuma rubrica ad hoc em 2024.

**Pendente:** confirmar se a exceção vale para 2016–2023 ou se é prática recente. Isso
só pode ser testado quando houver fonte de 8 dígitos para os anos anteriores (ver
divergência 2).

---

## 2. Separação principal × acessório não existe no Siconfi ✅ **decisão tomada em 2026-08-30 — opção B**

> Este item deixou de bloquear qualquer coisa. A decisão 1 de `docs/decisoes-pendentes.md`
> resolveu adotando o conceito do Siconfi (receita líquida, sem a distinção principal ×
> acessório). O registro abaixo fica como histórico: por que a fonte de 8 dígitos não
> existe, e o que foi investigado antes da decisão.

**Sintoma:** o Anexo I-C da DCA publica a natureza de receita em **7 níveis**
(`1.1.1.3.03.1.0`); o 8º dígito — o que distingue principal (`1`) de multas e juros
(`2`), dívida ativa (`3`) e demais acessórios — é sempre `0`. Verificado nas 746 contas
da União em 2024: nenhuma exceção.

**O que o Siconfi resolve, e resolve bem:** o *total* por rubrica. Somando
`Receitas Brutas Realizadas + Outras Deduções da Receita`, a DCA reproduz **ao centavo**
o total da planilha em 10 das 11 rubricas testadas para 2024 (a 11ª é Taxas, pela regra
da divergência 1). A diferença entre as duas fontes não é de cobertura — é de conceito:
a planilha publica o principal, a DCA publica bruto e dedução.

**O que o Siconfi não resolve:** os R$ 77,4 bi da linha *Multas e Dívida Ativa*, e o
fato de IR, IPI, Cofins etc. serem publicados **só com o principal**. Sem o 8º dígito,
nenhum dos dois é reproduzível.

**Fontes de 8 dígitos investigadas:**

| fonte | veredito |
|---|---|
| Siconfi DCA Anexo I-C | ❌ agrega em 7 níveis |
| Portal da Transparência, `download-de-dados/receitas/{ano}` | ⚠️ tem o detalhamento por nome (`"COFINS S/FATURAMENTO-NAO O"`), no formato das abas de microdado da planilha, mas **não publica o código numérico** — o casamento teria de ser por texto |
| CKAN `receita-orcamentaria-da-uniao` | ❌ agregado por categoria econômica, série anual desde 1980 |
| Balanço Geral da União (STN) | fonte declarada na própria planilha; publicação anual, sem API |

**Decisão tomada:** ver `docs/decisoes-pendentes.md` §1.

---

## 3. Quebra de layout da DCA em 2019 ⚠️ **ABERTA — tratável**

Até 2018 o Anexo I-C tem conta-raiz `TotalReceitas` e ~345 linhas; de 2019 em diante é
`ReceitasExcetoIntraOrcamentarias`, com o dobro de linhas e a separação
intra/extraorçamentária. O pipeline precisa reconhecer as duas raízes. Usar só uma
silenciaria 2016–2018 — que é exatamente o tipo de erro que a Regra 2 do `CLAUDE.md`
proíbe.

---

## 6. Contas lançadas em rubrica sem competência do ente ✅ **RESOLVIDA em 2026-08-31**

A checagem de continuidade da série (`uv run ctb dicionario validar`) acusou uma rubrica
*Outros impostos* estadual oscilando sem sentido: R$ 3,1 bi em 2018, R$ 2,5 bi em 2019,
R$ 1,5 bi em 2023, quase zero nos demais anos. Investigando conta a conta e ente a ente,
eram tributos lançados em contas de competência que o ente não tem.

**Caso 1 — IRPF e IRPJ lançados por estados.** Estado não arrecada IRPF nem IRPJ; só
retém IRRF sobre a própria folha. O teste decisivo é se o ente que lança IRPF tem o IRRF
zerado:

| ano | ente | IRPF (`1.1.1.3.01`) | IRRF (`1.1.1.3.03`) |
|---|---|---|---|
| 2019 | Goiás | 2,074 | 0,009 |
| 2019 | Acre | 0,372 | 0,000 |
| 2023 | Paraíba | 0,930 | 0,000 |
| 2023 | Roraima | 0,499 | 0,000 |

**Quatro deslocamentos, zero convivências** em 2018–2025: o IRRF inteiro foi lançado na
conta errada. Reclassificado para IRRF, com o `tributo` registrando a procedência.

**Caso 2 — ICMS lançado como IVVC pelo Ceará em 2018.** O imposto sobre vendas a varejo
de combustíveis está extinto desde 1996, e havia R$ 2,595 bi nessa conta. A série de ICMS
do Ceará mostra o buraco:

| 2016 | 2017 | **2018** | 2019 | 2020 |
|---|---|---|---|---|
| 10,342 | 11,193 | **9,385** | 13,155 | 13,229 |

ICMS + IVVC em 2018 = **11,979**, exatamente entre 11,193 e 13,155. Reclassificado para
ICMS.

**Efeito na série estadual:** ICMS 2018 de 491,6 para 494,2 · IRRF 2019 de 44,3 para 46,8
e 2023 de 71,9 para 73,3 · *Outros impostos* de 3,1 para 0,5 em 2018, virando o resíduo
que deveria ser. A reconciliação de 2024 continua exata.

**Nos municípios a mesma reclassificação é mais fraca.** Em 2024, dos R$ 0,710 bi em
contas de IRPF/IRPJ municipais, 113 entes mostram deslocamento limpo (R$ 0,311 bi) e 107
lançam IRPF *e* IRRF ao mesmo tempo (R$ 0,399 bi). Reclassificou-se assim mesmo, porque
município também não tem competência de IRPF, e aplicar regra diferente ao mesmo código
em esferas diferentes é pior de defender. **Isso move o IRRF municipal de 49,005 para
49,715**, afastando-o da linha publicada (48,839) em vez de aproximá-lo. Custo: 0,006 p.p.
do PIB. Se preferir a leitura conservadora, é uma linha de CSV — ver
`docs/decisoes-pendentes.md`.

### O que sobrou em *Outros impostos* municipal, e um risco a investigar na Fase 2

Depois das reclassificações, a rubrica ficou entre R$ 0,1 e R$ 1,9 bi ao ano, difusa entre
milhares de prefeituras (maior lançamento individual: R$ 0,13 bi). Dois componentes
merecem nota:

- **ITR de municípios conveniados** (`1.1.1.2.01`, R$ 0,39–0,42 bi/ano) **não é erro.** O
  município arrecada o ITR por convênio com a União e fica com o produto, então não há
  dupla contagem contra o ITR federal — que vem da DCA da União, onde essa parcela não
  entra.
- **ICMS lançado por município** (`1.1.1.8.02.1.0`, R$ 1,09 bi em 2018) **é suspeito de
  dupla contagem.** A cota-parte do ICMS é transferência corrente (ramo `1.7`), não receita
  própria. Se parte desses lançamentos for cota-parte mal classificada, ela já está contada
  no ICMS estadual e voltaria a ser contada como arrecadação municipal. O valor é pequeno
  e está isolado numa rubrica visível, mas precisa de checagem cruzada contra o bloco de
  transferências na Fase 2.

---

## 5. A DCA municipal é retificada depois da entrega ⚠️ **ABERTA — provavelmente não tem conserto**

Com o censo completo de 2024 (5.569 municípios, extraído em 2026-08-30) o dicionário
municipal reproduz o quadro publicado quase inteiro, mas três rubricas ficam fora da
tolerância de R$ 0,1 bi:

| rubrica | dicionário | publicado | diferença | leitura |
|---|---|---|---|---|
| ISS | 142,632 | 142,634 | −0,002 | ✅ |
| ITBI | 25,187 | 25,103 | +0,084 | ✅ |
| Previd. Municipal | 29,301 | 29,225 | +0,076 | ✅ |
| TAXAS | 20,165 | 20,125 | +0,040 | ✅ |
| Contribuições de Melhoria e Econômicas | 16,847 | 16,237 | +0,610 | ✅ explicada — ver nota |
| IRRF | 49,715 | 48,839 | +0,876 | ⚠️ ver decisão 7 |
| IPTU | 76,957 | 77,634 | −0,678 | ⚠️ |

Atualizado em 2026-08-31 depois de duas decisões que mudaram os números desta tabela:
o IRRF subiu (49,005 → 49,715) porque a decisão 7 confirmou a reclassificação de
IRPF/IRPJ lançados por município; e Contribuições de Melhoria e Econômicas subiu
(16,525 → 16,847) porque a decisão 2 rerroteou a COSIP do DF (R$ 0,323 bi) para este
bloco. As duas ficaram maiores, não menores — nenhuma decisão foi tomada para "melhorar"
o número.

**Contribuições de Melhoria e Econômicas** está explicada: R$ 0,256 bi dos R$ 0,288 bi
são contribuições econômicas municipais (ramo `1.2.2`), que a aba `Municipios` da
planilha traz zeradas na coluna `CON. ECONOMICAS`. A planilha simplesmente não capturou
esse ramo. O resto (R$ 0,032 bi) é COSIP.

**IPTU e IRRF não têm explicação estrutural.** O ramo de patrimônio fecha exato na
decomposição — ITR 0,064 + IPTU 75,622 + IPVA 0,001 + ITCD 0,029 + ITBI 24,566 = 100,282,
que é o total do ramo `1.1.1.2`. Não há IPTU escondido em outra conta, e o censo está
completo, então também não é cobertura.

A causa provável é que **a fonte mudou**: os entes retificam a DCA depois da entrega, e a
extração que alimentou a planilha é anterior à nossa. Uma revisão de 0,9% no IPTU
municipal agregado é plenamente compatível com isso.

**Consequência de projeto:** o modelo de dados precisa de `data_extracao` por ente e ano,
não só `data_extracao_pib`. Hoje ela é inferida da data de modificação do arquivo em
`dados/bruto/`, e o validador a reporta. Sem esse carimbo, um número publicado não é
reproduzível: rodar o pipeline seis meses depois dá outro resultado, e não há como
distinguir isso de um bug.

**Não ajuste o dicionário para fechar esta diferença.** Ela é medida e explicada, que é o
que o `CLAUDE.md` pede — forçar o encaixe esconderia a mutabilidade da fonte, que é
informação relevante para uma publicação institucional.

---

## 7. Resíduo de R$ 5,4 bi em Contribuições Econômicas da União, revelado pela decisão 4 ⚠️ **ABERTA — não urgente**

Antes da decisão 4, o resíduo entre *Contribuições Econômicas* calculada e publicada era
R$ 104,563 bi — quase todo ele royalties classificados na linha errada (ver decisão 4).
Tirando os royalties da conta, sobra um resíduo menor mas genuíno:

| | R$ bi |
|---|---|
| calculado (CIDE e afins, ramo `1.2.2`) | 34,403 |
| publicado (`Contribuições Econômicas` menos os royalties calculados) | 28,981 |
| diferença | **+5,422** |

Isto **não é efeito de nenhuma decisão tomada** — é um resíduo que já existia em 2024,
só que invisível, encoberto pelo resíduo cem vezes maior dos royalties. Equivale a
0,046% do PIB: pequeno, mas não nulo, e sem causa identificada ainda.

**Não investigado.** Candidatos a checar na Fase 2: contas do ramo `1.2.2` com vigência
recente que o dicionário ainda não cobre (o ramo tem naturezas que só passaram a existir
em 2022, como `1.2.2.1.13` — adicional à contribuição previdenciária sobre a folha), ou
alguma conta de CIDE-combustíveis fora do padrão. Fica registrado aqui para não ser
esquecido, não para ser forçado a fechar.

---

## 4. Rota de transferências constitucionais do `PROJETO-CTB.md` está errada ✅ **RESOLVIDA em 2026-08-31**

**Sintoma:** `https://apiapex.tesouro.gov.br/aria/v1/transferencias_constitucionais/` e
variantes retornam 404. O host responde (devolve JSON de erro do Spring), então a rota
estava errada, não o serviço indisponível.

**Causa:** faltava o segmento `/custom/` antes do nome do endpoint. A rota correta é:

```
https://apiapex.tesouro.gov.br/aria/v1/transferencias_constitucionais/custom/<endpoint>
```

Testado e devolvendo 200 em 2026-08-31: `/custom/transferencias` (catálogo de 18
modalidades), `/custom/estados`, `/custom/municipios`, `/custom/por_estados`,
`/custom/por_estado_municipio`. Sem esse segmento, o roteador Aria devolve 404; com o
segmento errado mas o prefixo certo (`.../transferencias-constitucionais/custom/...`,
hífen em vez de underscore), devolve 500 com mensagem "Endpoint não encontrado" — foi
esse 500, e não mais um 404, que indicou que o prefixo estava quase certo.

O segmento `/custom/` não está documentado em nenhuma página pública — só aparece no PDF
de metadados do dataset CKAN `api-de-transferencias-constitucionais`
(`metadados-apitransferenciasconstitucionais.pdf`), na tabela "Mapeamento de Endpoints e
Rotas de Acesso".

Decisão de uso e detalhes de parâmetros em `docs/decisoes-pendentes.md` §5. O bloco
**Estados→Municípios** (cota-parte do ICMS e do IPVA) continua sem fonte — essa API é só
de transferências da União.

---

## 8. União, 2019 — Previdência Social e Outras contribuições sociais trocam ±1,7 p.p. do PIB ✅ **RESOLVIDA em 2026-09-01**

**Sintoma**, achado pela Fase 4 (`uv run ctb comparar-historico`): comparando contra
`CTB-Resumo.xlsx`, 2019 é o único ano em que *Previdência Social* despenca
(−1,664 p.p. do PIB) e *Outras contribuições sociais* dispara (+1,771 p.p.) — nenhum
outro ano da série tem esses dois saltos.

**Causa:** a conta `RO1.2.1.9.99.2.0 - Demais Contribuições Sociais - Parcelamento`
sozinha soma **R$ 132,875 bi** em 2019 (contra valores residuais em outros anos) —
provavelmente um parcelamento (tipo REFIS) de dívida previdenciária. A DCA classifica
essa conta no ramo genérico `1.2.1.9` ("Outras Contribuições Sociais"), não no ramo
específico do RGPS (`1.2.1.4`) — o dicionário segue o código corretamente; o gap é a
granularidade que a opção B perdeu (o 8º dígito separaria "parcelamento de dívida do
RGPS" de "outras contribuições genuínas", mas não está disponível na DCA de 7 níveis).

R$ 132,875 bi explica quase toda a diferença combinada das duas linhas nesse ano —
não é erro de mapeamento, é um evento real de 2019 caindo numa conta genérica.

---

## 9. Estados e Municípios — "Demais (multas, juros e dívida ativa)" já era zero na série antiga desde 2018 ✅ **RESOLVIDA em 2026-09-01**

**Sintoma**, achado pela Fase 4: a linha antiga *Demais (multas, juros e dívida ativa)*
de Estados e Municípios tem valor em 2016-2017 (R$ 13,7 bi e R$ 13,0 bi em 2016) e depois
é **exatamente R$ 0,00 todo ano, de 2018 a 2024** — não some gradualmente, cai a zero de
uma vez.

**Causa:** a série antiga bateu no mesmo limite que motivou a decisão 1 — o 8º dígito da
natureza de receita (que separa principal de multas/dívida ativa) deixou de estar
disponível na fonte que ela usava a partir de 2018, e ela zerou a linha em vez de
estimá-la, **subestimando o total de Estados e Municípios** nesses anos (não é um efeito
pequeno: R$ 13-16 bi/ano ao câmbio de 2016-2017, provavelmente mais em anos recentes).
A opção B, que redistribui esse valor de volta às rubricas de origem em vez de
descartá-lo, é mais completa para 2018 em diante — ao custo de perder comparabilidade
direta contra 2016-2017, onde a série antiga ainda tinha o dado.

---

## 10. União, IR, 2020-2023 — diferença 5-9× maior que o efeito normal da opção B ⚠️ **ABERTA — causa localizada, raiz não confirmada**

**Sintoma**, achado pela Fase 4: o IR diverge da série antiga em +0,175 p.p. do PIB em
2024 (o efeito esperado da opção B, conforme a decisão 1) mas **entre +0,593 e
+1,541 p.p. em 2020-2023** — 5 a 9 vezes maior.

**Causa localizada (2026-09-01):** a conta `RO1.1.1.3.02.0.0` ("Imposto sobre a Renda de
Pessoa Jurídica - IRPJ - Líquido") tem, na coluna "Outras Deduções da Receita", valor
**positivo** especificamente em 2020-2023 (+46,9 / +33,6 / +28,6 / +38,2 bi) — em todos
os outros oito anos da série (2016-2019 e 2024) essa mesma coluna, para essa mesma
conta, é **sempre negativa** (ex.: −33,8 bi em 2019, −39,5 bi em 2024), como se espera de
uma coluna de restituições/deduções. É essa inversão de sinal isolada no IRPJ, em
exatamente quatro anos, que a opção B (líquida = bruta + Outras Deduções) transforma em
receita adicional em vez de dedução.

**Raiz ainda não confirmada.** Hipótese mais provável: a dinâmica de estimativa mensal
vs. ajuste anual do IRPJ (pago por estimativa ao longo do ano, ajustado depois pela ECF)
amplificada pela recessão de 2020 e por programas de renegociação de dívida tributária do
período (Lei 13.988/2020, transação tributária da PGFN) — mas isso não foi verificado
conta a conta como o item 8. Fica aberta para investigação futura antes da divulgação
pública da série revisada.
