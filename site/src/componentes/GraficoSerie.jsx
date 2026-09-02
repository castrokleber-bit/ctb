import { useEffect, useRef } from "react";
import * as echarts from "echarts";
import { UNIDADES } from "../lib/formato";
import { CORES_ESFERA, gradienteVertical, TOOLTIP_TEMA } from "../lib/cores";

const ESFERAS_EMPILHADAS = ["U", "E", "M"];
const ROTULO_TOTAL = "Setor Público Consolidado";

// Barras empilhadas — uma esfera por segmento, ano a ano; o total (Setor Público
// Consolidado) não é um segmento colorido, e sim um rótulo na extremidade externa da
// barra, calculado a partir de `serie.consolidado` — série separada da soma dos
// segmentos por design (`consolidar_linhas()` soma por rótulo, não por posição de pilha).
export default function GraficoSerie({ serie, rotuloEsfera, unidade, titulo, nomeArquivoPng }) {
  const containerRef = useRef(null);
  const instanciaRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const instancia = echarts.init(containerRef.current);
    instanciaRef.current = instancia;
    const aoRedimensionar = () => instancia.resize();
    window.addEventListener("resize", aoRedimensionar);
    return () => {
      window.removeEventListener("resize", aoRedimensionar);
      instancia.dispose();
    };
  }, []);

  useEffect(() => {
    const instancia = instanciaRef.current;
    if (!instancia || !serie) return;
    const config = UNIDADES[unidade];
    const anos = serie.U?.map((p) => p.ano) ?? [];
    const totais = serie.consolidado ?? [];

    const seriesEmpilhadas = ESFERAS_EMPILHADAS.map((esf) => ({
      name: rotuloEsfera[esf] ?? esf,
      type: "bar",
      stack: "esferas",
      barMaxWidth: 46,
      data: serie[esf].map((p) => p[config.campo]),
      itemStyle: { color: gradienteVertical(CORES_ESFERA[esf]) },
      label: {
        show: true,
        position: "inside",
        color: "#fff",
        fontSize: 10,
        // União tem o segmento com mais dígitos ("24,52") — com 26 anos no eixo, a
        // barra fica estreita demais pra caber o número na horizontal sem sobrar
        // pra fora; giradas na vertical cabem na largura da barra tranquilo.
        rotate: esf === "U" ? 90 : 0,
        formatter: (p) => config.formatar(p.value),
      },
      labelLayout: { hideOverlap: true },
    }));

    // Fronteira 2015→2016: série histórica (2000-2015) é extraída direto do
    // CTB-Resumo.xlsx, sem passar pela metodologia automatizada — ver
    // manual/README.md §ctb_resumo_*.csv. Marca a virada em vez de deixar o degrau
    // (ex.: "Multas e Dívida Ativa" some) sem contexto.
    const indiceFronteira = anos.findIndex((a) => a >= 2016);
    const temFronteira = indiceFronteira > 0;

    const serieTotal = {
      name: ROTULO_TOTAL,
      type: "bar",
      stack: "esferas",
      data: anos.map(() => 0),
      itemStyle: { color: "transparent" },
      silent: true,
      tooltip: { show: false },
      label: {
        show: true,
        position: "top",
        color: "#22303f",
        fontSize: 11,
        fontWeight: 600,
        formatter: (p) => config.formatar(totais[p.dataIndex]?.[config.campo]),
      },
      markLine: temFronteira
        ? {
            silent: true,
            symbol: "none",
            lineStyle: { type: "dashed", color: "#9aa3ad" },
            label: { formatter: "metodologia nova →", color: "#6b7684", fontSize: 10 },
            data: [{ xAxis: indiceFronteira - 0.5 }],
          }
        : undefined,
    };

    instancia.setOption({
      title: { text: titulo, left: "center", top: 8, textStyle: { fontSize: 14 } },
      grid: { left: 70, right: 30, top: 56, bottom: 92 },
      tooltip: {
        ...TOOLTIP_TEMA,
        trigger: "axis",
        axisPointer: { type: "shadow" },
        formatter: (params) => {
          const visiveis = params.filter((p) => p.seriesName !== ROTULO_TOTAL);
          if (visiveis.length === 0) return "";
          const idx = visiveis[0].dataIndex;
          const linhas = visiveis
            .map((p) => `${p.marker} ${p.seriesName}: ${config.formatar(p.value)}`)
            .join("<br/>");
          const total = totais[idx]?.[config.campo];
          return (
            `<strong>${visiveis[0].axisValueLabel}</strong><br/>${linhas}` +
            (total !== undefined
              ? `<br/><strong>${ROTULO_TOTAL}: ${config.formatar(total)}</strong>`
              : "")
          );
        },
      },
      legend: { bottom: 4, data: ESFERAS_EMPILHADAS.map((e) => rotuloEsfera[e] ?? e) },
      xAxis: {
        type: "category",
        data: anos,
        axisLabel: { interval: 0, rotate: 45 },
      },
      yAxis: { type: "value", name: config.rotulo, nameLocation: "middle", nameGap: 50 },
      series: [...seriesEmpilhadas, serieTotal],
    });
  }, [serie, rotuloEsfera, unidade, titulo]);

  function exportarPng() {
    const instancia = instanciaRef.current;
    if (!instancia) return;
    const url = instancia.getDataURL({ type: "png", pixelRatio: 2, backgroundColor: "#fff" });
    const a = document.createElement("a");
    a.href = url;
    a.download = nomeArquivoPng;
    a.click();
  }

  return (
    <div className="grafico-wrap">
      <div className="tabela-acoes">
        <button type="button" className="botao-secundario" onClick={exportarPng}>
          Exportar PNG
        </button>
      </div>
      <div ref={containerRef} className="grafico-canvas" />
      <p className="aviso-vazio">
        O rótulo no topo de cada barra é o {ROTULO_TOTAL} (soma de União, Estados e
        Municípios).
      </p>
    </div>
  );
}
