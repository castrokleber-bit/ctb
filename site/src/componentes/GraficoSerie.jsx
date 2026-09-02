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
        formatter: (p) => config.formatar(p.value),
      },
      labelLayout: { hideOverlap: true },
    }));

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
    };

    instancia.setOption({
      title: { text: titulo, left: "center", textStyle: { fontSize: 14 } },
      grid: { left: 70, right: 30, top: 60, bottom: 60 },
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
      legend: { top: 30, data: ESFERAS_EMPILHADAS.map((e) => rotuloEsfera[e] ?? e) },
      xAxis: { type: "category", data: anos },
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
