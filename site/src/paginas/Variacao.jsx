import { useEffect, useState } from "react";
import { carregarAno, carregarMetadados } from "../lib/dados";
import GraficoVariacao from "../componentes/GraficoVariacao";
import { pontosPib, percentual } from "../lib/formato";
import { exportarVariacaoCsv } from "../lib/exportarCsv";

// Une os rótulos de byGOVDetalhado "consolidado" dos dois anos e calcula a diferença em
// pontos do PIB por tributo — o rótulo é o canônico do dicionário (estável entre eras
// do plano de contas, CLAUDE.md §Regras de classificação), por isso dá pra comparar
// 2016 direto contra 2025 sem remapear nada aqui.
function compararAnos(dadosBase, dadosUltimo) {
  const pctBase = new Map(dadosBase.quadros.bygov_detalhado.consolidado.map((l) => [l.rotulo, l.pct_pib]));
  const pctUltimo = new Map(dadosUltimo.quadros.bygov_detalhado.consolidado.map((l) => [l.rotulo, l.pct_pib]));
  const rotulos = new Set([...pctBase.keys(), ...pctUltimo.keys()]);
  const linhas = [...rotulos]
    .map((rotulo) => {
      const base = pctBase.get(rotulo) ?? 0;
      const ultimo = pctUltimo.get(rotulo) ?? 0;
      return { rotulo, pctBase: base, pctUltimo: ultimo, delta: ultimo - base };
    })
    .sort((a, b) => b.delta - a.delta);
  return { deltaTotal: dadosUltimo.total_geral.pct_pib - dadosBase.total_geral.pct_pib, linhas };
}

// Variação por esfera (União/Estados/Municípios) — AD ESFERA (`dadosAno.ad_esfera`) e
// RD ESFERA (`dadosAno.rd_esfera.por_esfera`) já têm pct_pib por esfera calculado na
// publicação; aqui é só a diferença entre os dois anos. Ordem U/E/M — `GraficoVariacao`
// inverte pra desenhar, então a União acaba no topo do gráfico.
function compararPorEsfera(mapaBase, mapaUltimo, rotuloEsfera) {
  if (!mapaBase || !mapaUltimo) return null;
  return ["U", "E", "M"].map((esf) => ({
    rotulo: rotuloEsfera[esf],
    delta: mapaUltimo[esf].pct_pib - mapaBase[esf].pct_pib,
  }));
}

