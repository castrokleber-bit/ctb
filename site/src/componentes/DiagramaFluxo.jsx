import { useEffect, useRef } from "react";
import * as echarts from "echarts";
import { numero } from "../lib/formato";
import { CORES_ESFERA } from "../lib/cores";

const ESFERAS = ["U", "E", "M"];

// Diagrama aluvial (Sankey) — como a arrecadação direta (AD) de cada esfera vira receita
// disponível (RD) depois das transferências constitucionais. Os seis fluxos vêm direto
// dos totais já publicados (AD ESFERA + os três blocos de transferência do RD ESFERA) —
// nenhum valor novo é calculado aqui, só recombinado:
//   União:      retido = AD(U) − (U→E) − (U→M);  transfere (U→E) e (U→M)
//   Estados:    retido = AD(E) − (E→M);           transfere (E→M)
//   Municípios: retido = AD(M) inteiro (não repassa a mais ninguém)
// `pipeline/dominio/rd_esfera.py::calcular` já garante que RD ESFERA conserva o total de
// AD ESFERA (a soma dos seis fluxos abaixo bate exato com a soma de AD e de RD).
export default function DiagramaFluxo({ adEsfera, transferencias, rotuloEsfera, ano }) {
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
    if (!instancia || !adEsfera || !transferencias) return;

    const somar = (lista) => (lista ?? []).reduce((s, t) => s + t.valor_bi, 0);
    const tUE = somar(transferencias.uniao_estados);
    const tUM = somar(transferencias.uniao_municipios);
    const tEM = somar(transferencias.estados_municipios);
    const ad = Object.fromEntries(ESFERAS.map((e) => [e, adEsfera[e].valor_bi]));

    const nomeAd = (esf) => `${rotuloEsfera[esf]} (AD)`;
    const nomeRd = (esf) => `${rotuloEsfera[esf]} (RD)`;

    const nodes = ESFERAS.flatMap((esf) => [
      { name: nomeAd(esf), itemStyle: { color: CORES_ESFERA[esf] } },
      { name: nomeRd(esf), itemStyle: { color: CORES_ESFERA[esf] } },
    ]);

    const links = [
      { source: nomeAd("U"), target: nomeRd("U"), value: ad.U - tUE - tUM },
      { source: nomeAd("U"), target: nomeRd("E"), value: tUE },
      { source: nomeAd("U"), target: nomeRd("M"), value: tUM },
      { source: nomeAd("E"), target: nomeRd("E"), value: ad.E - tEM },
      { source: nomeAd("E"), target: nomeRd("M"), value: tEM },
      { source: nomeAd("M"), target: nomeRd("M"), value: ad.M },
    ].filter((l) => l.value > 0.0005);

    instancia.setOption({
      title: {
        text: `Arrecadação Direta → Receita Disponível (${ano})`,
        left: "center",
        textStyle: { fontSize: 14 },
      },
      tooltip: {
        trigger: "item",
        triggerOn: "mousemove",
        formatter: (p) =>
          p.dataType === "edge"
            ? `${p.data.source.replace(" (AD)", "")} → ${p.data.target.replace(" (RD)", "")}: R$ ${numero(p.data.value, 2)} bi`
            : `${p.name}: R$ ${numero(p.value, 2)} bi`,
      },
      series: [
        {
          type: "sankey",
          data: nodes,
          links,
          nodeGap: 20,
          nodeWidth: 16,
          emphasis: { focus: "adjacency" },
          lineStyle: { color: "source", opacity: 0.35, curveness: 0.45 },
          label: { fontSize: 11, color: "#33414f" },
        },
      ],
    });
  }, [adEsfera, transferencias, rotuloEsfera, ano]);

  function exportarPng() {
    const instancia = instanciaRef.current;
    if (!instancia) return;
    const url = instancia.getDataURL({ type: "png", pixelRatio: 2, backgroundColor: "#fff" });
    const a = document.createElement("a");
    a.href = url;
    a.download = `fluxo_ad_rd_${ano}.png`;
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
        À esquerda, arrecadação direta (AD) por esfera; à direita, receita disponível
        (RD), depois das transferências constitucionais. Valores em R$ bilhões,
        independente da unidade selecionada acima.
      </p>
    </div>
  );
}
