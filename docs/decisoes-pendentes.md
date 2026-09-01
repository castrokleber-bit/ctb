# Decisões pendentes

Itens que o `CLAUDE.md` reserva explicitamente para decisão humana: escolhas
metodológicas que mudam número publicado. Cada um traz os números dos dois lados.

Status em 2026-08-31: **todas as nove decisões foram tomadas.** As decisões 2, 4, 6 e
7 já estão implementadas nos dicionários e validadas contra o censo completo de 2024
(`uv run ctb dicionario validar`). A decisão 3 mudou de tabela (FPM em vez das faixas
originais propostas). A decisão 8 fixa o escopo de identidade visual da Fase 5. A decisão
5 foi **substituída** ao construir `RD ESFERA` (Fase 2): a API de transferências
constitucionais mostrou-se pouco confiável (filtro por transferência ignorado pelo
servidor, endpoint municipal sempre em timeout) e foi trocada por CKAN + FUNDEB da STN +
CSV do usuário + duas fórmulas internas — ver a nota no início da seção 5. Essa
construção revelou a decisão 9 (cota do ICMS × retenção do FUNDEB), decidida no mesmo
dia.

Denominador usado em todas as contas abaixo: PIB de 2024 = R$ 11.744,709 bi, o mesmo
da planilha `CTB2024.xlsx`.

---

## 1. ✅ **DECIDIDA em 2026-08-30: opção B** — de onde vem a separação principal × acessório da União?

> **Decisão:** adotar o conceito do Siconfi. Cada rubrica passa a ser publicada pela
> receita líquida da DCA (`bruta + Outras Deduções da Receita`). A linha
> *Multas e Dívida Ativa* **deixa de existir** e seus R$ 77,4 bi voltam para as rubricas
> de origem. A Fase 1 está destravada: o dicionário é chaveado por **conta DCA de 7
> níveis**, não por natureza de 8 dígitos.
>
> Consequências operacionais, todas já refletidas no `CLAUDE.md`:
> - A Regra 2 (último dígito → tipo) e a exceção de Taxas saem da metodologia. Passam a
>   ser conhecimento histórico, preservado em `docs/divergencias.md` §1 porque é o que
>   explica a série antiga.
> - O critério de aceite da Fase 1 muda: o alvo não é mais reproduzir `byGOVDetalhado`,
>   e sim reproduzir a coluna "com a opção B" da tabela abaixo.
> - As três esferas passam a vir da mesma fonte, com o mesmo plano de contas — que era a
>   vantagem metodológica citada na seção 4 do `PROJETO-CTB.md`.
> - A quebra contra a série publicada é material do `docs/revisao-metodologica.md`
>   (Fase 4). O texto abaixo é a base dele.

O registro do problema e das alternativas fica preservado:

**O problema.** O Siconfi DCA publica a natureza de receita em 7 níveis. O 8º dígito —
que separa principal (`1`) de multas e juros (`2`), dívida ativa (`3`) e demais
acessórios — não existe na API. A metodologia atual depende dele para duas coisas:
publicar IR, IPI, Cofins etc. **só com o principal**, e montar a linha
*Multas e Dívida Ativa*. Detalhes em `docs/divergencias.md` §2.

### Opção A — manter a metodologia atual ❌ *não escolhida*

Exige uma fonte de 8 dígitos para os dez anos. As candidatas mapeadas:

| fonte | automatizável? | risco |
|---|---|---|
| Portal da Transparência, `download-de-dados/receitas/{ano}` | sim, ZIP público por ano, ~2 MB | publica o detalhamento **por nome** (`"COFINS S/FATURAMENTO-NAO O"`), sem o código numérico. O casamento com o dicionário seria por texto, sujeito a renomeação silenciosa |
| Balanço Geral da União (STN) | não, publicação anual | é a fonte declarada na própria planilha; entraria em `manual/`, 10 arquivos, um por ano |

Nada muda nos números publicados. O custo é fragilidade (opção por nome) ou trabalho
manual recorrente (opção BGU).

### Opção B — adotar o conceito do Siconfi para a União ✅ *escolhida*

Publicar cada rubrica pela **receita líquida** da DCA (`bruta + Outras Deduções`), que
já vimos reproduzir o total da planilha ao centavo. Consequência: a linha
*Multas e Dívida Ativa* deixa de existir e seus R$ 77,4 bi voltam para as rubricas de
origem.

