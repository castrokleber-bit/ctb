import { useEffect, useState } from "react";
import { carregarMetadados, carregarMetodologia } from "../lib/dados";

const ROTULO_ESFERA_FIXO = { U: "União", E: "Estados", M: "Municípios" };

export default function Metodologia() {
  const [metodologia, setMetodologia] = useState(null);
  const [metadados, setMetadados] = useState(null);
  const [esfera, setEsfera] = useState("U");
  const [erro, setErro] = useState(null);

  useEffect(() => {
    Promise.all([carregarMetodologia(), carregarMetadados()])
      .then(([m, md]) => {
        setMetodologia(m);
        setMetadados(md);
      })
      .catch((e) => setErro(String(e)));
  }, []);

  if (erro) return <p className="aviso-erro">Erro carregando metodologia: {erro}</p>;
  if (!metodologia) return <p>Carregando…</p>;

  const linhas = metodologia[esfera] ?? [];

  return (
    <div>
      <h2>Metodologia</h2>
      <p>
        A carga tributária é calculada a partir de um <strong>dicionário versionado</strong>{" "}
        que mapeia cada conta do plano de contas da DCA (Siconfi/Tesouro Nacional) a uma
        rubrica de publicação. A tabela abaixo é gerada direto desse dicionário — não é um
        texto solto que pode dessincronizar do que o pipeline realmente aplica.
      </p>
      <p>
        Cada rubrica é publicada como <strong>receita líquida</strong> (Receitas Brutas
        Realizadas ± Outras Deduções da Receita — o sinal da operação varia por esfera, ver
        a coluna "conta"). Contas com vigência encerrada (<code>vigência fim</code>{" "}
        preenchida) valeram só até aquele ano — o plano de contas da DCA mudou pelo menos
        três vezes entre 2016 e 2025.
      </p>

      <div className="abas-esfera">
        {Object.keys(ROTULO_ESFERA_FIXO).map((e) => (
          <button
            key={e}
            type="button"
            className={e === esfera ? "aba-ativa" : "aba"}
            onClick={() => setEsfera(e)}
          >
            {(metadados?.rotulo_esfera ?? ROTULO_ESFERA_FIXO)[e]}
          </button>
        ))}
      </div>

      <div className="tabela-scroll">
        <table className="tabela-quadro tabela-metodologia">
          <thead>
            <tr>
              <th>Conta DCA</th>
              <th>Rubrica</th>
              <th>Tributo / descrição</th>
              <th>Base de incidência</th>
              <th>Bloco</th>
              <th>Vigência</th>
              <th>Observação</th>
            </tr>
          </thead>
          <tbody>
            {linhas.map((l) => (
              <tr key={`${l.cod_conta}-${l.vigencia_inicio}`}>
                <td className="mono">{l.cod_conta}</td>
                <td>{l.rubrica}</td>
                <td>{l.tributo}</td>
                <td>{l.base_incidencia}</td>
                <td>{ROTULO_ESFERA_FIXO[l.bloco] ?? l.bloco}</td>
                <td>
                  {l.vigencia_inicio}–{l.vigencia_fim ?? "atual"}
                </td>
                <td className="observacao">{l.observacao}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
