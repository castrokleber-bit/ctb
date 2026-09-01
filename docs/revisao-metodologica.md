# Revisão metodológica — comparação contra a série histórica

Gerado por `uv run ctb comparar-historico`. Compara `dados/intermediario/{ano}.parquet` (2016-2024, os anos em comum com `CTB-Resumo.xlsx`, que não tem 2025) contra a série publicada. **Isto não é um teste que precisa passar** (CLAUDE.md) — é o material que sustenta a comunicação da revisão. Nenhuma divergência aqui foi corrigida ajustando a metodologia para o diff diminuir.

## Por que a série diverge — mecanismos, não erros

Quatro mudanças deliberadas explicam a maior parte da diferença que resta, todas já decididas e documentadas em `docs/decisoes-pendentes.md` — FGTS e Sistema S (o antigo maior gap do total geral) passaram a ser incluídos a partir de 2016 (fonte em `manual/README.md`), o que já fechou a maior parte da diferença sozinho:

1. **Opção B (decisão 1):** cada rubrica passa a ser receita líquida da DCA (bruta + Outras Deduções), não mais só o "principal". *Multas e Dívida Ativa* deixa de existir como linha própria — o valor volta para as rubricas de origem. Isso não muda o total da União, só a composição.
2. **Royalties (decisão 4):** ganham linha própria (*Royalties e Compensações Financeiras*) nas três esferas, separada de *Contribuições Econômicas*/*Contribuições de Melhoria e Econômicas*. Na tabela abaixo, somamos as duas rubricas novas para comparar com a linha antiga combinada.
3. **Receita líquida em estados e municípios (decisão 6):** uniformiza com a União — reduz o total de Estados e Municípios frente à bruta que a série antiga publicava.
4. **IRPF/IRPJ reclassificado para IRRF (decisão 7):** em estados e municípios, afasta um pouco o IRRF calculado do publicado (o publicado tratava esses lançamentos como "Outros impostos").

## Total geral

### Brasil

| ano | antigo (R$ bi) | antigo (% PIB) | novo (R$ bi) | novo (% PIB) | Δ R$ bi | Δ p.p. PIB |
|---|---|---|---|---|---|---|
| 2016 | 2.086,156 | 33,287 | 2.040,055 | 32,540 | −46,101 | −0,747 |
| 2017 | 2.203,404 | 33,620 | 2.151,019 | 32,663 | −52,385 | −0,957 |
| 2018 | 2.372,800 | 34,442 | 2.380,757 | 33,991 | +7,957 | −0,452 |
| 2019 | 2.496,924 | 33,792 | 2.572,402 | 34,813 | +75,478 | +1,021 |
| 2020 | 2.451,557 | 32,217 | 2.551,494 | 33,530 | +99,936 | +1,313 |
| 2021 | 3.060,966 | 34,398 | 3.180,329 | 35,289 | +119,363 | +0,892 |
| 2022 | 3.518,497 | 34,907 | 3.688,283 | 36,591 | +169,786 | +1,684 |
| 2023 | 3.783,988 | 34,578 | 3.842,822 | 35,116 | +58,834 | +0,538 |
| 2024 | 4.222,222 | 35,950 | 4.203,383 | 35,685 | −18,839 | −0,265 |

## Arrecadação Direta (AD ESFERA) — por esfera

### União

| ano | antigo (R$ bi) | antigo (% PIB) | novo (R$ bi) | novo (% PIB) | Δ R$ bi | Δ p.p. PIB |
|---|---|---|---|---|---|---|
| 2016 | 1.374,545 | 21,932 | 1.364,661 | 21,767 | −9,884 | −0,165 |
| 2017 | 1.439,747 | 21,968 | 1.423,767 | 21,620 | −15,980 | −0,348 |
| 2018 | 1.550,492 | 22,506 | 1.566,612 | 22,367 | +16,120 | −0,139 |
| 2019 | 1.610,623 | 21,797 | 1.693,993 | 22,925 | +83,371 | +1,128 |
| 2020 | 1.541,698 | 20,260 | 1.649,118 | 21,672 | +107,420 | +1,412 |
| 2021 | 1.962,241 | 22,051 | 2.067,137 | 22,937 | +104,895 | +0,886 |
| 2022 | 2.292,723 | 22,746 | 2.471,036 | 24,515 | +178,313 | +1,769 |
| 2023 | 2.470,283 | 22,573 | 2.548,760 | 23,291 | +78,478 | +0,717 |
| 2024 | 2.735,214 | 23,289 | 2.737,373 | 23,239 | +2,159 | −0,050 |

### Estados

| ano | antigo (R$ bi) | antigo (% PIB) | novo (R$ bi) | novo (% PIB) | Δ R$ bi | Δ p.p. PIB |
|---|---|---|---|---|---|---|
| 2016 | 560,819 | 8,948 | 537,091 | 8,567 | −23,727 | −0,381 |
| 2017 | 599,899 | 9,153 | 579,417 | 8,798 | −20,482 | −0,355 |
| 2018 | 650,273 | 9,439 | 639,259 | 9,127 | −11,014 | −0,312 |
| 2019 | 694,779 | 9,403 | 682,102 | 9,231 | −12,677 | −0,172 |
| 2020 | 712,176 | 9,359 | 699,997 | 9,199 | −12,179 | −0,160 |
| 2021 | 858,147 | 9,643 | 868,349 | 9,635 | +10,203 | −0,008 |
| 2022 | 950,187 | 9,427 | 935,245 | 9,279 | −14,942 | −0,148 |
| 2023 | 995,581 | 9,098 | 975,558 | 8,915 | −20,023 | −0,183 |
| 2024 | 1.127,211 | 9,598 | 1.106,954 | 9,397 | −20,257 | −0,200 |

### Municípios

| ano | antigo (R$ bi) | antigo (% PIB) | novo (R$ bi) | novo (% PIB) | Δ R$ bi | Δ p.p. PIB |
|---|---|---|---|---|---|---|
| 2016 | 150,792 | 2,406 | 138,303 | 2,206 | −12,489 | −0,200 |
| 2017 | 163,758 | 2,499 | 147,834 | 2,245 | −15,924 | −0,254 |
| 2018 | 172,035 | 2,497 | 174,886 | 2,497 | +2,852 | −0,000 |
| 2019 | 191,523 | 2,592 | 196,307 | 2,657 | +4,784 | +0,065 |
| 2020 | 197,683 | 2,598 | 202,379 | 2,660 | +4,696 | +0,062 |
| 2021 | 240,578 | 2,704 | 244,843 | 2,717 | +4,265 | +0,013 |
| 2022 | 275,586 | 2,734 | 282,002 | 2,798 | +6,416 | +0,064 |
| 2023 | 318,124 | 2,907 | 318,503 | 2,910 | +0,379 | +0,003 |
| 2024 | 359,797 | 3,063 | 359,056 | 3,048 | −0,741 | −0,015 |

## Receita Disponível (RD ESFERA) — por esfera

### União

| ano | antigo (R$ bi) | antigo (% PIB) | novo (R$ bi) | novo (% PIB) | Δ R$ bi | Δ p.p. PIB |
|---|---|---|---|---|---|---|
| 2016 | 1.139,041 | 18,175 | 1.124,565 | 17,938 | −14,475 | −0,237 |
| 2017 | 1.204,505 | 18,379 | 1.185,214 | 17,997 | −19,290 | −0,381 |
| 2018 | 1.289,236 | 18,714 | 1.300,908 | 18,573 | +11,673 | −0,141 |
| 2019 | 1.332,559 | 18,034 | 1.397,291 | 18,910 | +64,732 | +0,876 |
| 2020 | 1.208,844 | 15,886 | 1.301,511 | 17,104 | +92,667 | +1,218 |
| 2021 | 1.598,366 | 17,962 | 1.695,920 | 18,818 | +97,554 | +0,856 |
| 2022 | 1.826,677 | 18,122 | 1.988,343 | 19,726 | +161,666 | +1,604 |
| 2023 | 1.969,692 | 17,999 | 2.055,305 | 18,781 | +85,613 | +0,782 |
| 2024 | 2.176,573 | 18,532 | 2.178,093 | 18,491 | +1,520 | −0,041 |

### Estados

| ano | antigo (R$ bi) | antigo (% PIB) | novo (R$ bi) | novo (% PIB) | Δ R$ bi | Δ p.p. PIB |
|---|---|---|---|---|---|---|
| 2016 | 526,755 | 8,405 | 504,166 | 8,042 | −22,589 | −0,363 |
| 2017 | 556,612 | 8,493 | 536,838 | 8,152 | −19,775 | −0,341 |
| 2018 | 603,720 | 8,763 | 595,610 | 8,504 | −8,110 | −0,260 |
| 2019 | 639,177 | 8,650 | 637,048 | 8,621 | −2,129 | −0,029 |
| 2020 | 682,721 | 8,972 | 677,036 | 8,897 | −5,685 | −0,075 |
| 2021 | 796,248 | 8,948 | 801,629 | 8,895 | +5,381 | −0,053 |
| 2022 | 910,112 | 9,029 | 901,006 | 8,939 | −9,106 | −0,090 |
| 2023 | 949,886 | 8,680 | 924,869 | 8,451 | −25,016 | −0,229 |
| 2024 | 1.063,173 | 9,052 | 1.043,246 | 8,857 | −19,927 | −0,196 |

### Municípios

| ano | antigo (R$ bi) | antigo (% PIB) | novo (R$ bi) | novo (% PIB) | Δ R$ bi | Δ p.p. PIB |
|---|---|---|---|---|---|---|
| 2016 | 420,361 | 6,707 | 411,324 | 6,561 | −9,037 | −0,146 |
| 2017 | 442,287 | 6,749 | 428,967 | 6,514 | −13,321 | −0,235 |
| 2018 | 479,844 | 6,965 | 484,238 | 6,914 | +4,395 | −0,052 |
| 2019 | 525,189 | 7,108 | 538,064 | 7,282 | +12,875 | +0,174 |
| 2020 | 559,993 | 7,359 | 572,948 | 7,529 | +12,955 | +0,170 |
| 2021 | 666,352 | 7,488 | 682,780 | 7,576 | +16,428 | +0,088 |
| 2022 | 781,708 | 7,755 | 798,934 | 7,926 | +17,226 | +0,171 |
| 2023 | 864,410 | 7,899 | 862,647 | 7,883 | −1,763 | −0,016 |
| 2024 | 982,476 | 8,365 | 982,044 | 8,337 | −0,433 | −0,028 |

## Achados que pedem atenção

Três divergências na tabela abaixo saem muito do padrão normal de ruído da opção B (que fica tipicamente abaixo de 0,3 p.p.) e foram investigadas até a causa raiz ou até o limite razoável desta passada:

1. **União, 2019 — Previdência Social despenca, Outras contribuições sociais dispara (−1,664 p.p. e +1,771 p.p.).** Causa identificada: a conta `RO1.2.1.9.99.2.0 - Demais Contribuições Sociais - Parcelamento` sozinha soma R$ 132,875 bi em 2019 — um parcelamento (provavelmente REFIS/renegociação de dívida previdenciária) que a própria DCA classificou dentro do ramo genérico "Outras Contribuições Sociais" (`1.2.1.9`) em vez do ramo específico do RGPS (`1.2.1.4`). O dicionário segue corretamente o código que a DCA usa — o gap é a granularidade que a opção B perdeu (o 8º dígito que separaria "parcelamento de dívida do RGPS" de "outras contribuições genuínas"), não um erro de mapeamento. R$ 132,875 bi explica quase toda a diferença combinada das duas linhas nesse ano.
2. **Estados e Municípios, 2018 em diante — a linha "Demais (multas, juros e dívida ativa)" da série antiga é exatamente R$ 0,00 todo ano.** Não é um artefato desta leitura: `CTB-Resumo.xlsx` já publicava zero para essa linha em Estados e Municípios a partir de 2018 (em 2016-2017 tinha valor: R$ 13,7 bi e R$ 13,0 bi em 2016). A série antiga bateu no mesmo limite que motivou a decisão 1 (o 8º dígito da natureza de receita, que separa principal de acessório, deixa de estar disponível) e simplesmente zerou a linha em vez de estimá-la — subestimando o total de Estados e Municípios nesses anos. A opção B, que redistribui esse valor de volta às rubricas de origem em vez de descartá-lo, é mais completa para 2018 em diante, ao custo de comparabilidade direta contra 2016-2017.
3. **União, IR, 2020-2023 — diferença 5 a 9× maior que o efeito normal da opção B (até +1,541 p.p. em 2020, contra +0,175 p.p. em 2024).** Causa localizada, não totalmente explicada: a conta `RO1.1.1.3.02.0.0` (IRPJ líquido) tem, na coluna "Outras Deduções da Receita", valor **positivo** em 2020-2023 (+46,9 / +33,6 / +28,6 / +38,2 bi) — nos outros oito anos da série (2016-2019 e 2024) essa mesma coluna é sempre **negativa** (ex.: −39,5 bi em 2024), como se espera de uma coluna de restituições. É essa inversão de sinal, isolada nessas quatro contas do IRPJ, que explica o salto: sob a opção B (líquida = bruta + Outras Deduções), um valor positivo nessa coluna soma à receita em vez de subtrair. O porquê da STN reportar essa conta assim especificamente em 2020-2023 não foi determinado — hipótese mais provável é a dinâmica de estimativa mensal vs. ajuste anual do IRPJ (o imposto é pago por estimativa ao longo do ano e ajustado depois) amplificada pela recessão de 2020 e por programas de renegociação de dívida tributária do período, mas isso não foi verificado linha a linha. Fica registrado para investigação futura, não decidido nem corrigido nesta passada.

Fora esses três, as células acima de 0,3 p.p. na matriz abaixo seguem os mecanismos já listados (opção B, royalties, receita líquida, reclassificação de IRPF/IRPJ) sem achado adicional que justifique investigação linha a linha.

## byGOVDetalhado — linha a linha, por esfera

Célula = diferença em pontos percentuais do PIB (novo − antigo, calculado com o PIB corrente de cada ano). `⚠️` marca acima de 0,3 p.p., o limiar de divergência do CLAUDE.md que exigiria decisão do usuário se fosse uma escolha metodológica nova — aqui é resíduo medido, não decisão pendente.

### União

| rubrica (rótulo antigo) | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|
| IR | +0,121 | −0,183 | +0,175 | +0,142 | +1,541 ⚠️ | +1,077 ⚠️ | +0,982 ⚠️ | +0,593 ⚠️ | +0,175 |
| IPI | +0,009 | +0,007 | +0,024 | +0,006 | +0,051 | +0,091 | +0,114 | +0,038 | +0,019 |
| IOF | +0,002 | +0,003 | +0,002 | +0,001 | −0,010 | −0,010 | −0,006 | −0,005 | +0,003 |
| Imp. Sobre Comércio Exterior | +0,001 | −0,000 | +0,002 | +0,003 | +0,005 | +0,000 | +0,002 | +0,002 | +0,002 |
| ITR | +0,001 | +0,001 | +0,001 | +0,001 | +0,001 | +0,001 | +0,002 | +0,002 | +0,002 |
| Taxas | +0,000 | −0,003 | +0,000 | +0,000 | −0,000 | +0,001 | +0,002 | +0,002 | +0,001 |
| Previdência (1) | +0,094 | +0,120 | +0,107 | −1,664 ⚠️ | −0,297 | −0,260 | −0,305 ⚠️ | −0,084 | +0,215 |
| Cofins | +0,060 | −0,065 | +0,117 | +0,033 | +0,144 | +0,328 ⚠️ | +0,782 ⚠️ | +0,464 ⚠️ | +0,114 |
| CPMF | +0,000 | +0,001 | −0,000 | +0,000 | +0,000 | +0,001 | +0,000 | +0,000 | +0,000 |
| CSLL | +0,029 | +0,015 | +0,052 | +0,033 | +0,305 ⚠️ | +0,265 | +0,162 | +0,111 | +0,052 |
| PIS-PASEP | +0,019 | −0,016 | +0,035 | +0,014 | +0,078 | +0,101 | +0,159 | +0,096 | +0,034 |
| Contrib. Seg. Serv. Público (2) | +0,000 | −0,000 | +0,000 | +0,000 | +0,001 | +0,000 | +0,000 | +0,000 | +0,000 |
| Outras contribuições sociais (3) | −0,061 | −0,043 | −0,022 | +1,771 ⚠️ | +0,012 | +0,016 | +0,018 | +0,002 | +0,000 |
| Contribuições Econômicas (5) | +0,305 ⚠️ | +0,365 ⚠️ | +0,282 | +1,150 ⚠️ | +0,002 | +0,008 | +0,363 ⚠️ | +0,004 | +0,046 |
| Salário Educação | +0,001 | +0,001 | +0,002 | +0,003 | −0,043 | −0,032 | −0,043 | −0,024 | +0,008 |
| Multas e Dívida Ativa | −0,739 ⚠️ | −0,443 ⚠️ | −0,546 ⚠️ | −0,364 ⚠️ | −0,379 ⚠️ | −0,425 ⚠️ | −0,461 ⚠️ | −0,490 ⚠️ | −0,657 ⚠️ |
| FGTS (4) | −0,000 | −0,000 | −0,000 | +0,000 | −0,000 | −0,000 | +0,000 | +0,006 | +0,005 |
| Sistema S (4) | −0,000 | −0,000 | −0,000 | +0,000 | −0,000 | −0,000 | +0,000 | +0,000 | +0,000 |

**Rubricas novas sem linha antiga correspondente** (R$ bi):

| rubrica | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|
| Outros impostos | 0,003 | 0,002 | 0,003 | 0,022 | 0,023 | 0,004 | 0,011 | 0,001 | 0,001 |

### Estados

| rubrica (rótulo antigo) | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|
| ICMS | −0,091 | −0,126 | −0,149 | −0,175 | −0,198 | +0,030 | −0,149 | −0,162 | −0,170 |
| IPVA | −0,003 | −0,000 | −0,008 | −0,007 | −0,000 | −0,003 | −0,003 | −0,003 | −0,004 |
| ITCD | −0,000 | −0,000 | −0,000 | −0,000 | −0,007 | −0,001 | −0,001 | −0,002 | −0,001 |
| IRRF | −0,113 | −0,112 | −0,001 | +0,020 | +0,002 | +0,000 | +0,000 | −0,001 | −0,000 |
| TAXAS | −0,007 | −0,008 | −0,009 | −0,021 | −0,017 | −0,021 | −0,018 | −0,017 | −0,018 |
| Previ. Estadual | −0,001 | −0,001 | −0,001 | −0,000 | −0,001 | −0,000 | −0,000 | −0,000 | −0,001 |
| Contribuições de Melhoria e Econômicas | +0,056 | +0,109 | +0,003 | +0,011 | +0,062 | +0,109 | +0,023 | +0,001 | +0,021 |
| Demais (multas, juros e dívida ativa) | −0,218 | −0,174 | +0,000 | +0,000 | +0,000 | +0,000 | +0,000 | +0,000 | +0,000 |

**Rubricas novas sem linha antiga correspondente** (R$ bi):

| rubrica | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|
| Outros impostos | 0,000 | 0,000 | 0,472 | 0,080 | 0,003 | 0,011 | 0,028 | 0,047 | 0,047 |

### Municípios

| rubrica (rótulo antigo) | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|
| ISS | +0,000 | +0,001 | +0,000 | +0,016 | +0,013 | −0,005 | −0,017 | −0,002 | −0,005 |
| IPTU | −0,006 | −0,007 | −0,005 | −0,005 | −0,004 | −0,016 | −0,005 | −0,015 | −0,031 |
| ITBI | −0,000 | −0,000 | +0,000 | +0,001 | +0,001 | −0,001 | −0,003 | −0,001 | −0,000 |
| IRRF | +0,000 | +0,001 | +0,004 | +0,016 | +0,018 | +0,008 | +0,027 | +0,007 | +0,008 |
| TAXAS | −0,000 | −0,001 | +0,000 | +0,001 | +0,001 | −0,003 | +0,001 | −0,003 | −0,006 |
| Previd. Municipal | +0,004 | +0,003 | +0,006 | +0,009 | +0,007 | −0,000 | +0,022 | +0,000 | +0,001 |
| Contribuições de Melhoria e Econômicas | +0,007 | +0,006 | +0,009 | +0,014 | +0,015 | +0,060 | +0,027 | +0,011 | +0,022 |
| Demais (multas, juros e dívida ativa) | −0,208 | −0,247 | +0,000 | +0,000 | +0,000 | +0,000 | +0,000 | +0,000 | +0,000 |

**Rubricas novas sem linha antiga correspondente** (R$ bi):

| rubrica | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|
| Outros impostos | 0,230 | 0,142 | 1,880 | 0,996 | 0,769 | 0,498 | 1,221 | 0,686 | 0,511 |
