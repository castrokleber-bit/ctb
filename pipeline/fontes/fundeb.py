"""FUNDEB — planilha oficial da STN com o total distribuído a Estados/DF e a
Municípios, já separado por origem (União vs. Estados).

Fonte: publicação "Transferências ao Fundo de Manutenção e Desenvolvimento da Educação
Básica (FUNDEB)" do Tesouro Transparente
(https://www.tesourotransparente.gov.br/publicacoes/transferencias-ao-fundo-de-
manutencao-e-desenvolvimento-da-educacao-basica-fundeb/{ano}/114), arquivo .xls legado
(formato OLE2/BIFF — usa `xlrd`, não `openpyxl`). Publicação por ano; a URL de download
(`thot-arquivos.tesouro.gov.br/publicacao/N`) muda a cada ano e foi obtida navegando a
página de cada ano (2016-2025) em 2026-08-31/2026-09-01 — ver `URLS_POR_ANO`. 2022 é a
exceção: a página fica em `.../2022/114-2`, não `.../2022/114` (só afeta a navegação
manual, o download em si já está mapeado).

A planilha tem, para Estados e para Municípios, três abas relevantes:
- `{E,M}_TOTAL`: total anual distribuído (líquido, já com a redistribuição nacional).
- `{E,M}_Tot1_U`: a parcela desse total que se origina de complementação da União.
- `{E,M}_Tot2_E`: a parcela que se origina do próprio pool retido de Estados/Municípios.
`Tot1_U + Tot2_E == TOTAL`, por definição.

Conferido (2026-08-31) contra `CTB2024.xlsx` (aba RD ESFERA): a linha "FUNDEB" de União
para Estados publicada (36,668 bi) bate exato com `E_Tot1_U`; a de União para Municípios
(89,855 bi) bate exato com `M_Tot1_U`; a de Estados para Municípios (109,833 bi) bate
exato com `M_Tot2_E`. `E_Tot2_E` (73,981 bi) é redistribuição horizontal entre os
próprios Estados — não entra em nenhum bloco de transferência entre esferas porque, no
agregado "Estados" como esfera, o que um estado manda para o pool e o que recebe de
volta se cancelam.
"""

from __future__ import annotations

from dataclasses import dataclass

from pipeline.fontes.http import obter_binario

FONTE = "fundeb"

# URLs de download descobertas navegando a publicação de cada ano (padrão
# `.../transferencias-ao-fundo-.../{ano}/114`; 2022 é a exceção, publicada em
# `.../2022/114-2`). Levantadas em 2026-09-01.
URLS_POR_ANO: dict[int, str] = {
    2016: "https://thot-arquivos.tesouro.gov.br/publicacao/28521",
    2017: "https://thot-arquivos.tesouro.gov.br/publicacao/28522",
    2018: "https://thot-arquivos.tesouro.gov.br/publicacao/28523",
    2019: "https://thot-arquivos.tesouro.gov.br/publicacao/29102",
    2020: "https://thot-arquivos.tesouro.gov.br/publicacao/31597",
    2021: "https://thot-arquivos.tesouro.gov.br/publicacao/37244",
    2022: "https://thot-arquivos.tesouro.gov.br/publicacao/42670",
    2023: "https://thot-arquivos.tesouro.gov.br/publicacao/46131",
    2024: "https://thot-arquivos.tesouro.gov.br/publicacao/48848",
    2025: "https://thot-arquivos.tesouro.gov.br/publicacao/51322",
}


class ErroFundeb(RuntimeError):
    """Estrutura inesperada na planilha do FUNDEB — nunca inventa um total."""


@dataclass(frozen=True)
class TotaisFundeb:
    estados_total: float
    estados_origem_uniao: float
    estados_origem_estados: float
    municipios_total: float
    municipios_origem_uniao: float
    municipios_origem_estados: float


def _total_anual(sh) -> float:
    for r in range(sh.nrows):
        if str(sh.cell_value(r, 0)).strip().upper() == "REPASSE MENSAL TOTAL":
            return float(sh.cell_value(r, sh.ncols - 1))
    raise ErroFundeb("linha 'REPASSE MENSAL TOTAL' não encontrada na aba")


def obter_totais(ano: int, *, forcar: bool = False) -> TotaisFundeb:
    import xlrd

    if ano not in URLS_POR_ANO:
        raise ErroFundeb(
            f"{ano}: URL de download do FUNDEB não mapeada nesta primeira passada "
            f"(só {sorted(URLS_POR_ANO)}). Navegar "
            "https://www.tesourotransparente.gov.br/publicacoes/transferencias-ao-fundo-"
            f"de-manutencao-e-desenvolvimento-da-educacao-basica-fundeb/{ano}/114 "
            "para achar o link de download desse ano e adicionar em URLS_POR_ANO."
        )
    caminho = obter_binario(URLS_POR_ANO[ano], fonte=FONTE, ano=ano, chave="fundeb.xls", forcar=forcar)
    wb = xlrd.open_workbook(str(caminho))
    abas = {"E_TOTAL", "E_Tot1_U", "E_Tot2_E", "M_TOTAL", "M_Tot1_U", "M_Tot2_E"}
    faltando = abas - set(wb.sheet_names())
    if faltando:
        raise ErroFundeb(f"{caminho}: aba(s) esperada(s) ausente(s): {sorted(faltando)}")
    return TotaisFundeb(
        estados_total=_total_anual(wb.sheet_by_name("E_TOTAL")),
        estados_origem_uniao=_total_anual(wb.sheet_by_name("E_Tot1_U")),
        estados_origem_estados=_total_anual(wb.sheet_by_name("E_Tot2_E")),
        municipios_total=_total_anual(wb.sheet_by_name("M_TOTAL")),
        municipios_origem_uniao=_total_anual(wb.sheet_by_name("M_Tot1_U")),
        municipios_origem_estados=_total_anual(wb.sheet_by_name("M_Tot2_E")),
    )
