import { useEffect, useRef } from "react";
import * as echarts from "echarts";
import { pontosPib } from "../lib/formato";
import { COR_ALTA, COR_QUEDA } from "../lib/cores";

// Barra horizontal divergente (eixo zero ao centro) — usada tanto pro ranking de
// tributos (muitas linhas, `altura` maior) quanto pra variação por esfera (3 linhas,
// `altura` menor). `linhas` já vem ordenada pelo chamador; aqui só desenha.
export default function GraficoVariacao({ linhas, titulo, nomeArquivoPng, altura, margemEsquerda = 190 }) {
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
    if (!instancia || !linhas) return;
    // ECharts empilha categorias de baixo pra cima — inverte pra maior alta ficar no topo.
    const ordenadas = [...linhas].reverse();
    instancia.setOption({
      title: { text: titulo, left: "center", textStyle: { fontSize: 14 } },
      grid: { left: margemEsquerda, right: 60, top: 50, bottom: 30 },
      tooltip: {
        trigger: "axis",
        axisPointer: { type: "shadow" },
        valueFormatter: (v) => pontosPib(v, 2),
      },
      xAxis: { type: "value", name: "p.p. do PIB", nameLocation: "middle", nameGap: 30 },
      yAxis: {
        type: "category",
        data: ordenadas.map((l) => l.rotulo),
        axisLabel: { fontSize: 11, width: 180, overflow: "truncate" },
      },
      series: [
        {
          type: "bar",
          data: ordenadas.map((l) => ({
            value: l.delta,
            itemStyle: { color: l.delta >= 0 ? COR_ALTA : COR_QUEDA },
            label: { position: l.delta >= 0 ? "right" : "left" },
          })),
          label: {
            show: true,
            formatter: (p) => pontosPib(p.value, 2),
            fontSize: 10,
          },
        },
      ],
    });
  }, [linhas, titulo, margemEsquerda]);

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
      <div
        ref={containerRef}
        className="grafico-canvas grafico-variacao"
        style={altura ? { height: altura } : undefined}
      />
    </div>
  );
}
