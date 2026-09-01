import { numero, percentual } from "../lib/formato";

export default function NotaCobertura({ cobertura, gapFgtsSistemaS }) {
  if (!cobertura) return null;
  return (
    <aside className="nota-cobertura">
      <strong>Cobertura da imputação municipal:</strong>{" "}
      {numero(cobertura.declarantes)} de {numero(cobertura.total_municipios)} municípios
      declararam ({percentual(cobertura.pct_populacao_coberta)} da população coberta) —{" "}
      {numero(cobertura.imputados)} municípios imputados por média per capita da faixa
      populacional ({percentual(cobertura.pct_receita_imputada, 3)} da receita municipal).
      {gapFgtsSistemaS && (
        <>
          {" "}
          <strong>FGTS e Sistema S ainda não têm fonte para este ano</strong> — o total
          geral fica abaixo do que seria com os dois incluídos.
        </>
      )}
    </aside>
  );
}