**O total da carga não muda.** Os acessórios já estão dentro dos R$ 4.222,222 bi
(35,950% do PIB); o que muda é a composição.

| rubrica | hoje (principal) | com a opção B | Δ R$ bi | Δ p.p. do PIB |
|---|---|---|---|---|
| Previdência (RGPS) | 611,642 | 636,975 | +25,333 | +0,216 |
| Imposto de Renda | 764,550 | 785,151 | +20,601 | +0,175 |
| Cofins | 353,793 | 367,242 | +13,449 | +0,114 |
| CSLL | 160,607 | 166,760 | +6,153 | +0,052 |
| PIS-PASEP | 99,843 | 103,824 | +3,981 | +0,034 |
| IPI | 82,174 | 84,373 | +2,199 | +0,019 |
| IOF | 67,402 | 67,748 | +0,346 | +0,003 |
| Comércio exterior | 77,507 | 77,762 | +0,255 | +0,002 |
| ITR | 3,246 | 3,493 | +0,247 | +0,002 |
| Taxas | 9,444 | 9,444 | 0,000 | 0,000 |
| demais rubricas da União | — | — | +4,860 | +0,041 |
| **Multas e Dívida Ativa** | **77,424** | **deixa de existir** | **−77,424** | **−0,659** |
| **TOTAL** | **4.222,222** | **4.222,222** | **0,000** | **0,000** |

Nenhuma rubrica isolada se move mais que 0,216 p.p. do PIB — abaixo do limiar de
0,3 p.p. do `CLAUDE.md`. Mas a **supressão de uma linha inteira do quadro**
(−0,659 p.p.) é mudança editorial, não técnica.

A favor da opção B: as três esferas passam a vir da mesma fonte, com o mesmo plano de
contas e o mesmo critério de consolidação — que é a vantagem metodológica citada na
seção 4 do `PROJETO-CTB.md`. Contra: perde-se uma informação que a série publica há
anos, e a comparabilidade com a série antiga por rubrica se rompe.

**O que precisa entrar na comunicação da revisão (Fase 4):** a carga total não muda, mas
*Multas e Dívida Ativa* some do quadro e nove rubricas sobem. Quem comparar a nova série
com a antiga linha a linha vai ver o IR subir R$ 20,6 bi sem que a arrecadação tenha
mudado. Isso precisa estar explicado **antes** da divulgação, não depois da pergunta.

---

## 2. Regra do Distrito Federal — ✅ **DECIDIDA em 2026-08-31: COSIP do DF vai para Municípios**

A pergunta era "qual é a lista exata de contas *tipicamente municipais* do DF?". A
decomposição do quadro `byGOVDetalhado` de 2024 responde sem ambiguidade:

| rubrica | bloco Municípios publicado | municípios | DF | fecha? |
|---|---|---|---|---|
| ISS | 142,634 | 139,146 | 3,488 | ✅ |
| IPTU | 77,634 | 76,299 | 1,335 | ✅ |
| ITBI | 25,103 | 24,481 | 0,621 | ✅ |
| IRRF | 48,839 | 48,839 | — | o IRRF do DF fica em Estados |
| TAXAS | 20,125 | 20,125 | — | idem |
| Previd. Municipal | 29,225 | 29,225 | — | idem |
| Contrib. de Melhoria e Econômicas | 16,237 | 16,237 | — | a COSIP do DF fica em Estados |

**A regra é: ISS, IPTU e ITBI do DF vão para o bloco Municípios; todo o resto do DF —
ICMS, IPVA, ITCD, IRRF, taxas, contribuições e COSIP — fica no bloco Estados.** As três
somas fecham na terceira casa decimal.

Está implementada na coluna `bloco` de `dicionario/contas_dca_estados.csv` e o validador
imprime a parcela que o DF envia ao bloco Municípios, para a regra ficar visível em vez
de embutida.

> **Decisão:** manter ISS, IPTU e ITBI do DF no bloco Municípios, e mandar também a
> **COSIP** para lá — mais coerente com o tratamento da COSIP municipal, que também é
> arrecadação tipicamente municipal. Todo o resto do DF (ICMS, IPVA, ITCD, IRRF, taxas e
> demais contribuições) permanece no bloco Estados.

