"""PIB corrente e população — SIDRA/IBGE.

Denominadores da publicação. Nenhum dos dois é armazenado como indicador — só como
insumo bruto (R$ correntes, pessoas), com a data de extração registrada. Revisão do PIB
pelo IBGE muda toda a série de % do PIB retroativamente; por isso `data_extracao_pib`
tem que acompanhar todo número derivado dele.
"""

from __future__ import annotations

from datetime import date, datetime

from pipeline.fontes.http import ErroFonte, obter_json

SIDRA = "https://apisidra.ibge.gov.br/values/"

TABELA_PIB = 1846
VARIAVEL_PIB = "585"  # Valores a preços correntes
CLASSIFICACAO_PIB = "c11255"
CATEGORIA_PIB = "90707"  # PIB a preços de mercado

TABELA_POPULACAO = 6579
VARIAVEL_POPULACAO = "9324"  # População residente estimada

# 2022 e 2023 não têm linha na tabela 6579 (ela pula direto de 2021 para 2024). Não é
# buraco de coleta: 2022 foi ano de Censo Demográfico (o IBGE não publica estimativa
# intercensitária no próprio ano do censo, só a contagem real), e o resultado do Censo
# 2022 só foi publicado no Diário Oficial em 30/08/2023 — tarde demais no ano para gerar
# uma estimativa 2023 nova, então o Censo 2022 seguiu sendo a referência oficial também
# em 2023 (mesma população dos dois anos, não é aproximação nossa). A contagem está na
# tabela 4709 ("População Residente, Variação absoluta..."), variável 93, período único
# 2022 — não é uma série contínua alternativa, por isso não substitui 6579 nos outros anos.
TABELA_CENSO_2022 = 4709
VARIAVEL_CENSO_2022 = "93"
ANOS_CENSO_SEM_ESTIMATIVA = (2022, 2023)


def _valores(resp: list) -> list[dict]:
    """A resposta do SIDRA é uma lista com o cabeçalho de rótulos no item 0."""
    if not resp or len(resp) < 2:
        raise ErroFonte(f"resposta do SIDRA vazia ou só com cabeçalho: {resp!r}")
    return resp[1:]


def pib_corrente(ano: int, *, forcar: bool = False) -> tuple[float, date]:
    """PIB a preços correntes do ano, em reais — soma dos 4 trimestres.

    Devolve `(valor_reais, data_extracao)`. Se algum trimestre faltar (ano corrente
    ainda em curso, por exemplo), falha — nunca soma parcial silenciosa.
    """
    consulta = (
        f"t/{TABELA_PIB}/n1/1/v/{VARIAVEL_PIB}/p/{ano}01-{ano}04/"
        f"{CLASSIFICACAO_PIB}/{CATEGORIA_PIB}"
    )
    resp = obter_json(
        SIDRA + consulta, fonte="sidra_pib", ano=ano, chave="pib_trimestral",
        forcar=forcar, timeout=120,
    )
    itens = _valores(resp.dados)
    trimestres = {i["D3C"]: i for i in itens}
    esperados = [f"{ano}01", f"{ano}02", f"{ano}03", f"{ano}04"]
    faltando = [t for t in esperados if t not in trimestres]
    if faltando:
        raise ErroFonte(
            f"PIB de {ano}: trimestre(s) ausente(s) no SIDRA: {faltando}. "
            "Ano provavelmente ainda em curso — não some parcial."
        )
    total_milhoes = sum(float(trimestres[t]["V"]) for t in esperados)
    return total_milhoes * 1_000_000, date.today()


def _resp_vazia(resp: list) -> bool:
    return not resp or len(resp) < 2


def populacao_municipios(ano: int, *, forcar: bool = False) -> dict[str, int]:
    """cod_ibge (string, 7 dígitos) -> população do ano (estimada, ou a contagem do
    Censo 2022 nos dois anos sem estimativa própria — ver `ANOS_CENSO_SEM_ESTIMATIVA`)."""
    consulta = f"t/{TABELA_POPULACAO}/n6/all/v/{VARIAVEL_POPULACAO}/p/{ano}"
    resp = obter_json(
        SIDRA + consulta, fonte="sidra_populacao_municipios", ano=ano,
        chave="populacao_municipios", forcar=forcar, timeout=180,
    )
    if _resp_vazia(resp.dados) and ano in ANOS_CENSO_SEM_ESTIMATIVA:
        print(f"  aviso: SIDRA não tem estimativa intercensitária (tabela {TABELA_POPULACAO}) "
              f"para {ano} — usando a contagem do Censo Demográfico 2022 (tabela "
              f"{TABELA_CENSO_2022}), a mesma referência oficial usada em 2022 e 2023.")
        consulta = f"t/{TABELA_CENSO_2022}/n6/all/v/{VARIAVEL_CENSO_2022}/p/2022"
        resp = obter_json(
            SIDRA + consulta, fonte="sidra_populacao_municipios", ano=ano,
            chave="populacao_municipios_censo", forcar=forcar, timeout=180,
        )
    itens = _valores(resp.dados)
    populacao = {}
    for i in itens:
        valor = i["V"]
        if valor in ("...", "-", "X", None):
            continue  # SIDRA usa esses códigos para "sem informação"
        populacao[i["D1C"]] = int(valor)
    if not populacao:
        raise ErroFonte(f"população municipal de {ano}: nenhum valor utilizável no SIDRA")
    return populacao


def populacao_brasil(ano: int, *, forcar: bool = False) -> int:
    consulta = f"t/{TABELA_POPULACAO}/n1/1/v/{VARIAVEL_POPULACAO}/p/{ano}"
    resp = obter_json(
        SIDRA + consulta, fonte="sidra_populacao_brasil", ano=ano,
        chave="populacao_brasil", forcar=forcar, timeout=60,
    )
    if _resp_vazia(resp.dados) and ano in ANOS_CENSO_SEM_ESTIMATIVA:
        consulta = f"t/{TABELA_CENSO_2022}/n1/1/v/{VARIAVEL_CENSO_2022}/p/2022"
        resp = obter_json(
            SIDRA + consulta, fonte="sidra_populacao_brasil", ano=ano,
            chave="populacao_brasil_censo", forcar=forcar, timeout=60,
        )
    itens = _valores(resp.dados)
    if len(itens) != 1:
        raise ErroFonte(f"população do Brasil em {ano}: resposta inesperada ({len(itens)} linhas)")
    return int(itens[0]["V"])
