import { useEffect, useRef } from "react";
import * as echarts from "echarts";
import { UNIDADES } from "../lib/formato";
import { PALETA_CATEGORICA, matizes } from "../lib/cores";

// Rosca (pizza com furo) — cada fatia é uma linha do quadro. `cor` deixa o chamador
// tingir todas as fatias em tons de uma única cor (QuadroPorEsfera: identidade da
// esfera em foco); sem `cor`, cicla a paleta categórica padrão (quadros sem esfera
// única, como Principais Tributos). `coresPorRotulo` tinge cada fatia individualmente
// e tem prioridade sobre as duas — usado em RD ESFERA, onde cada fatia já é uma esfera.
export default function Grafico({
  linhas, unidade, titulo, nomeArquivoPng, cor, coresPorRotulo,
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
    const ordenadas = [...linhas].sort((a, b) => b[config.campo] - a[config.campo]);
    const tons = cor ? matizes(cor, ordenadas.length) : null;

    instancia.setOption({
      title: { text: titulo, left: "center", textStyle: { fontSize: 14 } },
      tooltip: {
        trigger: "item",
        formatter: (p) => `${p.marker} ${p.name}: ${config.formatar(p.value)} (${p.percent}%)`,
      },
      series: [
        {
          type: "pie",
          radius: ["36%", "70%"],
          center: ["50%", "54%"],
          avoidLabelOverlap: true,
          minShowLabelAngle: 3,
          itemStyle: { borderColor: "#fff", borderWidth: 2 },
          label: {
            formatter: (p) => `${p.name}\n${config.formatar(p.value)}`,
            fontSize: 11,
            color: "#6b7684",
          },
          labelLine: { length: 10, length2: 8 },
          data: ordenadas.map((l, i) => ({
            name: l.rotulo,
            value: l[config.campo],
            itemStyle: {
              color:
                coresPorRotulo?.[l.rotulo] ?? tons?.[i] ?? PALETA_CATEGORICA[i % PALETA_CATEGORICA.length],
            },
          })),
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
      <div ref={containerRef} className="grafico-canvas grafico-pizza" />
    </div>
  );
}