Confirmado no censo completo de 2024: **só o Distrito Federal** lança a conta COSIP
(`RO1.2.4.0.00.0.0`) entre os 27 entes de esfera E/D — R$ 0,3225 bi, 100% do valor. Real
estado não tem competência de COSIP (art. 149-A da CF é privativo de município e DF), o
que confirma que a conta é seguramente roteável sem risco de arrastar dinheiro de outro
ente. O DF só passou a declarar COSIP a partir de 2019 (zero em 2016-2018).

Implementado na coluna `bloco` de `dicionario/contas_dca_estados.csv`
(`RO1.2.4.0.00.0.0` e sua antecessora `RO1.2.3.0.00.00.00`, plano de 2016-2017). O
validador confirma: bloco Estados fecha exato contra `byGOVDetalhado` de 2024
(diferença de R$ 0,323 bi, exatamente a COSIP redirecionada, dentro da tolerância
ampliada e documentada em `pipeline/dominio/validar.py`).

Detalhe de cadastro por trás disso: o DF aparece no Siconfi **duas vezes** — como ente de
esfera `D` (`cod_ibge=53`, quem entrega a DCA) e como município Brasília
(`cod_ibge=5300108`), que nunca entrega. O diagnóstico já exclui Brasília do universo
municipal, senão a salvaguarda de município grande ausente dispararia nos dez anos por
uma razão errada.

---

## 3. Faixas populacionais — ✅ **DECIDIDA em 2026-08-31: tabela do FPM**

> **Decisão:** abandonar as 8 faixas arbitrárias propostas originalmente e usar as
> **18 faixas oficiais do FPM Interior**, definidas pelo Decreto-Lei nº 1.881/1981 e
> reproduzidas na Tabela VII da *Cartilha FPM* da Secretaria do Tesouro Nacional
> (mar/2023): de "até 10.188 habitantes" a "acima de 156.216 habitantes". Fonte:
> https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/thot/arquivos/publicacoes/28549_909191/anexos/6370_978491/Cartilha%20FPM.pdf
> — não são números estimados nem arredondados por conveniência: são o corte legal que
> o próprio TCU usa para ratear o FPM todo ano.

Implementado em `dicionario/faixas_populacionais.csv`, com a fonte declarada em cada
linha (regra 1 do `CLAUDE.md` — nenhum número sem fonte).

**Checagem contra o censo completo de 2024** (5.569 municípios, excluída Brasília):
a salvaguarda de "faixa com menos de 30 declarantes" do `PROJETO-CTB.md` §5 dispara em
duas das dezoito faixas — as mais estreitas, que existem no meio da tabela porque o
espaçamento do Decreto-Lei não é uniforme:

| faixa | população | declarantes 2024 |
|---|---|---|
| 16 | 129.049–142.632 | 29 |
| 17 | 142.633–156.216 | 18 |

As demais dezesseis faixas têm entre 40 e 2.478 declarantes — folgadas. A regra
"avisa e usa faixa vizinha" do `CLAUDE.md` §5 se aplica a essas duas na Fase 3.

**Nota de dimensionamento**, agora com o censo completo (não mais amostra): a cobertura
municipal fica entre 97,7% (2016) e 99,9% (2021) ao ano — nunca abaixo de 98,4% em 2025.
**A imputação é marginal em toda a série.** Ver a tabela completa em
`PROJETO-CTB.md` §Fase 3.

**Observação para a Fase 3 (não muda esta decisão):** a faixa 18 ("acima de 156.216")
não tem teto — mistura uma cidade de 160 mil habitantes com São Paulo (12 milhões). Para
o FPM isso não importa (coeficiente único, 4,0, para todo mundo acima do corte), mas para
imputar receita per capita por média da faixa poderia distorcer, se algum município muito
grande estivesse ausente. Na prática isso não ocorre: nenhum município acima de 500 mil
habitantes falta em nenhum ano da série (Fase 0). As **capitais** também merecem nota:
o FPM as calcula por fórmula própria (fator população × fator renda per capita), fora da
tabela de faixas — se alguma capital precisar de imputação, a média da sua faixa
populacional pode não ser representativa, já que ela compete com municípios do interior
de porte parecido mas perfil arrecadatório muito diferente. Registrar como ponto de
atenção da Fase 3, não como decisão nova.

---

## 4. Royalties — ✅ **DECIDIDA em 2026-08-31: linha própria**

O `PROJETO-CTB.md` trata royalties como "entram ou não entram na carga tributária?".
A decomposição da planilha mostra que **já entram**, e há anos: a linha
*Contribuições Econômicas (4)* dos quadros não é só CIDE.

