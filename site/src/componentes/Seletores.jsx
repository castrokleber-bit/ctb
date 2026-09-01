import { UNIDADES } from "../lib/formato";

export function SeletorAno({ anos, anoSelecionado, aoMudar }) {
  return (
    <label className="seletor">
      <span>Ano</span>
      <select value={anoSelecionado} onChange={(e) => aoMudar(Number(e.target.value))}>
        {anos.map((ano) => (
          <option key={ano} value={ano}>
            {ano}
          </option>
        ))}
      </select>
    </label>
  );
}

export function SeletorUnidade({ unidadeSelecionada, aoMudar }) {
  return (
    <label className="seletor">
      <span>Unidade</span>
      <select value={unidadeSelecionada} onChange={(e) => aoMudar(e.target.value)}>
        {Object.entries(UNIDADES).map(([chave, { rotulo }]) => (
          <option key={chave} value={chave}>
            {rotulo}
          </option>
        ))}
      </select>
    </label>
  );
}
