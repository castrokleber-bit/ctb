import { useEffect, useState } from "react";
import Quadros from "./paginas/Quadros";
import SerieHistorica from "./paginas/SerieHistorica";
import Variacao from "./paginas/Variacao";
import Metodologia from "./paginas/Metodologia";
import { carregarMetadados } from "./lib/dados";
import { dataHora } from "./lib/formato";

const PAGINAS = [
  { chave: "quadros", rotulo: "Quadros", componente: Quadros },
  { chave: "serie_historica", rotulo: "Série Histórica", componente: SerieHistorica },
  { chave: "variacao", rotulo: "Variação da Carga", componente: Variacao },
  { chave: "metodologia", rotulo: "Metodologia", componente: Metodologia },
];

export default function App() {
  const [pagina, setPagina] = useState("quadros");
  const [geradoEm, setGeradoEm] = useState(null);
  const Conteudo = PAGINAS.find((p) => p.chave === pagina).componente;

  useEffect(() => {
    carregarMetadados()
      .then((m) => setGeradoEm(m.gerado_em))
      .catch(() => {});
  }, []);

  return (
    <div className="app">
      <header className="cabecalho">
        <h1>Carga Tributária Brasileira</h1>
        <nav className="nav-principal">
          {PAGINAS.map((p) => (
            <button
              key={p.chave}
              type="button"
              className={pagina === p.chave ? "nav-ativo" : "nav-item"}
              onClick={() => setPagina(p.chave)}
            >
              {p.rotulo}
            </button>
          ))}
        </nav>
      </header>
      <main className="conteudo">
        <Conteudo />
      </main>
      <footer className="rodape">
        <p>
          Elaboração própria. Fontes: Siconfi/Tesouro Nacional (DCA), IBGE (SIDRA), Caixa
          Econômica Federal (FGTS), Receita Federal/Cetad (Sistema S).
        </p>
        {geradoEm && <p>Dados atualizados em {dataHora(geradoEm)}.</p>}
        <p className="creditos">
          Desenvolvido por Kleber Pacheco de Castro. Metodologia: José Roberto Afonso.
        </p>
        <p className="aviso-reproducao">
          Em caso de reprodução, total ou parcial, dos dados e análises desta página,
          solicita-se a citação dos autores como fonte.
        </p>
      </footer>
    </div>
  );
}
