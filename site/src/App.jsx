import { useState } from "react";
import Quadros from "./paginas/Quadros";
import SerieHistorica from "./paginas/SerieHistorica";
import Metodologia from "./paginas/Metodologia";

const PAGINAS = [
  { chave: "quadros", rotulo: "Quadros", componente: Quadros },
  { chave: "serie_historica", rotulo: "Série Histórica", componente: SerieHistorica },
  { chave: "metodologia", rotulo: "Metodologia", componente: Metodologia },
];

export default function App() {
  const [pagina, setPagina] = useState("quadros");
  const Conteudo = PAGINAS.find((p) => p.chave === pagina).componente;

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
        Elaboração própria. Fontes: Siconfi/Tesouro Nacional (DCA), IBGE (SIDRA), Caixa
        Econômica Federal (FGTS), Receita Federal/Cetad (Sistema S).
      </footer>
    </div>
  );
}