export default function Variacao() {
  const [metadados, setMetadados] = useState(null);
  const [dados, setDados] = useState(null);
  const [comparacao, setComparacao] = useState("anterior");
  const [erro, setErro] = useState(null);

  useEffect(() => {
    carregarMetadados()
      .then(setMetadados)
      .catch((e) => setErro(String(e)));
  }, []);

  useEffect(() => {
    if (!metadados) return;
    const anos = metadados.anos_disponiveis;
    const anoUltimo = anos[anos.length - 1];
    const anoAnterior = anos[anos.length - 2];
    const anoPrimeiro = anos[0];
    const necessarios = [...new Set([anoUltimo, anoAnterior, anoPrimeiro])];
    Promise.all(necessarios.map((a) => carregarAno(a).then((d) => [a, d])))
      .then((pares) => setDados(Object.fromEntries(pares)))
      .catch((e) => setErro(String(e)));
  }, [metadados]);

  if (erro) return <p className="aviso-erro">Erro carregando dados: {erro}</p>;
  if (!metadados || !dados) return <p>Carregando…</p>;

  const anos = metadados.anos_disponiveis;
  if (anos.length < 2) {
    return <p className="aviso-vazio">Série com menos de dois anos publicados — sem base de comparação.</p>;
  }
  const anoUltimo = anos[anos.length - 1];
  const anoAnterior = anos[anos.length - 2];
  const anoPrimeiro = anos[0];
  const temPrimeiro = anoPrimeiro !== anoAnterior;

  const rotuloEsfera = metadados.rotulo_esfera;
  const montarComparacao = (chave, anoBase) => ({
    chave,
    anoBase,
    resultado: compararAnos(dados[anoBase], dados[anoUltimo]),
    porEsferaAd: compararPorEsfera(dados[anoBase].ad_esfera, dados[anoUltimo].ad_esfera, rotuloEsfera),
    porEsferaRd: compararPorEsfera(
      dados[anoBase].rd_esfera?.por_esfera,
      dados[anoUltimo].rd_esfera?.por_esfera,
      rotuloEsfera
    ),
  });

  const comparacoes = [
    montarComparacao("anterior", anoAnterior),
    ...(temPrimeiro ? [montarComparacao("primeiro", anoPrimeiro)] : []),
  ];
  const atual = comparacoes.find((c) => c.chave === comparacao) ?? comparacoes[0];
  const cAnterior = comparacoes[0];
  const cPrimeiro = comparacoes.find((c) => c.chave === "primeiro");

  return (
    <div>
      <div className="cartoes-variacao">
        <div className="cartao-variacao">
          <span className="rotulo">{anoUltimo} vs {anoAnterior}</span>
          <span className={`valor ${cAnterior.resultado.deltaTotal >= 0 ? "alta" : "queda"}`}>
            {pontosPib(cAnterior.resultado.deltaTotal, 2)}
          </span>
          <span className="contexto">
            de {percentual(dados[anoAnterior].total_geral.pct_pib, 2)} para{" "}
            {percentual(dados[anoUltimo].total_geral.pct_pib, 2)} do PIB
          </span>
        </div>
        {cPrimeiro && (
          <div className="cartao-variacao">
            <span className="rotulo">{anoUltimo} vs {anoPrimeiro}</span>
            <span className={`valor ${cPrimeiro.resultado.deltaTotal >= 0 ? "alta" : "queda"}`}>
              {pontosPib(cPrimeiro.resultado.deltaTotal, 2)}
            </span>
            <span className="contexto">
              de {percentual(dados[anoPrimeiro].total_geral.pct_pib, 2)} para{" "}
              {percentual(dados[anoUltimo].total_geral.pct_pib, 2)} do PIB
            </span>
          </div>
        )}
      </div>

      {temPrimeiro && (
        <div className="barra-controles">
          <label className="seletor">
            <span>Comparação</span>
            <select value={comparacao} onChange={(e) => setComparacao(e.target.value)}>
              <option value="anterior">{anoUltimo} vs {anoAnterior}</option>
              <option value="primeiro">{anoUltimo} vs {anoPrimeiro}</option>
            </select>
          </label>
        </div>
      )}

      <h3 className="subtitulo">Variação por esfera de governo</h3>
      <div className="duas-colunas">
        <GraficoVariacao
          linhas={atual.porEsferaAd}
          titulo={`Arrecadação Direta — ${anoUltimo} vs ${atual.anoBase}`}
          nomeArquivoPng={`variacao_ad_esfera_${atual.anoBase}_${anoUltimo}.png`}
          altura="220px"
          margemEsquerda={110}
        />
        {atual.porEsferaRd ? (
          <GraficoVariacao
            linhas={atual.porEsferaRd}
            titulo={`Receita Disponível — ${anoUltimo} vs ${atual.anoBase}`}
            nomeArquivoPng={`variacao_rd_esfera_${atual.anoBase}_${anoUltimo}.png`}
            altura="220px"
            margemEsquerda={110}
          />
        ) : (
          <p className="aviso-vazio">
            RD ESFERA não calculado para {atual.anoBase} ou {anoUltimo}.
          </p>
        )}
      </div>

      <h3 className="subtitulo">Tributos que mais explicam a variação</h3>
      <GraficoVariacao
        linhas={atual.resultado.linhas}
        titulo={`Variação da carga por tributo — ${anoUltimo} vs ${atual.anoBase}`}
        nomeArquivoPng={`variacao_carga_${atual.anoBase}_${anoUltimo}.png`}
      />

      <div className="tabela-wrap">
        <div className="tabela-acoes">
          <button
            type="button"
            className="botao-secundario"
            onClick={() =>
              exportarVariacaoCsv(
                atual.resultado.linhas,
                String(atual.anoBase),
                String(anoUltimo),
                `variacao_carga_${atual.anoBase}_${anoUltimo}.csv`
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
                <th>% PIB {atual.anoBase}</th>
                <th>% PIB {anoUltimo}</th>
                <th>Variação</th>
              </tr>
            </thead>
            <tbody>
              {atual.resultado.linhas.map((l) => (
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
        eras do plano de contas, por isso {anoPrimeiro} e {anoUltimo} são comparáveis
        direto. A soma das variações por tributo bate com a variação total da carga
        mostrada acima, ao arredondamento.
      </p>
    </div>
  );
}
