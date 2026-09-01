import { useState } from "react";
import Quadros from "./paginas/Quadros";
import Metodologia from "./paginas/Metodologia";

export default function App() {
  const [pagina, setPagina] = useState("quadros");

  return (
    <div className="app">
      <header className="cabecalho">
        <h1>Carga Tributária Brasileira</h1>
        <nav className="nav-principal">
          <button
            type="button"
            className={pagina === "quadros" ? "nav-ativo" : "nav-item"}
            onClick={() => setPagina("quadros")}
          >
            Quadros
          </button>
          <button
            type="button"
            className={pagina === "metodologia" ? "nav-ativo" : "nav-item"}
            onClick={() => setPagina("metodologia")}
          >
            Metodologia
          </button>
        </nav>
      </header>
      <main className="conteudo">{pagina === "quadros" ? <Quadros /> : <Metodologia />}</main>
      <footer className="rodape">
        Elaboração própria. Fontes: Siconfi/Tesouro Nacional (DCA), IBGE (SIDRA), Caixa
        Econômica Federal (FGTS), Receita Federal/Cetad (Sistema S).
      </footer>
    </div>
  );
}
