import { useEffect, useState } from "react";
import { carregarAno, carregarMetadados } from "../lib/dados";
import { SeletorAno } from "../componentes/Seletores";
import GraficoVariacao from "../componentes/GraficoVariacao";
import { pontosPib, percentual } from "../lib/formato";
import { exportarVariacaoCsv } from "../lib/exportarCsv";

// Une os rótulos de byGOVDetalhado "consolidado" dos dois anos e calcula a diferença em
// pontos do PIB por tributo — o rótulo é o canônico do dicionário (estável entre eras
// do plano de contas, CLAUDE.md §Regras de classificação), por isso dá pra comparar
// anos distantes direto.
function compararAnos(dadosInicial, dadosFinal) {
  const pctInicial = new Map(dadosInicial.quadros.bygov_detalhado.consolidado.map((l) => [l.rotulo, l.pct_pib]));
  const pctFinal = new Map(dadosFinal.quadros.bygov_detalhado.consolidado.map((l) => [l.rotulo, l.pct_pib]));
  const rotulos = new Set([...pctInicial.keys(), ...pctFinal.keys()]);
  const linhas = [...rotulos]
    .map((rotulo) => {
      const inicial = pctInicial.get(rotulo) ?? 0;
      const final = pctFinal.get(rotulo) ?? 0;
      return { rotulo, pctBase: inicial, pctUltimo: final, delta: final - inicial };
    })
    .sort((a, b) => b.delta - a.delta);
  return { deltaTotal: dadosFinal.total_geral.pct_pib - dadosInicial.total_geral.pct_pib, linhas };
}

// Variação por esfera (União/Estados/Municípios) — AD ESFERA (`dadosAno.ad_esfera`) e
// RD ESFERA (`dadosAno.rd_esfera.por_esfera`) já têm pct_pib por esfera calculado na
// publicação; aqui é só a diferença entre os dois anos. Ordem U/E/M — `GraficoVariacao`
// inverte pra desenhar, então a União acaba no topo do gráfico.
function compararPorEsfera(mapaInicial, mapaFinal, rotuloEsfera) {
  if (!mapaInicial || !mapaFinal) return null;
  return ["U", "E", "M"].map((esf) => ({
    rotulo: rotuloEsfera[esf],
    delta: mapaFinal[esf].pct_pib - mapaInicial[esf].pct_pib,
  }));
}

export default function Variacao() {
  const [metadados, setMetadados] = useState(null);
  const [anoInicial, setAnoInicial] = useState(null);
  const [anoFinal, setAnoFinal] = useState(null);
  const [dadosInicial, setDadosInicial] = useState(null);
  const [dadosFinal, setDadosFinal] = useState(null);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    carregarMetadados()
      .then((m) => {
        setMetadados(m);
        // Default: último ano publicado vs ano anterior.
        const anos = m.anos_disponiveis;
        setAnoFinal(anos[anos.length - 1]);
        setAnoInicial(anos[Math.max(0, anos.length - 2)]);
      })
      .catch((e) => setErro(String(e)));
  }, []);

  useEffect(() => {
    if (anoInicial === null || anoFinal === null) return;
    setDadosInicial(null);
    setDadosFinal(null);
    Promise.all([carregarAno(anoInicial), carregarAno(anoFinal)])
      .then(([di, df]) => {
        setDadosInicial(di);
        setDadosFinal(df);
      })
      .catch((e) => setErro(String(e)));
  }, [anoInicial, anoFinal]);

  if (erro) return <p className="aviso-erro">Erro carregando dados: {erro}</p>;
  if (!metadados) return <p>Carregando…</p>;

  const anos = metadados.anos_disponiveis;
  if (anos.length < 2) {
    return <p className="aviso-vazio">Série com menos de dois anos publicados — sem base de comparação.</p>;
  }

  const rotuloEsfera = metadados.rotulo_esfera;

  return (
    <div>
      <div className="barra-controles">
        <SeletorAno anos={anos} anoSelecionado={anoInicial ?? anos[0]} aoMudar={setAnoInicial} rotulo="Ano inicial" />
        <SeletorAno anos={anos} anoSelecionado={anoFinal ?? anos[anos.length - 1]} aoMudar={setAnoFinal} rotulo="Ano final" />
      </div>

      {anoInicial === anoFinal ? (
        <p className="aviso-vazio">Escolha dois anos diferentes para comparar.</p>
      ) : !dadosInicial || !dadosFinal ? (
        <p>Carregando…</p>
      ) : (
        <ConteudoVariacao
          anoInicial={anoInicial}
          anoFinal={anoFinal}
          dadosInicial={dadosInicial}
          dadosFinal={dadosFinal}
          rotuloEsfera={rotuloEsfera}
        />
      )}
    </div>
  );
}

