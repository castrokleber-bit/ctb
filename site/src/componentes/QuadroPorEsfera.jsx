import { useState } from "react";
import TabelaQuadro from "./TabelaQuadro";
import Grafico from "./Grafico";

const ESFERAS = ["U", "E", "M", "consolidado"];

export default function QuadroPorEsfera({ dadosPorEsfera, rotuloEsfera, unidade, ano, prefixoArquivo, titulo }) {
  const [esfera, setEsfera] = useState("U");
  const linhas = dadosPorEsfera[esfera] ?? [];

  return (
    <div>
      <div className="abas-esfera">
        {ESFERAS.map((e) => (
          <button
            key={e}
            type="button"
            className={e === esfera ? "aba-ativa" : "aba"}
            onClick={() => setEsfera(e)}
          >
            {rotuloEsfera[e]}
          </button>
        ))}
      </div>
      <Grafico
        linhas={linhas}
        unidade={unidade}
        titulo={`${titulo} — ${rotuloEsfera[esfera]} (${ano})`}
        nomeArquivoPng={`${prefixoArquivo}_${esfera}_${ano}.png`}
      />
      <TabelaQuadro
        linhas={linhas}
        unidade={unidade}
        rotuloColuna="Rubrica"
        nomeArquivo={`${prefixoArquivo}_${esfera}_${ano}.csv`}
      />
    </div>
  );
}
