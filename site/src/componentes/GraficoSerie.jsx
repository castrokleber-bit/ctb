import { useEffect, useRef } from "react";
import * as echarts from "echarts";
import { UNIDADES } from "../lib/formato";

const CORES = {
  U: "#1f5e9e",
  E: "#e07b39",
  M: "#3c9d5f",
  consolidado: "#8b3a9e",
};

// Linha do tempo, uma série por esfera (+ consolidado) — complemento de `Grafico.jsx`
// (que é por rubrica, um ano só) para a visão intertemporal.
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
    const esferas = Object.keys(serie);
    const anos = serie[esferas[0]]?.map((p) => p.ano) ?? [];
    instancia.setOption({
      title: { text: titulo, left: "center", textStyle: { fontSize: 14 } },
      grid: { left: 70, right: 30, top: 60, bottom: 60 },
      tooltip: { trigger: "axis", valueFormatter: (v) => config.formatar(v) },
      legend: { top: 30, data: esferas.map((e) => rotuloEsfera[e] ?? e) },
      xAxis: { type: "category", data: anos },
      yAxis: { type: "value", name: config.rotulo, nameLocation: "middle", nameGap: 50 },
      series: esferas.map((esf) => ({
        name: rotuloEsfera[esf] ?? esf,
        type: "line",
        data: serie[esf].map((p) => p[config.campo]),
        itemStyle: { color: CORES[esf] },
        lineStyle: { width: esf === "consolidado" ? 3 : 2 },
      })),
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
    </div>
  );
}
