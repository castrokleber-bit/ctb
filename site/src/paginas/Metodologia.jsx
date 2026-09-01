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

      <section className="conceito-carga">
        <blockquote className="citacao">
          <p>
            O conceito de carga tributária é equivalente à arrecadação de todos os
            tributos coletados no país em proporção ao PIB (produto interno bruto). Ou
            seja, dividindo-se tudo aquilo que o governo arrecada a título de tributos
            pelo valor nominal do PIB em determinado período chega-se a uma medida da
            parcela do produto interno que é apropriada pelo setor público através da
            cobrança de tributos.
          </p>
          <p>
            O significado de um aumento de carga tributária (quando dois períodos
            distintos são comparados) é, portanto, de que a razão arrecadação
            tributária/PIB se elevou.
          </p>
          <p>
            A carga tributária leva com consideração tanto o valor nominal da
            arrecadação quanto o valor nominal do PIB. Assim, uma das condições para que
            haja aumento de carga é que a arrecadação tributária cresça em proporção
            maior que o PIB, não importando os efeitos da inflação sobre a variação da
            arrecadação e do PIB.
          </p>
          <p>
            Por exemplo, quando a economia atravessa um período onde o desempenho da
            atividade é considerado fraco é de se esperar que a carga tributária
            diminua, pois a retração da atividade tende a deprimir a arrecadação. No
            entanto, pode acontecer o oposto. Se o governo encontra caminhos para
            proteger a arrecadação dos efeitos recessivos, haverá aumento de carga
            tributária. Mesmo que o aumento nominal da arrecadação não seja muito grande
            haverá aumento de carga se a variação da receita for maior que a variação do
            produto.
          </p>
          <p>
            É importante destacar que o cálculo da carga tributária aqui apresentado foi
            elaborado com base em estatísticas oficiais de arrecadação e do produto
            recentemente divulgadas pelos órgãos públicos responsáveis por sua
            elaboração. Assim, ainda que a conta não tenha caráter definitivo (seja pela
            revisão dos dados de arrecadação pelos governos, seja pela revisão do valor
            nominal do PIB calculado pelo IBGE), tal indicador não deve sofrer grandes
            alterações. Isto significa que fica frustrada a expectativa de queda
            razoável da carga tributária – exatamente ao contrário do anunciado pelas
            autoridades fazendárias do governo federal.
          </p>
          <p>
            A arrecadação tributária nacional compreende as receitas da União, dos
            estados e do Distrito Federal e dos municípios. Foi adotado o conceito amplo
            da contabilidade, abrangendo todos os impostos, taxas e contribuições –
            previdenciárias, sociais e econômicas – e a dívida ativa. Ou seja, o conceito
            de arrecadação tributária aqui adotado considera como tributo todo tipo de
            receita compulsoriamente obtido da sociedade por cada uma das três esferas
            de governo.
          </p>
          <p className="citacao-fonte">
            KHAIR, ARAUJO e AFONSO, 2005, p.27 —{" "}
            <a
              href="https://www.nepp.unicamp.br/wp-content/uploads/sites/57/2024/10/CadPesq_58.pdf"
              target="_blank"
              rel="noopener noreferrer"
            >
              nepp.unicamp.br
            </a>
          </p>
        </blockquote>
        <p className="nota-fonte">
          A fonte básica utilizada para apuração da carga (DCA) tem origem contábil,
          seguindo as melhores práticas internacionais.
        </p>
      </section>

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