function ConteudoVariacao({ anoInicial, anoFinal, dadosInicial, dadosFinal, rotuloEsfera }) {
  const resultado = compararAnos(dadosInicial, dadosFinal);
  const porEsferaAd = compararPorEsfera(dadosInicial.ad_esfera, dadosFinal.ad_esfera, rotuloEsfera);
  const porEsferaRd = compararPorEsfera(
    dadosInicial.rd_esfera?.por_esfera,
    dadosFinal.rd_esfera?.por_esfera,
    rotuloEsfera
  );

  return (
    <div>
      <div className="cartoes-variacao">
        <div className="cartao-variacao">
          <span className="rotulo">{anoFinal} vs {anoInicial}</span>
          <span className={`valor ${resultado.deltaTotal >= 0 ? "alta" : "queda"}`}>
            {pontosPib(resultado.deltaTotal, 2)}
          </span>
          <span className="contexto">
            de {percentual(dadosInicial.total_geral.pct_pib, 2)} para{" "}
            {percentual(dadosFinal.total_geral.pct_pib, 2)} do PIB
          </span>
        </div>
      </div>

      <h3 className="subtitulo">Variação por esfera de governo</h3>
      <div className="duas-colunas">
        <GraficoVariacao
          linhas={porEsferaAd}
          titulo={`Arrecadação Direta — ${anoFinal} vs ${anoInicial}`}
          nomeArquivoPng={`variacao_ad_esfera_${anoInicial}_${anoFinal}.png`}
          altura="220px"
          margemEsquerda={110}
        />
        {porEsferaRd ? (
          <GraficoVariacao
            linhas={porEsferaRd}
            titulo={`Receita Disponível — ${anoFinal} vs ${anoInicial}`}
            nomeArquivoPng={`variacao_rd_esfera_${anoInicial}_${anoFinal}.png`}
            altura="220px"
            margemEsquerda={110}
          />
        ) : (
          <p className="aviso-vazio">
            RD ESFERA não calculado para {anoInicial} ou {anoFinal}.
          </p>
        )}
      </div>

      <h3 className="subtitulo">Tributos que mais explicam a variação</h3>
      <GraficoVariacao
        linhas={resultado.linhas}
        titulo={`Variação da carga por tributo — ${anoFinal} vs ${anoInicial}`}
        nomeArquivoPng={`variacao_carga_${anoInicial}_${anoFinal}.png`}
      />

      <div className="tabela-wrap">
        <div className="tabela-acoes">
          <button
            type="button"
            className="botao-secundario"
            onClick={() =>
              exportarVariacaoCsv(
                resultado.linhas,
                String(anoInicial),
                String(anoFinal),
                `variacao_carga_${anoInicial}_${anoFinal}.csv`
              )
            }
          >
            Exportar CSV
          </button>
        </div>
        <div className="tabela-scroll">
          <table className="tabela-quadro">
            <thead>
              <tr>
                <th>Rubrica</th>
                <th>% PIB {anoInicial}</th>
                <th>% PIB {anoFinal}</th>
                <th>Variação</th>
              </tr>
            </thead>
            <tbody>
              {resultado.linhas.map((l) => (
                <tr key={l.rotulo}>
                  <td>{l.rotulo}</td>
                  <td className="numero">{percentual(l.pctBase, 2)}</td>
                  <td className="numero">{percentual(l.pctUltimo, 2)}</td>
                  <td className="numero">{pontosPib(l.delta, 2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <p className="aviso-vazio">
        Ranking pelo rótulo canônico do dicionário de classificação — estável entre as
        eras do plano de contas, por isso {anoInicial} e {anoFinal} são comparáveis
        direto. A soma das variações por tributo bate com a variação total da carga
        mostrada acima, ao arredondamento.
      </p>
    </div>
  );
}