Composição da linha publicada de 2024 (R$ 138,966 bi, principal):

| origem na planilha | rótulo interno | R$ bi |
|---|---|---|
| aba `Contribuições` | CIDE | 18,988 |
| aba `Contribuições` | CIDE RURAL | 2,765 |
| aba `Contribuições` | OUTRAS CONTR. ECO. | 5,600 |
| aba `Contribuições` | TECNOL. INFO. TELEC. | 1,712 |
| aba `Contribuições` | OUTROS ROYALTIES | 1,389 |
| aba `Contribuições` | SELOS + JOGOS | 0,089 |
| **aba `Patrimoniais`** | **ROYALTIES PETROL. (concessão)** | **74,259** |
| **aba `Patrimoniais`** | **ROYALTIES PETROL. (partilha)** | **22,903** |
| **aba `Patrimoniais`** | **OUTROS ROYALTIES (minerais)** | **7,428** |
| **aba `Patrimoniais`** | **CONTRIB. ECON. (hídricos)** | **3,831** |
| | **soma** | **138,964** |

Ou seja: **R$ 108,4 bi dos R$ 139,0 bi da linha são royalties**, 78% dela. Na DCA eles
não estão em `1.2.2` (Contribuições Econômicas) e sim em `1.3.4` (Exploração de Recursos
Naturais) — por isso o dicionário atual fecha em R$ 34,403 bi contra os R$ 138,966
publicados. O gap de R$ 104,563 bi é inteiramente esse ramo.

> **Decisão:** linha própria, *Royalties e Compensações Financeiras*, separada de
> *Contribuições Econômicas*. Não muda o total nem a carga — só a leitura do quadro
> `byGOVDetalhado`. Torna explícito que a compensação por exploração de recursos naturais
> tem peso próprio, em vez de ficar escondida dentro de uma linha nomeada como CIDE.

**Implementado nas três esferas**, mapeando o ramo `RO1.3.4` (Exploração de Recursos
Naturais) da DCA — cada esfera com a sua própria conta agregadora
(`RO1.3.4.0.00.0.0`, mais `RO1.3.4.0.00.00.00` para o plano de contas de 2016-2017).
Confirmado que não há dupla contagem entre esferas: cada uma registra só a sua própria
cota de royalties como beneficiária, não o total nacional repassado por outra esfera.

**O que ficou de fora do ramo 1.3, deliberadamente:** `RO1.3.1` (aluguéis de imóveis do
governo), `RO1.3.2` (juros e dividendos de aplicações financeiras — R$ 108 bi só na
União em 2024, maior que os próprios royalties), `RO1.3.3` (delegação de serviços
públicos), `RO1.3.5` (patrimônio intangível) e `RO1.3.6` (cessão de direitos —
majoritariamente exploração de loterias) e `RO1.3.9` (demais). Nenhum desses é
compensação por exploração de recurso natural, nenhum esteve nos quadros publicados
historicamente, e por isso ficam **fora do escopo de arrecadação** — nem classificados,
nem tratados como órfãos (`RAMOS_ARRECADACAO` em `pipeline/dominio/dicionario.py`).

**Validação (censo completo de 2024):**

| esfera | calculado (líquida) | alvo | diferença |
|---|---|---|---|
| União | R$ 109,985 bi | R$ 108,445 bi (aba `Patrimoniais` do CTB2024.xlsx) | +R$ 1,540 bi |
| Estados+DF | R$ 4,451 bi (bruta) | — | sem alvo publicado à parte |
| Municípios | R$ 2,033 bi (bruta) | — | sem alvo publicado à parte |

O resíduo de R$ 1,54 bi na União é esperado e está dentro da tolerância ampliada
documentada no validador — provavelmente outorgas e bônus de assinatura que a planilha
histórica não incluía. Não é forçado a fechar.

**Efeito colateral que a separação revelou:** depois de tirar os royalties de
*Contribuições Econômicas*, sobra um resíduo de R$ 5,4 bi nessa linha (CIDE e afins) que
**já existia antes** e estava simplesmente encoberto pelo resíduo, cem vezes maior, dos
royalties. Registrado como item novo em `docs/divergencias.md` — não investigado ainda,
não é urgente (0,05% do PIB), mas é genuíno e fica para a Fase 2.

---

## 5. Fonte das transferências constitucionais — ⚠️ **SUBSTITUÍDA em 2026-08-31 ao construir RD ESFERA**

