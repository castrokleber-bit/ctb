import { numero, pontosPib } from "./formato";

function baixarCsv(cabecalho, corpo, nomeArquivo) {
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

// byGOVDetalhado de todas as esferas num único CSV — mesmo espírito do CTB2024.xlsx
// original, que tinha União/Estados/Municípios lado a lado numa aba só. Não inclui
// "consolidado": ele soma rótulos repetidos entre esferas, e misturar isso com as
// linhas por esfera no mesmo arquivo duplicaria valor pra quem somar a coluna toda.
export function exportarBygovTudo(dadosPorEsfera, rotuloEsfera, ano, nomeArquivo) {
  const cabecalho = ["Esfera", "Rubrica", "R$ bilhões", "% do PIB", "% do total", "Per capita (R$)"];
  const corpo = ["U", "E", "M"].flatMap((esf) =>
    (dadosPorEsfera[esf] ?? []).map((l) => [
      rotuloEsfera[esf],
      l.rotulo,
      numero(l.valor_bi, 2),
      numero(l.pct_pib, 2),
      numero(l.pct_total, 2),
      numero(l.per_capita, 2),
    ])
  );
  baixarCsv(cabecalho, corpo, nomeArquivo);
}

// Ranking de variação de carga por tributo (Variação da Carga) — % do PIB nos dois
// anos comparados e a diferença em pontos do PIB.
export function exportarVariacaoCsv(linhas, rotuloBase, rotuloUltimo, nomeArquivo) {
  const cabecalho = ["Rubrica", `% do PIB (${rotuloBase})`, `% do PIB (${rotuloUltimo})`, "Variação (p.p. do PIB)"];
  const corpo = linhas.map((l) => [l.rotulo, numero(l.pctBase, 2), numero(l.pctUltimo, 2), pontosPib(l.delta, 2)]);
  baixarCsv(cabecalho, corpo, nomeArquivo);
}
