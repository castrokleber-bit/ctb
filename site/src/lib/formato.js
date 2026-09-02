// Formatação pt-BR — mesmo padrão de `pipeline/fontes/diagnostico.py::br()`.
const fmtNumero = (casas) =>
  new Intl.NumberFormat("pt-BR", { minimumFractionDigits: casas, maximumFractionDigits: casas });

export function numero(valor, casas = 0) {
  if (valor === null || valor === undefined || Number.isNaN(valor)) return "—";
  return fmtNumero(casas).format(valor);
}

export function reaisBi(valorBi, casas = 2) {
  return `R$ ${numero(valorBi, casas)} bi`;
}

export function percentual(valor, casas = 2) {
  return `${numero(valor, casas)}%`;
}

const fmtPontos = (casas) =>
  new Intl.NumberFormat("pt-BR", {
    minimumFractionDigits: casas,
    maximumFractionDigits: casas,
    signDisplay: "exceptZero",
  });

// Variação em pontos do PIB, com sinal explícito (+/−) — não confundir com `percentual`,
// que formata um nível (35,90%), não uma diferença entre dois níveis.
export function pontosPib(valor, casas = 2) {
  if (valor === null || valor === undefined || Number.isNaN(valor)) return "—";
  return `${fmtPontos(casas).format(valor)} p.p.`;
}

// Data/hora de publicação (`metadados.json::gerado_em`, ISO local sem fuso) formatada
// em pt-BR — mesmo horário do servidor que rodou `uv run ctb publicar`.
export function dataHora(isoLocal) {
  if (!isoLocal) return "—";
  const d = new Date(isoLocal);
  if (Number.isNaN(d.getTime())) return isoLocal;
  return `${d.toLocaleDateString("pt-BR")} às ${d.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}`;
}

// Unidade selecionada -> como extrair e formatar o valor de uma LinhaQuadro
// ({rotulo, valor_reais, valor_bi, pct_pib, pct_total, per_capita}).
export const UNIDADES = {
  bi: { rotulo: "R$ bilhões", campo: "valor_bi", formatar: (v) => numero(v, 2) },
  pct_pib: { rotulo: "% do PIB", campo: "pct_pib", formatar: (v) => numero(v, 2) },
  pct_total: { rotulo: "% do total", campo: "pct_total", formatar: (v) => numero(v, 2) },
  per_capita: { rotulo: "Per capita (R$)", campo: "per_capita", formatar: (v) => numero(v, 2) },
};