> **Atualização (Fase 2, construção de `RD ESFERA`):** a API abaixo tem dois problemas
> que só apareceram ao tentar realmente ingerir os dados — o parâmetro `transferencia`
> é ignorado pelo servidor (sempre devolve as 54.576 linhas inteiras) e o endpoint
> municipal (`por_estado_municipio`) estoura o timeout do próprio gateway do Tesouro
> (60s) mesmo sem filtro nenhum. `RD ESFERA` de 2024 foi construído sem essa API, usando:
> o CKAN `transferencias-obrigatorias-da-uniao` (FPE, FPM, ITR, IPI-Exp, IOF, CIDE,
> LC176 — 7 modalidades, validadas exatas contra a planilha antiga); a planilha oficial
> do FUNDEB da STN (`pipeline/fontes/fundeb.py`); dois CSVs fornecidos pelo usuário em
> `manual/` (royalties e demais compensações); e duas fórmulas calculadas internamente
> (ICMS/IPVA cota-parte municipal, Salário-Educação quota estadual). Ver
> `pipeline/dominio/rd_esfera.py` e a seção `RD ESFERA` de `docs/resultado-2024.md`. O
> registro abaixo (API de transferências constitucionais) fica preservado como histórico
> de investigação — não é mais a fonte usada.

> **Decisão original:** usar a API de Transferências Constitucionais do Tesouro Nacional
> (dataset CKAN `api-de-transferencias-constitucionais`), em vez do CSV mensal do CKAN
> mapeado na Fase 0.

**A rota documentada no `PROJETO-CTB.md` original estava quase certa — faltava um
segmento.** A URL correta é:

```
https://apiapex.tesouro.gov.br/aria/v1/transferencias_constitucionais/custom/<endpoint>
```

O `PROJETO-CTB.md` já apontava para `apiapex.tesouro.gov.br/aria/v1/`, e a Fase 0
descartou essa fonte porque `transferencias_constitucionais/` sozinho devolve 404. O que
faltava era o segmento `/custom/` antes do nome do endpoint — não documentado em lugar
nenhum público; só apareceu no PDF de metadados do dataset CKAN
(`metadados-apitransferenciasconstitucionais.pdf`, mapeamento de endpoints, página 2).

**Testado e funcionando** (2026-08-31):

| endpoint | retorna |
|---|---|
| `/custom/transferencias` | catálogo das 18 modalidades (FPM=3, FPE=7, Royalties=12, FUNDEB=10, …) |
| `/custom/estados` | 27 UFs com código interno |
| `/custom/municipios` | cadastro municipal, filtrável por `uf` |
| `/custom/por_estados` | série completa por estado, parâmetro `transferencia=<código>` |
| `/custom/por_estado_municipio` | idem, nível município |

Sem paginação e sem filtro efetivo por ano — cada chamada de `por_estados` devolve a
série inteira 1997–2026 para a transferência pedida (testado com FPM: 54.576 registros,
5,5 MB). O filtro por ano é feito no cliente, depois de baixar; o cache em
`dados/bruto/` torna isso indolor.

**O que resolve:** as transferências União→Estados e União→Municípios do quadro
`RD ESFERA`, incluindo especificamente os **royalties de transferência** (ANP, FEP, PEA,
Itaipu, CFH, CFEM — código 12 do catálogo), que são o outro lado da decisão 4.

**O que ainda não resolve:** o bloco Estados→Municípios (cota-parte do ICMS e do IPVA).
Essa API é só de transferências da União; a cota-parte estadual continua sem fonte
mapeada — permanece candidato deduzir da própria DCA (conta de transferências concedidas
pelo estado / recebidas pelo município), a verificar na Fase 2.

**Escopo desta decisão:** identifica e valida a fonte. Escrever o módulo de ingestão
(`pipeline/fontes/transferencias.py`) é trabalho de Fase 2, não feito agora.

---

## 6. Receita bruta ou líquida nos estados e municípios? ✅ **DECIDIDA em 2026-08-31: líquida, igual à União**

A opção B fixou a União em **receita líquida** (`bruta + Outras Deduções`). Nos estados
e municípios a coluna de deduções existe também — mas com **convenção de sinal
diferente**, o que só apareceu ao montar o dicionário:

