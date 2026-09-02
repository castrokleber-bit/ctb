// Paleta categórica por esfera de governo — usada em todo gráfico do site (Grafico,
// GraficoSerie, DiagramaFluxo) pra manter a mesma cor por esfera em qualquer visão.
// Valores hex fixos (não variáveis CSS): o ECharts renderiza em canvas e não resolve
// custom properties.
export const CORES_ESFERA = {
  U: "#2E7CB8",
  E: "#D99E2B",
  M: "#21A69A",
  consolidado: "#7C4DA8",
};

// Alta (verde) e queda (terracota) — ranking de variação de carga por tributo.
export const COR_ALTA = "#2F8F57";
export const COR_QUEDA = "#C0503F";

// Paleta categórica default — usada quando o gráfico não tem uma esfera única de
// referência (Principais Tributos, Bases de Incidência): ciclo de tons "planos" que
// combinam com o resto da identidade, em vez de cores arbitrárias do ECharts.
export const PALETA_CATEGORICA = [
  "#2E7CB8", "#D99E2B", "#21A69A", "#7C4DA8",
  "#D9622E", "#4F8A5B", "#5B6B7A", "#B25C8A",
];

function hexParaHsl(hex) {
  const n = hex.replace("#", "");
  const r = parseInt(n.slice(0, 2), 16) / 255;
  const g = parseInt(n.slice(2, 4), 16) / 255;
  const b = parseInt(n.slice(4, 6), 16) / 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  let h = 0, s = 0;
  const l = (max + min) / 2;
  const d = max - min;
  if (d !== 0) {
    s = d / (1 - Math.abs(2 * l - 1));
    switch (max) {
      case r: h = ((g - b) / d) % 6; break;
      case g: h = (b - r) / d + 2; break;
      default: h = (r - g) / d + 4;
    }
    h *= 60;
    if (h < 0) h += 360;
  }
  return { h, s, l };
}

function hslParaHex(h, s, l) {
  const c = (1 - Math.abs(2 * l - 1)) * s;
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = l - c / 2;
  let [r, g, b] = [0, 0, 0];
  if (h < 60) [r, g, b] = [c, x, 0];
  else if (h < 120) [r, g, b] = [x, c, 0];
  else if (h < 180) [r, g, b] = [0, c, x];
  else if (h < 240) [r, g, b] = [0, x, c];
  else if (h < 300) [r, g, b] = [x, 0, c];
  else [r, g, b] = [c, 0, x];
  const toHex = (v) =>
    Math.round((v + m) * 255).toString(16).padStart(2, "0");
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
}

// N tons de `corBase`, do mais escuro ao mais claro — pra um gráfico de pizza de uma
// esfera só (composição interna) manter a identidade de cor da esfera em vez de virar
// multicolorido sem relação com o resto do site.
export function matizes(corBase, n) {
  if (n <= 1) return [corBase];
  const { h, s, l } = hexParaHsl(corBase);
  const lMin = Math.max(0.24, l - 0.24);
  const lMax = Math.min(0.82, l + 0.28);
  return Array.from({ length: n }, (_, i) => hslParaHex(h, s, lMin + (lMax - lMin) * (i / (n - 1))));
}

// Gradiente vertical sutil (mais claro no topo) pra dar um pouco de profundidade às
// barras — mesmo espírito de painel "premium" da referência, sem exagerar: só dois
// tons da própria cor, não um gradiente multicolorido.
export function gradienteVertical(corBase) {
  const { h, s, l } = hexParaHsl(corBase);
  const claro = hslParaHex(h, s, Math.min(0.88, l + 0.16));
  return {
    type: "linear", x: 0, y: 0, x2: 0, y2: 1,
    colorStops: [
      { offset: 0, color: claro },
      { offset: 1, color: corBase },
    ],
  };
}

// Tooltip escuro e arredondado, flutuando sobre o gráfico claro — usado em todo
// gráfico ECharts do site (Grafico, GraficoSerie, GraficoVariacao, DiagramaFluxo) pra
// dar contraste e uma sensação mais "painel de controle" sem escurecer o site inteiro.
export const TOOLTIP_TEMA = {
  backgroundColor: "#22303f",
  borderWidth: 0,
  borderRadius: 10,
  padding: [8, 12],
  textStyle: { color: "#f2f4f7", fontSize: 12, fontFamily: "Inter, sans-serif" },
  extraCssText: "box-shadow: 0 12px 28px -10px rgba(20, 24, 18, 0.45);",
};
