import TabelaQuadro from "./TabelaQuadro";
import Grafico from "./Grafico";
import DiagramaFluxo from "./DiagramaFluxo";
import { reaisBi } from "../lib/formato";
import { CORES_ESFERA } from "../lib/cores";

const BLOCOS = [
  { chave: "uniao_estados", titulo: "União → Estados" },
  { chave: "uniao_municipios", titulo: "União → Municípios" },
  { chave: "estados_municipios", titulo: "Estados → Municípios" },
];

export default function QuadroRdEsfera({ rdEsfera, adEsfera, rotuloEsfera, unidade, ano }) {
  if (!rdEsfera) {
    return (
      <p className="aviso-vazio">
        RD ESFERA não calculado para {ano} — fora do intervalo coberto por
        `pipeline/dominio/rd_esfera.py`.
      </p>
    );
  }
  const linhasPorEsfera = Object.values(rdEsfera.por_esfera);
  const coresPorRotulo = Object.fromEntries(
    Object.keys(rdEsfera.por_esfera).map((esf) => [rotuloEsfera[esf], CORES_ESFERA[esf]])
  );

  return (
    <div>
      <h3 className="subtitulo">Fluxo das transferências (AD → RD)</h3>
      <DiagramaFluxo
        adEsfera={adEsfera}
        transferencias={rdEsfera.transferencias}
        rotuloEsfera={rotuloEsfera}
        ano={ano}
      />

      <h3 className="subtitulo">Receita disponível por esfera</h3>
      <Grafico
        linhas={linhasPorEsfera}
        unidade={unidade}
        titulo={`Receita Disponível por Esfera (${ano})`}
        nomeArquivoPng={`rd_esfera_${ano}.png`}
        coresPorRotulo={coresPorRotulo}
      />
      <TabelaQuadro
        linhas={linhasPorEsfera}
        unidade={unidade}
        rotuloColuna="Esfera"
        nomeArquivo={`rd_esfera_${ano}.csv`}
      />
      <h3 className="subtitulo">Transferências constitucionais</h3>
      {BLOCOS.map(({ chave, titulo }) => {
        const itens = rdEsfera.transferencias[chave] ?? [];
        const total = itens.reduce((soma, i) => soma + i.valor_bi, 0);
        return (
          <details key={chave} className="bloco-transferencia">
            <summary>
              {titulo} — <strong>{reaisBi(total)}</strong>
            </summary>
            <table className="tabela-quadro">
              <thead>
                <tr>
                  <th>Modalidade</th>
                  <th>R$ bilhões</th>
                </tr>
              </thead>
              <tbody>
                {itens.map((item) => (
                  <tr key={item.modalidade}>
                    <td>{item.modalidade}</td>
                    <td className="numero">{reaisBi(item.valor_bi)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </details>
        );
      })}
    </div>
  );
}
