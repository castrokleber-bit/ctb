"""CKAN "transferências obrigatórias da União" — FPE, FPM, ITR, IPI-Exp (FPEx), IOF
sobre ouro, CIDE e LC176/2020 (Seguro-Receita ICMS).

Fonte: pacote `transferencias-obrigatorias-da-uniao`
(https://www.tesourotransparente.gov.br/ckan/dataset/transferencias-obrigatorias-da-uniao),
package id `f85b6632-1c9c-4beb-9e60-72e91156c984`. Série mensal por UF desde jan/1991.

Investigado e validado contra `CTB2024.xlsx` (aba RD ESFERA, 2026-08-31) para 2024: os
valores já saem líquidos de retenção FUNDEB/FUNDEB (nota de rodapé do próprio arquivo) e
batem exatos ou muito próximos para FPE, FPM, ITR, IPI-EXP, IOF (EST/MUN), CIDE (EST/MUN)
e LC176 (EST/MUN — rotulada "SEGURO REC. ICMS" na planilha antiga).

`FPM_CAPITAIS` é um recorte que já está dentro de `FPM` — nunca somar os dois. `TCP`
(Ministério do Esporte) não tem correspondência identificada na planilha antiga — fora
do escopo desta passada. `LC87` (Lei Kandir, extinta dez/2018) e `FEX` (extinta
dez/2017) são mantidas por completude — valem 0 em 2024, mas isso é verificado, não
assumido.
"""

from __future__ import annotations

from dataclasses import dataclass

from pipeline.fontes.http import obter_binario, obter_json

FONTE = "ckan_transferencias_uniao"
PACOTE = "transferencias-obrigatorias-da-uniao"
URL_PACKAGE_SHOW = f"https://www.tesourotransparente.gov.br/ckan/api/3/action/package_show?id={PACOTE}"

# recurso -> (bloco_destino, modalidade); bloco_destino é sempre "E" (Estados+DF) ou
# "M" (Municípios); origem é sempre "U" (União).
RECURSOS: dict[str, tuple[str, str]] = {
    "FPE": ("E", "FPE"),
    "FPM": ("M", "FPM"),
    "ITR": ("M", "ITR"),
    "IPI-EXP": ("E", "IPI-Exp (FPEx)"),
    "IOF_EST": ("E", "IOF-Ouro"),
    "IOF_MUN": ("M", "IOF-Ouro"),
    "CIDE_EST": ("E", "CIDE"),
    "CIDE_MUN": ("M", "CIDE"),
    "LC176_EST": ("E", "LC176/2020 (Seguro-Receita ICMS)"),
    "LC176_MUN": ("M", "LC176/2020 (Seguro-Receita ICMS)"),
    "FEX_EST": ("E", "FEX"),
    "FEX_MUN": ("M", "FEX"),
    "LC87_EST": ("E", "LC87/1996 (Lei Kandir)"),
    "LC87_MUN": ("M", "LC87/1996 (Lei Kandir)"),
}

UFS = {
    "acre", "alagoas", "amazonas", "amapá", "bahia", "ceará", "distrito federal",
    "espírito santo", "goiás", "maranhão", "minas gerais", "mato grosso do sul",
    "mato grosso", "pará", "paraíba", "pernambuco", "piauí", "paraná",
    "rio de janeiro", "rio grande do norte", "rondônia", "roraima",
    "rio grande do sul", "santa catarina", "sergipe", "são paulo", "tocantins",
}


class ErroCkanTransferencias(RuntimeError):
    """Estrutura inesperada num recurso do CKAN — nunca soma dado que não entendeu."""


@dataclass(frozen=True)
class Transferencia:
    modalidade: str
    bloco_origem: str
    bloco_destino: str
    valor_reais: float


def _parse_br(s: str) -> float:
    s = s.strip()
    if not s or s in ("-", "..."):
        return 0.0
    return float(s.replace(".", "").replace(",", "."))


def _urls_dos_recursos(ano: int, forcar: bool) -> dict[str, str]:
    resp = obter_json(URL_PACKAGE_SHOW, fonte=FONTE, ano="_pacote", chave="package_show", forcar=forcar)
    pacote = resp.dados["result"]
    return {r["name"]: r["url"] for r in pacote["resources"]}


_MESES = (
    "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
    "setembro", "outubro", "novembro", "dezembro",
)


def _somar_recurso(caminho, ano: int) -> float:
    texto = caminho.read_bytes().decode("latin-1")
    linhas = [ln for ln in texto.splitlines() if ln.strip()]
    cab_idx = next(
        (i for i, ln in enumerate(linhas)
         if ln.split(";")[0].strip().upper() in ("ESTADOS", "MUNICÍPIOS", "MUNICIPIOS", "UF", "ENTE")),
        None,
    )
    if cab_idx is None:
        raise ErroCkanTransferencias(f"{caminho}: cabeçalho não encontrado nas 3 primeiras colunas")
    cabecalho = linhas[cab_idx].split(";")
    idxs = [j for j, c in enumerate(cabecalho) if f"/{str(ano)[2:]}" in c.lower()]
    if not idxs:
        # a maioria dos recursos é mensal desde jan/1991, mas alguns fundos foram
        # extintos antes de `ano` (Lei Kandir, dez/2018; FEX, dez/2017) e outros só
        # passaram a existir depois (LC176/2020, a partir de jan/2020) — o cabeçalho
        # simplesmente não cobre `ano`. Distingue isso de um cabeçalho quebrado: só
        # aceita ausência silenciosa se `ano` estiver fora do intervalo coberto.
        def _ano_4d(yy: str) -> int:
            # a série mais antiga começa em 1991 — 2 dígitos >= 50 é 19XX, senão 20XX.
            n = int(yy)
            return 1900 + n if n >= 50 else 2000 + n

        colunas_mes = [c for c in cabecalho if "/" in c and c.split("/")[0].lower() in _MESES]
        anos_cobertos = [_ano_4d(c.split("/")[1]) for c in colunas_mes]
        if anos_cobertos and not (min(anos_cobertos) <= ano <= max(anos_cobertos)):
            print(f"  aviso: {caminho.name} não tem dado para {ano} (série cobre "
                  f"{min(anos_cobertos)}-{max(anos_cobertos)}) — modalidade não existia "
                  "ou já tinha sido extinta nesse ano, tratada como R$ 0")
            return 0.0
        raise ErroCkanTransferencias(f"{caminho}: nenhuma coluna de {ano} encontrada no cabeçalho")
    total = 0.0
    for ln in linhas[cab_idx + 1:]:
        campos = ln.split(";")
        if len(campos) < 3 or campos[0].strip().lower() not in UFS:
            continue
        total += sum(_parse_br(campos[j]) for j in idxs if j < len(campos))
    return total


def obter_transferencias(ano: int, *, forcar: bool = False) -> list[Transferencia]:
    """Modalidades do CKAN para `ano`, uma por (bloco_destino, modalidade)."""
    urls = _urls_dos_recursos(ano, forcar)
    resultado = []
    for nome, (bloco_destino, modalidade) in RECURSOS.items():
        if nome not in urls:
            raise ErroCkanTransferencias(
                f"recurso '{nome}' não está mais no pacote CKAN '{PACOTE}' — "
                "catálogo mudou, revisar RECURSOS em ckan_transferencias.py"
            )
        caminho = obter_binario(urls[nome], fonte=FONTE, ano=ano, chave=f"{nome}.csv", forcar=forcar)
        valor = _somar_recurso(caminho, ano)
        resultado.append(Transferencia(modalidade, "U", bloco_destino, valor))
    return resultado
