// Aviso de proveniência pros anos 2000-2015 (fonte_dados: "ctb_resumo_legado") — vêm
// direto do CTB-Resumo.xlsx, não recalculados pela metodologia automatizada deste
// projeto (Siconfi/DCA, 2016+). Ver manual/README.md §ctb_resumo_*.csv.
export default function NotaFonteLegado({ fonteDados, ano }) {
  if (fonteDados !== "ctb_resumo_legado") return null;
  return (
    <aside className="nota-legado">
      <strong>{ano} é da série histórica antiga</strong> — extraído direto do
      CTB-Resumo.xlsx, sem passar pela metodologia automatizada deste projeto (que cobre
      2016 em diante, a partir do Siconfi/DCA). A linha "Multas e Dívida Ativa" existe
      até 2015 e desaparece em 2016 porque passa a ser redistribuída nas rubricas de
      origem — não é queda real de arrecadação.
    </aside>
  );
}
