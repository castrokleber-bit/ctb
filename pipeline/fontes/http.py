"""Cliente HTTP com cache em disco.

Regra 5 do CLAUDE.md: cache é sagrado. Toda resposta vai para
``dados/bruto/{fonte}/{ano}/{chave}.json`` e nunca é rebaixada sem ``forcar=True``.
As APIs do Tesouro são públicas e lentas — refazer download é abuso, não zelo.
"""

from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[2]
DIR_BRUTO = RAIZ / "dados" / "bruto"

_UA = "ctb/0.1 (pipeline de carga tributaria; contato via repositorio)"


class ErroFonte(RuntimeError):
    """Falha ao obter dado de uma fonte externa. Nunca é engolida."""


@dataclass(frozen=True)
class Resposta:
    dados: Any
    do_cache: bool
    segundos: float


def _caminho_cache(fonte: str, ano: int | str, chave: str) -> Path:
    # A chave vira nome de arquivo; se for longa ou tiver caractere inválido no
    # Windows, cai para um hash estável.
    seguro = "".join(c if c.isalnum() or c in "-_." else "_" for c in chave)
    if len(seguro) > 80:
        seguro = seguro[:60] + "-" + hashlib.sha1(chave.encode()).hexdigest()[:12]
    return DIR_BRUTO / fonte / str(ano) / f"{seguro}.json"


def obter_json(
    url: str,
    *,
    fonte: str,
    ano: int | str,
    chave: str,
    params: dict[str, Any] | None = None,
    forcar: bool = False,
    tentativas: int = 4,
    timeout: int = 180,
) -> Resposta:
    """Baixa JSON com cache em disco e retry exponencial.

    Levanta ``ErroFonte`` se todas as tentativas falharem — nunca devolve
    ``None`` nem estrutura vazia disfarçada de sucesso.
    """
    destino = _caminho_cache(fonte, ano, chave)
    if destino.exists() and not forcar:
        return Resposta(json.loads(destino.read_text(encoding="utf-8")), True, 0.0)

    completa = url + ("?" + urllib.parse.urlencode(params) if params else "")
    inicio = time.time()
    ultimo: Exception | None = None
    for tentativa in range(tentativas):
        try:
            req = urllib.request.Request(completa, headers={"User-Agent": _UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                bruto = resp.read().decode("utf-8", "replace")
            dados = json.loads(bruto)
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
            return Resposta(dados, False, time.time() - inicio)
        except urllib.error.HTTPError as e:
            ultimo = e
            if e.code in (400, 404):  # erro de contrato: retry não resolve
                break
            time.sleep(2**tentativa)
        except Exception as e:  # rede, timeout, JSON malformado
            ultimo = e
            time.sleep(2**tentativa)

    raise ErroFonte(f"falha em {completa} após {tentativas} tentativa(s): {ultimo!r}")


def obter_binario(
    url: str,
    *,
    fonte: str,
    ano: int | str,
    chave: str,
    forcar: bool = False,
    tentativas: int = 4,
    timeout: int = 180,
) -> Path:
    """Baixa um arquivo binário (CSV, XLS) com cache em disco. Devolve o caminho do
    arquivo em cache — quem chama decide como parsear (texto, planilha etc.).
    """
    seguro = "".join(c if c.isalnum() or c in "-_." else "_" for c in chave)
    if len(seguro) > 80:
        seguro = seguro[:60] + "-" + hashlib.sha1(chave.encode()).hexdigest()[:12]
    destino = DIR_BRUTO / fonte / str(ano) / seguro
    if destino.exists() and not forcar:
        return destino

    ultimo: Exception | None = None
    for tentativa in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": _UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                bruto = resp.read()
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_bytes(bruto)
            return destino
        except urllib.error.HTTPError as e:
            ultimo = e
            if e.code in (400, 404):
                break
            time.sleep(2**tentativa)
        except Exception as e:
            ultimo = e
            time.sleep(2**tentativa)

    raise ErroFonte(f"falha em {url} após {tentativas} tentativa(s): {ultimo!r}")
