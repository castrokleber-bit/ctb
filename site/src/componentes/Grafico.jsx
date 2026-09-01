import { useEffect, useRef } from "react";
import * as echarts from "echarts";
import { UNIDADES } from "../lib/formato";
import { COR_PADRAO } from "../lib/cores";

// Barras horizontais — rótulos de rubrica costumam ser longos ("Contrib. Seg. Serv.
// Público"), barra horizontal evita truncar ou girar o texto. `cor` deixa o chamador
// tingir a barra pela esfera em foco (QuadroPorEsfera) — sem esfera, usa o azul padrão.
// `coresPorRotulo` tinge cada barra individualmente (RD ESFERA, onde cada linha já é
// uma esfera diferente) e tem prioridade sobre `cor` quando o rótulo bate.
export default function Grafico({
  linhas, unidade, titulo, nomeArquivoPng, cor = COR_PADRAO, coresPorRotulo,
}) {
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
    const config = UNIDADES[unidade];
    const ordenadas = [...linhas].sort((a, b) => a[config.campo] - b[config.campo]);
    instancia.setOption({
      title: { text: titulo, left: "center", textStyle: { fontSize: 14 } },
      grid: { left: 180, right: 40, top: 50, bottom: 30 },
      tooltip: {
        trigger: "axis",
        axisPointer: { type: "shadow" },
        valueFormatter: (v) => config.formatar(v),
      },
      xAxis: { type: "value", name: config.rotulo, nameLocation: "middle", nameGap: 30 },
      yAxis: {
        type: "category",
        data: ordenadas.map((l) => l.rotulo),
        axisLabel: { fontSize: 11, width: 170, overflow: "truncate" },
      },
      series: [
        {
          type: "bar",
          data: ordenadas.map((l) => ({
            value: l[config.campo],
            itemStyle: coresPorRotulo?.[l.rotulo] ? { color: coresPorRotulo[l.rotulo] } : undefined,
          })),
          itemStyle: { color: cor },
          label: { show: true, position: "right", formatter: (p) => config.formatar(p.value), fontSize: 11 },
        },
      ],
    });
  }, [linhas, unidade, titulo, cor, coresPorRotulo]);

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