| esfera | valores negativos em 2024 | valores positivos | soma |
|---|---|---|---|
| União | 68 | 40 | −R$ 268,808 bi |
| Estados | **0** | 49 | +R$ 88,543 bi |
| DF | **0** | 28 | +R$ 0,047 bi |
| Municípios (amostra) | **0** | 47 | +R$ 10,032 bi |

Na União a coluna vem assinada e somar produz a líquida. Nos estados e municípios ela
vem como magnitude: somar **inflaria** a receita, e netear exigiria subtrair.

A série publicada usa a **bruta** nos estados — IPVA, ITCD, IRRF e Taxas de 2024 batem
exatamente com a bruta, e nenhum deles bate com a líquida. É o que
`dicionario/politica_colunas.csv` faz hoje.

**O incômodo:** o argumento a favor da opção B foi "as três esferas passam a vir da
mesma fonte, com o mesmo critério de consolidação". Com União líquida e estados bruta,
o critério não é o mesmo.

**Atualizado com o censo completo de 2024** (antes era estimativa por amostra parcial):

| esfera | Outras Deduções | % da bruta | p.p. do PIB se netear |
|---|---|---|---|
| União (já líquida) | −77,040 | 3,10% | — |
| Estados e DF | +22,809 | 2,01% | −0,194 |
| Municípios | +4,642 | 1,31% | −0,040 |

Netear estados e municípios juntos custaria **0,234 p.p. do PIB** — abaixo do limiar de
0,3 p.p. do `CLAUDE.md`, mas ainda mudança de número publicado.

> **Decisão:** uniformizar. Estados, DF e municípios passam a subtrair a coluna
> `Outras Deduções da Receita` (ao contrário da União, que soma — a convenção de sinal é
> oposta). Implementado em `dicionario/politica_colunas.csv`. As três esferas voltam a
> ter o mesmo critério de consolidação, que era o argumento original a favor da opção B.

**Efeito medido no censo completo de 2024** (`uv run ctb dicionario validar`, bloco
"Efeito da decisão 6"):

| esfera | bruta | líquida | efeito | % do PIB |
|---|---|---|---|---|
| Estados (bloco) | R$ 1.131,401 bi | R$ 1.106,954 bi | −R$ 24,447 bi | −0,208 p.p. |
| Municípios (bloco) | R$ 363,350 bi | R$ 358,705 bi | −R$ 4,645 bi | −0,040 p.p. |

(O efeito por bloco inclui a parcela de royalties, R$ 1,641 bi em Estados — por isso é
um pouco maior que os R$ 22,809 bi + R$ 4,642 bi calculados antes só sobre o ramo
tributário 1.1+1.2, na primeira medição desta decisão.)

**A checagem estrutural do dicionário continua sendo feita pela receita bruta** — é o
que prova que as contas estão mapeadas certo, e é a comparação que ainda bate com
`byGOVDetalhado`. O validador mostra as duas: a estrutural (bruta, pass/fail) e a
efetivamente publicável (líquida, informativa). Ver `pipeline/dominio/validar.py`,
`_reconciliar_bloco`.

---

## 7. IRPF/IRPJ lançados por municípios: reclassificar ou não? ✅ **DECIDIDA em 2026-08-31: manter a reclassificação**

Nos **estados** a reclassificação de IRPF/IRPJ para IRRF é inequívoca: quatro casos, todos
com o IRRF zerado no mesmo ano — é deslocamento puro (`docs/divergencias.md` §6).

Nos **municípios** o padrão é misto. Em 2024, dos R$ 0,710 bi lançados em contas de
IRPF/IRPJ:

| situação | entes | R$ bi |
|---|---|---|
| lançou IRPF/IRPJ e tem IRRF zerado (deslocamento limpo) | 113 | 0,311 |
| lançou IRPF/IRPJ **e** IRRF no mesmo ano | 107 | 0,399 |

Foi reclassificado para IRRF, pelos mesmos dois motivos: município não tem competência de
IRPF nem de IRPJ, e aplicar regra diferente ao mesmo código conforme a esfera é pior de
sustentar publicamente.

**O custo é real e está no lado errado:** o IRRF municipal vai de 49,005 para **49,715**,
enquanto a linha publicada é 48,839. A reclassificação *afasta* o número da série antiga
em vez de aproximá-lo. Em p.p. do PIB são 0,006 — irrelevante para a carga, relevante para
quem comparar a linha.

A leitura conservadora — deixar em *Outros impostos* e assumir que não se sabe o que é —
é defensável. Trocar são duas linhas em `dicionario/contas_dca_municipios.csv`.

