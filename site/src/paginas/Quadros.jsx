import { useEffect, useState } from "react";
import { carregarAno, carregarMetadados } from "../lib/dados";
import { SeletorAno, SeletorUnidade } from "../componentes/Seletores";
import QuadroPorEsfera from "../componentes/QuadroPorEsfera";
import QuadroRdEsfera from "../componentes/QuadroRdEsfera";
import TabelaQuadro from "../componentes/TabelaQuadro";
import Grafico from "../componentes/Grafico";
import NotaCobertura from "../componentes/NotaCobertura";
import { reaisBi, percentual } from "../lib/formato";
import { exportarBygovTudo } from "../lib/exportarCsv";

const QUADROS = [
  { chave: "ad_esfera", rotulo: "AD ESFERA" },
  { chave: "bygov_detalhado", rotulo: "byGOVDetalhado" },
  { chave: "principais_tributos", rotulo: "Principais Tributos" },
  { chave: "bases_incidencia", rotulo: "Bases de Incidência" },
  { chave: "rd_esfera", rotulo: "RD ESFERA" },
];

export default function Quadros() {
  const [metadados, setMetadados] = useState(null);
  const [ano, setAno] = useState(null);
  const [dadosAno, setDadosAno] = useState(null);
  const [unidade, setUnidade] = useState("bi");
  const [quadro, setQuadro] = useState("ad_esfera");
  const [erro, setErro] = useState(null);

  useEffect(() => {
    carregarMetadados()
      .then((m) => {
        setMetadados(m);
        setAno(m.anos_disponiveis[m.anos_disponiveis.length - 1]);
      })
      .catch((e) => setErro(String(e)));
  }, []);

  useEffect(() => {
    if (ano === null) return;
    setDadosAno(null);
    carregarAno(ano)
      .then(setDadosAno)
      .catch((e) => setErro(String(e)));
  }, [ano]);

  if (erro) return <p className="aviso-erro">Erro carregando dados: {erro}</p>;
  if (!metadados || !dadosAno) return <p>Carregando…</p>;

  const rotuloEsfera = metadados.rotulo_esfera;

  return (
    <div>
      <div className="barra-controles">
        <SeletorAno anos={metadados.anos_disponiveis} anoSelecionado={ano} aoMudar={setAno} />
        <SeletorUnidade unidadeSelecionada={unidade} aoMudar={setUnidade} />
      </div>

      <div className="resumo-ano">
        <span>
          <strong>Total geral {ano}:</strong> {reaisBi(dadosAno.total_geral.valor_bi)} (
          {percentual(dadosAno.total_geral.pct_pib, 2)} do PIB)
        </span>
        <span>
          PIB corrente: {reaisBi(dadosAno.pib_bi)} (extraído em {dadosAno.data_extracao_pib})
        </span>
      </div>

      <NotaCobertura cobertura={dadosAno.cobertura_imputacao} gapFgtsSistemaS={dadosAno.gap_fgts_sistema_s} />

      <nav className="abas-quadro">
        {QUADROS.map((q) => (
          <button
            key={q.chave}
            type="button"
            className={q.chave === quadro ? "aba-quadro-ativa" : "aba-quadro"}
            onClick={() => setQuadro(q.chave)}
          >
            {q.rotulo}
          </button>
        ))}
      </nav>

      {(quadro === "ad_esfera" || quadro === "bygov_detalhado") && (
        <div>
          {quadro === "bygov_detalhado" && (
            <div className="tabela-acoes">
              <button
                type="button"
                className="botao-secundario"
                onClick={() =>
                  exportarBygovTudo(
                    dadosAno.quadros.bygov_detalhado,
                    rotuloEsfera,
                    ano,
                    `bygov_detalhado_todas_esferas_${ano}.csv`
                  )
                }
              >
                Exportar tudo (todas as esferas)
              </button>
            </div>
          )}
          <QuadroPorEsfera
            dadosPorEsfera={dadosAno.quadros[quadro]}
            rotuloEsfera={rotuloEsfera}
            unidade={unidade}
            ano={ano}
            prefixoArquivo={quadro}
            titulo={QUADROS.find((q) => q.chave === quadro).rotulo}
          />
        </div>
      )}

      {quadro === "principais_tributos" && (
        <div>
          <Grafico
            linhas={dadosAno.quadros.principais_tributos}
            unidade={unidade}
            titulo={`Principais Tributos (${ano})`}
            nomeArquivoPng={`principais_tributos_${ano}.png`}
          />
          <TabelaQuadro
            linhas={dadosAno.quadros.principais_tributos}
            unidade={unidade}
            rotuloColuna="Tributo"
            nomeArquivo={`principais_tributos_${ano}.csv`}
          />
        </div>
      )}

      {quadro === "bases_incidencia" && (
        <div>
          <Grafico
            linhas={dadosAno.quadros.bases_incidencia}
            unidade={unidade}
            titulo={`Bases de Incidência (${ano})`}
            nomeArquivoPng={`bases_incidencia_${ano}.png`}
          />
          <TabelaQuadro
            linhas={dadosAno.quadros.bases_incidencia}
            unidade={unidade}
            rotuloColuna="Base de incidência"
            nomeArquivo={`bases_incidencia_${ano}.csv`}
          />
        </div>
      )}

      {quadro === "rd_esfera" && (
        <QuadroRdEsfera
          rdEsfera={dadosAno.rd_esfera}
          adEsfera={dadosAno.ad_esfera}
          rotuloEsfera={rotuloEsfera}
          unidade={unidade}
          ano={ano}
        />
      )}
    </div>
  );
}
