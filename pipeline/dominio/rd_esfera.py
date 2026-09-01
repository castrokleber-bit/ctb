"""RD ESFERA — receita disponível por esfera de governo.

Ajusta `AD ESFERA` pelas transferências constitucionais entre entes: o que uma esfera
arrecada não é, necessariamente, o que fica disponível para ela gastar. Total geral não
muda (é redistribuição, não dinheiro novo) — `RD ESFERA` tem que somar exatamente o
mesmo que `AD ESFERA`.

Cobre 2016-2025. Cada fonte abaixo:

- **FPE, FPM, ITR, IPI-Exp (FPEx), IOF-Ouro, CIDE, LC176/2020 (Seguro-Receita ICMS)**
  — CKAN "transferências obrigatórias da União" (`pipeline.fontes.ckan_transferencias`).
- **Royalties e outras compensações financeiras, Cessão Onerosa, AFM/AFE, LC173/2020,
  LC201/2023** — CSV fornecido pelo usuário em `manual/` (ver `_normalizar_modalidade`
  para a lista completa e o porquê de excluir FEX/LC176 daí: já vêm do CKAN, contar dos
  dois lados duplicaria).
- **FUNDEB — 2024**: planilha oficial da STN (`pipeline.fontes.fundeb`), já separada por
  origem (União/Estados) nas próprias abas. **FUNDEB — outros anos**: o servidor que
  hospeda essa planilha (`thot-arquivos.tesouro.gov.br`) ficou fora do ar durante a
  extensão para a série; o usuário forneceu dois CSVs brutos em `manual/`
  (`fundeb_estados.csv`, `fundeb_municipios.csv`) com a redistribuição já decomposta por
  modalidade de origem (`FUNDEB - ICMS`, `FUNDEB - FPE`, `FUNDEB - COUN` etc.).
  `_somar_fundeb_manual` reclassifica essa decomposição em origem União/Estados — ver a
  regra e a validação (quase exata contra a planilha oficial de 2024) no docstring da
  função. **2024 continua vindo da planilha oficial**, não deste CSV, para preservar os
  números já publicados em `docs/decisoes-pendentes.md` §9.
- **ICMS e IPVA, cota-parte municipal** — calculado internamente: 25% e 50% da
  arrecadação estadual já computada em `AD ESFERA` (art. 158 CF), não uma fonte de dados
  externa. **Decidido pelo usuário em 2026-08-31** (`docs/decisoes-pendentes.md` §9): a
  cota do ICMS aplica também a retenção de 20% do FUNDEB (art. 212-A CF) antes do
  repasse — `25% × 80% = 20%` da arrecadação bruta —, reproduzindo o valor publicado em
  2024 quase exato (R$ 161,631 bi calculado contra R$ 161,083 bi publicado). A cota do
  IPVA não tem essa retenção (bate quase exato em 50% flat, sem ajuste).
- **Salário-Educação (quota estadual)** — calculado internamente: 2/3 da arrecadação da
  União com Salário-Educação (regra dada pelo usuário, 2026-08-31).
- **FPEx e LC201/2023, repasse aos municípios** — mesma cota de 25% do art. 159 §3º CF
  aplicada ao valor que os Estados receberam da União nessas duas modalidades
  (tratadas como ICMS para fins de repartição constitucional). Confere exato contra a
  planilha antiga (FPEx: 6,765 bi × 25% = 1,691 bi; LC201: 0,674 bi × 25% = 0,169 bi).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import polars as pl

from pipeline.fontes import ckan_transferencias, fundeb
from pipeline.fontes.http import RAIZ

DIR_MANUAL = RAIZ / "manual"
ARQUIVO_MANUAL_ESTADOS = DIR_MANUAL / "transferencias_royalties_e_compensacoes_estados.csv"
ARQUIVO_MANUAL_MUNICIPIOS = DIR_MANUAL / "transferencias_royalties_e_compensacoes_municipios.csv"
ARQUIVO_MANUAL_FUNDEB_ESTADOS = DIR_MANUAL / "fundeb_estados.csv"
ARQUIVO_MANUAL_FUNDEB_MUNICIPIOS = DIR_MANUAL / "fundeb_municipios.csv"

# No CSV bruto do FUNDEB (`FUNDEB - <modalidade>`), estas três são o único tributo
# próprio dos Estados que alimenta o pool — o resto (COUN* = Complementação da União,
# FPE, FPM, IPI-EXP, ITR, AFE, LC 87) é, por eliminação, origem União. Validado
# 2026-09-01: a soma de ICMS+IPVA+ITCMD no CSV de municípios para 2024 (R$ 109,830 bi)
# bate quase exato com "TOTAL ORIGEM ESTADOS" da planilha oficial da STN para o mesmo
# ano (R$ 109,833 bi, `pipeline.fontes.fundeb`) — a mesma reclassificação usada aqui
# para os outros nove anos.
MODALIDADES_FUNDEB_TRIBUTO_PROPRIO_ESTADOS = {"ICMS", "IPVA", "ITCMD"}

# Escopo do projeto (CLAUDE.md): 2016-2025. Os dois CSVs de manual/fundeb_*.csv também
# têm 2026, mas fica fora daqui até o restante do pipeline cobrir esse ano.
ANOS_DISPONIVEIS = range(2016, 2026)

FRACAO_ICMS_MUNICIPIOS = 0.25  # art. 158, IV, CF
FRACAO_IPVA_MUNICIPIOS = 0.50  # art. 158, III, CF
# retenção do FUNDEB (art. 212-A CF) sobre a cota-parte municipal do ICMS antes do
# repasse — decisão do usuário em 2026-08-31 (docs/decisoes-pendentes.md §9); não se
# aplica à cota-parte do IPVA, que bate exato sem esse ajuste.
RETENCAO_FUNDEB_ICMS_MUNICIPAL = 0.20
FRACAO_SALARIO_EDUCACAO_ESTADOS = 2 / 3  # quota estadual, Lei 9.766/1998
FRACAO_COTA_MUNICIPAL_ICMS_LIKE = 0.25  # art. 159, §3º, CF

# Modalidades recebidas pelos Estados que, por lei, repassam 25% aos municípios (mesma
# regra do ICMS) — nomes têm que bater com o rótulo emitido por ckan_transferencias/
# _normalizar_modalidade.
MODALIDADES_ICMS_LIKE_ESTADOS_PARA_MUNICIPIOS = {
    "IPI-Exp (FPEx)",
    "LC201/2023 (Compensação ICMS)",
}


class ErroRdEsfera(RuntimeError):
    """RD ESFERA não fecha, ou uma modalidade de manual/ não foi reconhecida."""


@dataclass(frozen=True)
class LinhaTransferencia:
    bloco_origem: str
    bloco_destino: str
    modalidade: str
    valor_reais: float


@dataclass(frozen=True)
class ResultadoRdEsfera:
    transferencias: list[LinhaTransferencia]
    rd_por_esfera: dict[str, float]


def _parse_valor(s: str) -> float:
    s = s.strip()
    if s.startswith("R$"):
        s = s[2:]
    s = s.strip()
    if not s:
        return 0.0
    return float(s.replace(".", "").replace(",", "."))


def _normalizar_modalidade(bruta: str) -> str | None:
    """Devolve o rótulo canônico da modalidade, ou None se ela já vem do CKAN (para
    não contar duas vezes). Levanta erro para qualquer rótulo não reconhecido — regra 3
    do CLAUDE.md, aplicada aqui a modalidades de transferência, não só a naturezas de
    receita.
    """
    b = bruta.strip()
    if b == "FEX" or b.startswith("LC 176/2020"):
        return None
    if b.startswith("Royalties"):
        return "Royalties e Compensações Financeiras"
    if b.startswith("Cessão Onerosa"):
        return "Cessão Onerosa"
    if b.startswith("AFM/AFE"):
        return "AFM/AFE"
    if b.startswith("LC 173/2020"):
        return "LC173/2020 (PFEC)"
    if b.startswith("LC 201/2023"):
        return "LC201/2023 (Compensação ICMS)"
    raise ErroRdEsfera(
        f"modalidade não reconhecida em manual/: {bruta!r} — atualizar "
        "_normalizar_modalidade em pipeline/dominio/rd_esfera.py"
    )


def _somar_manual(caminho: Path, ano: int) -> dict[str, float]:
    if not caminho.exists():
        raise ErroRdEsfera(f"arquivo manual não encontrado: {caminho}")
    somas: dict[str, float] = {}
    with caminho.open(encoding="utf-8-sig", newline="") as f:
        leitor = csv.reader(f, delimiter=";")
        cabecalho = next(leitor)
        cabecalho = [c.strip().strip('"') for c in cabecalho]
        idx_ano = cabecalho.index("Ano")
        idx_mod = cabecalho.index("Transferência")
        idx_val = cabecalho.index("Valor Consolidado")
        for linha in leitor:
            if not linha or len(linha) <= max(idx_ano, idx_mod, idx_val):
                continue
            if linha[idx_ano].strip().strip('"') != str(ano):
                continue
            modalidade = _normalizar_modalidade(linha[idx_mod].strip('"'))
            if modalidade is None:
                continue
            valor = _parse_valor(linha[idx_val].strip('"'))
            somas[modalidade] = somas.get(modalidade, 0.0) + valor
    return somas


def _somar_fundeb_manual(caminho: Path, ano: int) -> tuple[float, float]:
    """Lê `manual/fundeb_{estados,municipios}.csv` (rótulos `FUNDEB - <modalidade>`) e
    devolve `(origem_uniao, origem_estados)` para `ano` — ver a regra de reclassificação
    e a validação em `MODALIDADES_FUNDEB_TRIBUTO_PROPRIO_ESTADOS`.
    """
    if not caminho.exists():
        raise ErroRdEsfera(f"arquivo manual não encontrado: {caminho}")
    origem_uniao = 0.0
    origem_estados = 0.0
    encontrou_ano = False
    with caminho.open(encoding="utf-8-sig", newline="") as f:
        leitor = csv.reader(f, delimiter=";")
        cabecalho = [c.strip().strip('"') for c in next(leitor)]
        idx_ano = cabecalho.index("Ano")
        idx_mod = cabecalho.index("Transferência")
        idx_val = cabecalho.index("Valor Consolidado")
        for linha in leitor:
            if not linha or len(linha) <= max(idx_ano, idx_mod, idx_val):
                continue
            if linha[idx_ano].strip().strip('"') != str(ano):
                continue
            encontrou_ano = True
            bruta = linha[idx_mod].strip('"')
            if not bruta.startswith("FUNDEB - "):
                raise ErroRdEsfera(
                    f"{caminho.name}: modalidade sem o prefixo esperado 'FUNDEB - ': {bruta!r}"
                )
            modalidade = bruta[len("FUNDEB - "):]
            valor = _parse_valor(linha[idx_val].strip('"'))
            if modalidade in MODALIDADES_FUNDEB_TRIBUTO_PROPRIO_ESTADOS:
                origem_estados += valor
            else:
                origem_uniao += valor
    if not encontrou_ano:
        raise ErroRdEsfera(f"{caminho.name}: nenhuma linha para {ano}")
    return origem_uniao, origem_estados


def calcular(
    ano: int, df_intermediario: pl.DataFrame, ad_por_esfera: dict[str, float], *, forcar: bool = False,
) -> ResultadoRdEsfera:
    transferencias: list[LinhaTransferencia] = []

    for t in ckan_transferencias.obter_transferencias(ano, forcar=forcar):
        transferencias.append(LinhaTransferencia(t.bloco_origem, t.bloco_destino, t.modalidade, t.valor_reais))

    for modalidade, valor in _somar_manual(ARQUIVO_MANUAL_ESTADOS, ano).items():
        transferencias.append(LinhaTransferencia("U", "E", modalidade, valor))
    for modalidade, valor in _somar_manual(ARQUIVO_MANUAL_MUNICIPIOS, ano).items():
        transferencias.append(LinhaTransferencia("U", "M", modalidade, valor))

    if ano == 2024:
        # Único ano com a planilha oficial da STN já baixada e validada — mantém os
        # números tal como reportados em docs/decisoes-pendentes.md §9. Não troca pelo
        # CSV manual mesmo que este dê um resultado próximo.
        ft = fundeb.obter_totais(ano, forcar=forcar)
        e_uniao, m_uniao, m_estados = (
            ft.estados_origem_uniao, ft.municipios_origem_uniao, ft.municipios_origem_estados,
        )
        # ft.estados_origem_estados (E_Tot2_E) é redistribuição horizontal entre os
        # próprios Estados — no agregado da esfera "Estados" o que sai e o que volta se
        # cancelam, por isso fica fora do modelo de transferência entre esferas.
    else:
        e_uniao, _ = _somar_fundeb_manual(ARQUIVO_MANUAL_FUNDEB_ESTADOS, ano)
        m_uniao, m_estados = _somar_fundeb_manual(ARQUIVO_MANUAL_FUNDEB_MUNICIPIOS, ano)
    transferencias.append(LinhaTransferencia("U", "E", "FUNDEB", e_uniao))
    transferencias.append(LinhaTransferencia("U", "M", "FUNDEB", m_uniao))
    transferencias.append(LinhaTransferencia("E", "M", "FUNDEB", m_estados))

    arrecadacao_e = dict(
        df_intermediario.filter(pl.col("esfera") == "E")
        .group_by("rubrica").agg(pl.col("valor_reais").sum()).iter_rows()
    )
    icms = arrecadacao_e.get("ICMS", 0.0)
    ipva = arrecadacao_e.get("IPVA", 0.0)
    icms_cota = icms * FRACAO_ICMS_MUNICIPIOS * (1 - RETENCAO_FUNDEB_ICMS_MUNICIPAL)
    transferencias.append(LinhaTransferencia("E", "M", "ICMS (cota-parte municipal, líq. FUNDEB)", icms_cota))
    transferencias.append(LinhaTransferencia("E", "M", "IPVA (cota-parte municipal)", ipva * FRACAO_IPVA_MUNICIPIOS))

    arrecadacao_u = dict(
        df_intermediario.filter(pl.col("esfera") == "U")
        .group_by("rubrica").agg(pl.col("valor_reais").sum()).iter_rows()
    )
    sal_educ = arrecadacao_u.get("Salário Educação", 0.0)
    transferencias.append(LinhaTransferencia(
        "U", "E", "Salário-Educação (quota estadual)", sal_educ * FRACAO_SALARIO_EDUCACAO_ESTADOS,
    ))

    recebido_estados = {
        t.modalidade: t.valor_reais for t in transferencias if t.bloco_destino == "E"
    }
    for modalidade in MODALIDADES_ICMS_LIKE_ESTADOS_PARA_MUNICIPIOS:
        recebido = recebido_estados.get(modalidade, 0.0)
        if recebido:
            transferencias.append(LinhaTransferencia(
                "E", "M", f"{modalidade} (cota-parte municipal)", recebido * FRACAO_COTA_MUNICIPAL_ICMS_LIKE,
            ))

    rd = dict(ad_por_esfera)
    for t in transferencias:
        rd[t.bloco_origem] = rd.get(t.bloco_origem, 0.0) - t.valor_reais
        rd[t.bloco_destino] = rd.get(t.bloco_destino, 0.0) + t.valor_reais

    if abs(sum(rd.values()) - sum(ad_por_esfera.values())) > 1.0:
        raise ErroRdEsfera(
            "RD ESFERA não conserva o total de AD ESFERA — bug na construção das "
            "transferências (toda transferência tem que sair de um bloco e entrar em "
            "outro), não é resíduo esperado."
        )

    return ResultadoRdEsfera(transferencias=transferencias, rd_por_esfera=rd)