> **Decisão:** manter a reclassificação nas duas esferas, estados e municípios, já
> implementada. Já estava assim desde que a Fase 1 chegou nesta esfera; confirmada sem
> mudança.

O IRRF municipal calculado (bruta) fecha em R$ 49,715 bi para 2024 contra R$ 48,839 bi
publicado — diferença de +R$ 0,876 bi, composta pelos R$ 0,710 bi da reclassificação
mais um resíduo pré-existente de R$ 0,166 bi (já documentado, ver
`docs/divergencias.md` §5). Continua sinalizado como divergência no validador — não é
forçado a fechar.

---

## 8. Público ou interno — ✅ **DECIDIDA em 2026-08-31: público**

Pergunta 1 da seção 10 do `PROJETO-CTB.md`: a página é pública (site CNI) ou interna?

> **Decisão:** público. A Fase 5 (site) passa a ter como requisito identidade visual
> institucional adequada a publicação externa e aprovação editorial correspondente —
> não é mais um protótipo interno. Isso não muda nada do pipeline de dados nem das
> decisões 1 a 7; afeta só o escopo e os requisitos da Fase 5.

---

## 9. Cota-parte municipal do ICMS: bruta (25% flat) ou líquida do FUNDEB? — ✅ **DECIDIDA em 2026-08-31: líquida do FUNDEB**

Ao construir `RD ESFERA` (Fase 2), o usuário informou a regra: "ICMS transferido a
municípios = arrecadação estadual de ICMS × 25%" (art. 158, IV, CF). Aplicando isso à
arrecadação estadual de ICMS já calculada (R$ 808,157 bi, opção B), o resultado não bate
com o valor publicado em 2024:

| | fórmula (25% flat) | publicado 2024 | diferença | diferença em p.p. do PIB |
|---|---|---|---|---|
| ICMS (cota-parte municipal) | R$ 202,039 bi | R$ 161,083 bi | +R$ 40,956 bi | **+0,349 p.p.** |

Acima do limiar de 0,3 p.p. do `CLAUDE.md` — por isso fica registrado aqui em vez de
decidido sozinho.

**A mesma fórmula aplicada ao IPVA bate quase exato** (diferença de apenas R$ 0,240 bi,
−0,55%, dentro do ruído normal da opção B visto em outras rubricas — Salário-Educação
tem diferença parecida, +2,98%). Isso é o que torna o caso do ICMS interessante: não é
um erro de fórmula, é um comportamento diferente entre as duas cotas-partes.

**Hipótese testável:** a cota-parte do ICMS é uma das receitas sujeitas à retenção de
20% para o FUNDEB (art. 212-A, CF) — a União, ao repassar FPEx e Seguro-Receita ICMS aos
estados, não sofre essa retenção porque quem retém é quem recebe a parcela municipal
(o próprio município, ao receber sua cota do estado). Testando: R$ 808,157 bi × 25% ×
80% = **R$ 161,631 bi** — a R$ 0,548 bi (0,34%) do valor publicado, dentro do ruído
normal da opção B. O IPVA, por outro lado, não está na lista do art. 212-A sujeita a essa
retenção específica — o que explicaria por que ele bate flat.

**Duas outras linhas do bloco Estados→Municípios usam a mesma cota de 25% sem esse
ajuste e batem exatas:** FPEx (R$ 6,765 bi × 25% = R$ 1,691 bi, bate) e LC201/2023
(R$ 0,674 bi × 25% = R$ 0,169 bi, bate) — nenhuma das duas é, na prática, uma cota
"ICMS" per se para fins do art. 212-A, o que é consistente com a hipótese (a retenção
FUNDEB incidiria especificamente sobre a cota do ICMS, não sobre compensações tratadas
por analogia à mesma regra de repasse de 25%).

> **Decisão:** aplicar a retenção de 20% do FUNDEB à cota do ICMS antes do repasse —
> `25% × 80% = 20%` da arrecadação bruta, R$ 161,631 bi, que reproduz o valor publicado
> quase exato. Implementado em `pipeline/dominio/rd_esfera.py`
> (`RETENCAO_FUNDEB_ICMS_MUNICIPAL`); a linha aparece como "ICMS (cota-parte municipal,
> líq. FUNDEB)" em `docs/resultado-2024.md`. A cota do IPVA não recebe esse ajuste.
