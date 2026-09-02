import { useEffect, useState } from "react";
import { carregarMetadados, carregarSerieHistorica } from "../lib/dados";
import { SeletorUnidade } from "../componentes/Seletores";
import GraficoSerie from "../componentes/GraficoSerie";

const TIPOS = [
  { chave: "ad_esfera", rotulo: "Arrecadação Direta" },
  { chave: "rd_esfera", rotulo: "Receita Disponível" },
];

export default function SerieHistorica() {
  const [metadados, setMetadados] = useState(null);
  const [serie, setSerie] = useState(null);
  const [unidade, setUnidade] = useState("pct_pib");
  const [tipo, setTipo] = useState("ad_esfera");
  const [erro, setErro] = useState(null);

  useEffect(() => {
    Promise.all([carregarMetadados(), carregarSerieHistorica()])
      .then(([m, s]) => {
        setMetadados(m);
        setSerie(s);
      })
      .catch((e) => setErro(String(e)));
  }, []);

  if (erro) return <p className="aviso-erro">Erro carregando dados: {erro}</p>;
  if (!metadados || !serie) return <p>Carregando…</p>;

  const rotuloEsfera = metadados.rotulo_esfera;
  const dadosTipo = serie[tipo];
  const anosComDado = dadosTipo.U?.length ?? 0;
  const tituloTipo = TIPOS.find((t) => t.chave === tipo).rotulo;

  return (
    <div>
      <div className="barra-controles">
        <label className="seletor">
          <span>Quadro</span>
          <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
            {TIPOS.map((t) => (
              <option key={t.chave} value={t.chave}>
                {t.rotulo}
              </option>
            ))}
          </select>
        </label>
        <SeletorUnidade unidadeSelecionada={unidade} aoMudar={setUnidade} />
      </div>

      {tipo === "rd_esfera" && anosComDado < serie.anos_disponiveis.length && (
        <p className="aviso-vazio">
          RD ESFERA cobre {anosComDado} de {serie.anos_disponiveis.length} anos publicados —
          anos fora do intervalo de `pipeline/dominio/rd_esfera.py` ficam de fora do gráfico.
        </p>
      )}

      {anosComDado > 0 ? (
        <GraficoSerie
          serie={dadosTipo}
          rotuloEsfera={rotuloEsfera}
          unidade={unidade}
          titulo={`${tituloTipo} por esfera — série histórica`}
          nomeArquivoPng={`${tipo}_serie_historica.png`}
        />
      ) : (
        <p className="aviso-vazio">Sem anos disponíveis para {tituloTipo}.</p>
      )}

      {serie.anos_legado?.length > 0 && (
        <p className="aviso-vazio">
          {serie.anos_legado[0]}–{serie.anos_legado[serie.anos_legado.length - 1]} vêm do
          CTB-Resumo.xlsx (série antiga), não da metodologia automatizada deste projeto —
          ver Metodologia.
        </p>
      )}
    </div>
  );
}
