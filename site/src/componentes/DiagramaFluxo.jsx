import { useEffect, useRef } from "react";
import * as echarts from "echarts";
import { numero } from "../lib/formato";
import { CORES_ESFERA, TOOLTIP_TEMA } from "../lib/cores";

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
function somar(lista) {
  return (lista ?? []).reduce((s, t) => s + t.valor_bi, 0);
}

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

  const tUE = somar(transferencias?.uniao_estados);
  const tUM = somar(transferencias?.uniao_municipios);
  const tEM = somar(transferencias?.estados_municipios);

  useEffect(() => {
    const instancia = instanciaRef.current;
    if (!instancia || !adEsfera || !transferencias) return;

    const ad = Object.fromEntries(ESFERAS.map((e) => [e, adEsfera[e].valor_bi]));

    const nomeAd = (esf) => `${rotuloEsfera[esf]} (AD)`;
    const nomeRd = (esf) => `${rotuloEsfera[esf]} (RD)`;

    // Rótulo default do sankey fica à direita de todo nó, nos dois lados — os da
    // esquerda (AD) acabavam sobre o próprio fluxo em vez de espelhar os da direita
    // (RD) pra fora, deixando o diagrama com mais "peso" visual de um lado. Espelhando
    // AD pra fora à esquerda, os dois lados ganham a mesma folga e o diagrama fica
    // centralizado no card.
    const nodes = ESFERAS.flatMap((esf) => [
      {
        name: nomeAd(esf),
        itemStyle: { color: CORES_ESFERA[esf] },
        label: { position: "left", align: "right" },
      },
      {
        name: nomeRd(esf),
        itemStyle: { color: CORES_ESFERA[esf] },
        label: { position: "right", align: "left" },
      },
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
        top: 8,
        textStyle: { fontSize: 14 },
      },
      tooltip: {
        ...TOOLTIP_TEMA,
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
          top: 56,
          bottom: 24,
          left: 140,
          right: 140,
          data: nodes,
          links,
          nodeGap: 26,
          nodeWidth: 16,
          emphasis: { focus: "adjacency" },
          lineStyle: { color: "source", opacity: 0.35, curveness: 0.45 },
          label: {
            fontSize: 11,
            color: "#33414f",
            formatter: (p) => `${p.name}\nR$ ${numero(p.value, 2)} bi`,
          },
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
      <div ref={containerRef} className="grafico-canvas grafico-fluxo" />
      <div className="fluxo-transferencias">
        <span>
          {rotuloEsfera.U} → {rotuloEsfera.E}: <strong>R$ {numero(tUE, 2)} bi</strong>
        </span>
        <span>
          {rotuloEsfera.U} → {rotuloEsfera.M}: <strong>R$ {numero(tUM, 2)} bi</strong>
        </span>
        <span>
          {rotuloEsfera.E} → {rotuloEsfera.M}: <strong>R$ {numero(tEM, 2)} bi</strong>
        </span>
      </div>
      <p className="aviso-vazio">
        À esquerda, arrecadação direta (AD) por esfera; à direita, receita disponível
        (RD), depois das transferências constitucionais. Rótulos e valores acima em R$
        bilhões, independente da unidade selecionada.
      </p>
    </div>
  );
}
