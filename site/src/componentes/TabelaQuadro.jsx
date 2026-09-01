import { UNIDADES, numero } from "../lib/formato";

// Gera e baixa um CSV a partir das linhas visíveis — sempre com as 4 grandezas, não só
// a unidade selecionada na tela, pra exportação ser útil independente do que a pessoa
// estava olhando.
function exportarCsv(linhas, rotuloColuna, nomeArquivo) {
  const cabecalho = [rotuloColuna, "R$ bilhões", "% do PIB", "% do total", "Per capita (R$)"];
  const corpo = linhas.map((l) => [
    l.rotulo,
    numero(l.valor_bi, 2),
    numero(l.pct_pib, 2),
    numero(l.pct_total, 2),
    numero(l.per_capita, 2),
  ]);
  const csv = [cabecalho, ...corpo]
    .map((linha) => linha.map((v) => `"${String(v).replace(/"/g, '""')}"`).join(";"))
    .join("\r\n");
  const blob = new Blob(["﻿" + csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = nomeArquivo;
  a.click();
  URL.revokeObjectURL(url);
}

export default function TabelaQuadro({ linhas, unidade, rotuloColuna = "Rubrica", nomeArquivo }) {
  const config = UNIDADES[unidade];
  if (!linhas || linhas.length === 0) {
    return <p className="aviso-vazio">Sem dados para este quadro neste ano.</p>;
  }
  return (
    <div className="tabela-wrap">
      <div className="tabela-acoes">
        <button
          type="button"
          className="botao-secundario"
          onClick={() => exportarCsv(linhas, rotuloColuna, nomeArquivo)}
        >
          Exportar CSV
        </button>
      </div>
      <div className="tabela-scroll">
        <table className="tabela-quadro">
          <thead>
            <tr>
              <th>{rotuloColuna}</th>
              <th>{config.rotulo}</th>
            </tr>
          </thead>
          <tbody>
            {linhas.map((linha) => (
              <tr key={linha.rotulo}>
                <td>{linha.rotulo}</td>
                <td className="numero">{config.formatar(linha[config.campo])}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
