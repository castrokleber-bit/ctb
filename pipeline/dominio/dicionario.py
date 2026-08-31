"""Carrega e aplica o dicionário de contas DCA.

Metodologia vigente (decisão de 2026-08-30, opção B de `docs/decisoes-pendentes.md` §1):
a arrecadação é classificada pela conta DCA de 7 níveis, com a política de colunas
declarada em `dicionario/politica_colunas.csv`. Não há linha "Multas e Dívida Ativa" e
o 8º dígito da natureza não é usado — a DCA não o publica.

Duas armadilhas que este módulo existe para evitar:

1. **Dupla contagem.** A árvore de contas é hierárquica: `RO1.1.1.0.00.0.0` já contém
   `RO1.1.1.3.00.0.0`. Só as contas listadas no dicionário são somadas, e o carregador
   recusa um dicionário em que uma conta seja ancestral de outra.
2. **Conta órfã.** Uma conta do ramo de arrecadação que não esteja no dicionário nem
   descenda de uma conta do dicionário é erro, não "outros" (regra 3 do CLAUDE.md).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from pipeline.fontes.http import ErroFonte, RAIZ

DIR_DICIONARIO = RAIZ / "dicionario"

# Ramos do plano de contas que constituem arrecadação. `RO1.3.4` (Exploração de Recursos
# Naturais) entrou por decisão 4 (2026-08-31, "linha própria"): é royalties e
# compensações financeiras, e passa a ter rubrica própria — ver
# dicionario/contas_dca_uniao.csv. O resto do ramo patrimonial (1.3.1 exploração
# imobiliária/aluguéis, 1.3.2 valores mobiliários/juros e dividendos, 1.3.3 delegação de
# serviços públicos, 1.3.5 patrimônio intangível, 1.3.6 cessão de direitos — em geral
# loterias, 1.3.9 demais) fica **fora do escopo de arrecadação**, permanentemente: não é
# carga tributária, nunca esteve nos quadros publicados, e por isso nem é classificado
# nem é tratado como órfão — simplesmente não entra no loop abaixo.
#
# `RI` são as receitas intra-orçamentárias, excluídas por definição — a série publicada
# usa "RECEITAS (EXCETO INTRA-ORÇAMENTÁRIAS)".
RAMOS_ARRECADACAO = ("RO1.1.", "RO1.2.", "RO1.3.4.")


class ErroDicionario(RuntimeError):
    """Dicionário inconsistente ou incompleto. Nunca é contornado com um valor padrão."""


@dataclass(frozen=True)
class Mapeamento:
    cod_conta: str
    rubrica: str
    tributo: str
    base_incidencia: str
    vigencia_inicio: int
    vigencia_fim: int | None
    observacao: str
    # Bloco do quadro em que a rubrica é publicada. Quase sempre igual à esfera do ente;
    # difere só na regra do DF, cujos ISS, IPTU e ITBI são publicados no bloco
    # Municípios enquanto o resto fica em Estados. Ver docs/decisoes-pendentes.md §2.
    bloco: str = ""

    def vigente_em(self, ano: int) -> bool:
        return self.vigencia_inicio <= ano and (self.vigencia_fim is None or ano <= self.vigencia_fim)


def _ler_csv(caminho: Path) -> list[dict[str, str]]:
    """Lê um CSV do dicionário, exigindo que toda linha tenha o número de campos do
    cabeçalho.

    `csv.DictReader` por si só é permissivo: uma linha com um `;` a mais dentro do texto
    de uma observação — fácil de escrever sem querer numa nota longa — desalinha as
    colunas seguintes sem erro nenhum. Já aconteceu neste projeto. Falha alto aqui é
    mais barato que descobrir depois que uma vigência virou texto de observação.
    """
    if not caminho.exists():
        raise ErroDicionario(f"dicionário ausente: {caminho}")
    with caminho.open(encoding="utf-8-sig", newline="") as fh:
        leitor = csv.reader(fh, delimiter=";")
        cabecalho = next(leitor)
        linhas_brutas = list(leitor)
    esperado = len(cabecalho)
    problemas = [
        f"linha {n} tem {len(campos)} campos, esperado {esperado} — provável ';' dentro "
        f"de um texto de observação: {';'.join(campos)[:80]}"
        for n, campos in enumerate(linhas_brutas, start=2) if campos and len(campos) != esperado
    ]
    if problemas:
        raise ErroDicionario(f"{caminho.name} desalinhado:\n  - " + "\n  - ".join(problemas))
    linhas = [dict(zip(cabecalho, campos)) for campos in linhas_brutas if campos]
    if not linhas:
        raise ErroDicionario(f"dicionário vazio: {caminho}")
    return linhas


def _ancestral(possivel_pai: str, conta: str) -> bool:
    """`RO1.1.1.0.00.0.0` é ancestral de `RO1.1.1.3.00.0.0`.

    A conta agregadora é a que tem **cauda de zeros**: tudo depois do seu último nível
    não-zero é zero. Ela é ancestral de outra quando o prefixo até esse ponto coincide
    e a outra desce ao menos um nível dentro da cauda.

    Cuidado com o plano de contas anterior a 2018: `1.2.1.0.01.0.0` (Cofins) tem um zero
    **estrutural** no 4º nível que não é marca de agregação — por isso a regra olha o
    último nível não-zero, e não o primeiro zero.
    """
    if possivel_pai == conta or possivel_pai[:2] != conta[:2]:
        return False
    pai = possivel_pai[2:].split(".")
    filho = conta[2:].split(".")
    if len(pai) != len(filho):
        return False
    nao_zero = [i for i, n in enumerate(pai) if int(n) != 0]
    corte = max(nao_zero) + 1 if nao_zero else 0
    if corte >= len(pai):
        return False  # o pai não tem cauda de zeros: é folha, não agrega ninguém
    if pai[:corte] != filho[:corte]:
        return False
    return any(int(n) != 0 for n in filho[corte:])


def _sobrepoe(a: Mapeamento, b: Mapeamento) -> bool:
    return (a.vigencia_inicio <= (b.vigencia_fim or 9999)
            and b.vigencia_inicio <= (a.vigencia_fim or 9999))


def carregar_mapeamentos(esfera: str) -> list[Mapeamento]:
    arquivo = {"U": "contas_dca_uniao.csv",
               "E": "contas_dca_estados.csv",
               "D": "contas_dca_estados.csv",
               "M": "contas_dca_municipios.csv"}[esfera]
    mapas = []
    for r in _ler_csv(DIR_DICIONARIO / arquivo):
        fim = r["vigencia_fim"].strip()
        mapas.append(Mapeamento(
            r["cod_conta"].strip(), r["rubrica"].strip(), r["tributo"].strip(),
            r["base_incidencia"].strip(), int(r["vigencia_inicio"]),
            int(fim) if fim else None, r.get("observacao", "").strip(),
            (r.get("bloco") or "").strip() or ("E" if esfera in ("E", "D") else esfera),
        ))

    bases = {r["base_incidencia"] for r in _ler_csv(DIR_DICIONARIO / "bases_incidencia.csv")}
    problemas = []
    for m in mapas:
        if m.base_incidencia not in bases:
            problemas.append(f"base de incidência desconhecida em {m.cod_conta}: {m.base_incidencia!r}")
    for a in mapas:
        for b in mapas:
            if _sobrepoe(a, b) and _ancestral(a.cod_conta, b.cod_conta):
                problemas.append(
                    f"dupla contagem: {a.cod_conta} ({a.rubrica}) é ancestral de "
                    f"{b.cod_conta} ({b.rubrica}) — mapeie os filhos ou o pai, nunca os dois")
    if problemas:
        raise ErroDicionario(f"dicionário {arquivo} inconsistente:\n  - " + "\n  - ".join(problemas))
    return mapas


OPERACOES_VALIDAS = ("somar", "subtrair", "ignorar")


def carregar_politica_colunas() -> dict[tuple[str, str], str]:
    """(esfera, coluna) -> 'somar' | 'subtrair' | 'ignorar'.

    A coluna de deduções vem com convenções de sinal diferentes por esfera (decisão 6):
    na União ela já é assinada, então soma; em estados e municípios ela é magnitude, então
    subtrai. `subtrair` e `somar com valor negativo` dão o mesmo resultado numérico — a
    distinção existe para o CSV declarar a convenção de sinal em vez de escondê-la num
    valor negativo que ninguém mais vai notar.
    """
    politica = {}
    for r in _ler_csv(DIR_DICIONARIO / "politica_colunas.csv"):
        operacao = r["operacao"].strip()
        if operacao not in OPERACOES_VALIDAS:
            raise ErroDicionario(f"operação desconhecida em politica_colunas.csv: {operacao!r}")
        politica[(r["esfera"].strip(), r["coluna"].strip())] = operacao
    return politica


def classificar(
    itens: list[dict], esfera: str, ano: int,
    mapas: list[Mapeamento] | None = None,
    politica: dict[tuple[str, str], str] | None = None,
    por_bloco: bool = False,
) -> tuple[dict, list[str]]:
    """Agrega os itens de um ente por rubrica, aplicando a política de colunas.

    Devolve `(valores, contas_orfas)`. A chave de `valores` é a rubrica, ou a tupla
    `(bloco, rubrica)` quando `por_bloco` — necessário para separar o DF, cujos ISS,
    IPTU e ITBI são publicados no bloco Municípios.

    Quem chama decide o que fazer com as órfãs: o pipeline falha, o diagnóstico relata.
    """
    mapas = mapas if mapas is not None else carregar_mapeamentos(esfera)
    politica = politica if politica is not None else carregar_politica_colunas()
    vigentes = [m for m in mapas if m.vigente_em(ano)]

    valores: dict[str, float] = {}
    orfas: set[str] = set()
    for i in itens:
        conta, coluna = i["cod_conta"], i["coluna"]
        if not conta.startswith(RAMOS_ARRECADACAO):
            continue
        if (esfera, coluna) not in politica:
            raise ErroDicionario(
                f"coluna não prevista em politica_colunas.csv para a esfera {esfera}: {coluna!r}")
        alvo = next((m for m in vigentes if m.cod_conta == conta), None)
        if alvo is None:
            # Uma conta não mapeada só é aceitável em dois casos, ambos porque seu valor
            # já está contado em outro lugar: ela **descende** de uma conta mapeada, ou
            # é um **totalizador** cujos filhos foram mapeados individualmente (caso de
            # 1.2.1.9, onde Salário-Educação precisa de linha própria).
            descende = any(_ancestral(m.cod_conta, conta) for m in vigentes)
            # Ser nó de agregação é fato estrutural do plano de contas, não temporal:
            # `1.1.1.2.00.0.0` segue sendo o totalizador de patrimônio mesmo nos anos em
            # que os impostos estaduais moraram em `1.1.1.8`. Por isso a checagem olha
            # todos os mapeamentos, não só os vigentes. Não há risco de dupla contagem —
            # totalizador nunca é somado.
            totaliza = any(_ancestral(conta, m.cod_conta) for m in mapas)
            if not (descende or totaliza):
                orfas.add(conta)
            continue
        operacao = politica[(esfera, coluna)]
        if operacao == "ignorar":
            continue
        sinal = 1.0 if operacao == "somar" else -1.0
        chave = (alvo.bloco, alvo.rubrica) if por_bloco else alvo.rubrica
        valores[chave] = valores.get(chave, 0.0) + sinal * i["valor"]
    return valores, sorted(orfas)
