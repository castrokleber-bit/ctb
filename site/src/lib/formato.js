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

// Unidade selecionada -> como extrair e formatar o valor de uma LinhaQuadro
// ({rotulo, valor_reais, valor_bi, pct_pib, pct_total, per_capita}).
export const UNIDADES = {
  bi: { rotulo: "R$ bilhões", campo: "valor_bi", formatar: (v) => numero(v, 2) },
  pct_pib: { rotulo: "% do PIB", campo: "pct_pib", formatar: (v) => numero(v, 2) },
  pct_total: { rotulo: "% do total", campo: "pct_total", formatar: (v) => numero(v, 2) },
  per_capita: { rotulo: "Per capita (R$)", campo: "per_capita", formatar: (v) => numero(v, 2) },
};
