// Lê os JSON estáticos em public/dados/ (escritos por `uv run ctb publicar`,
// sincronizados com `npm run sync-dados`). Sem backend — cache simples em memória
// evita refetch ao trocar de ano e voltar.
const cache = new Map();

async function buscarJson(caminho) {
  if (cache.has(caminho)) return cache.get(caminho);
  const resp = await fetch(caminho);
  if (!resp.ok) {
    throw new Error(`Falha ao carregar ${caminho}: HTTP ${resp.status}`);
  }
  const dados = await resp.json();
  cache.set(caminho, dados);
  return dados;
}

export function carregarMetadados() {
  return buscarJson(`${import.meta.env.BASE_URL}dados/metadados.json`);
}

export function carregarAno(ano) {
  return buscarJson(`${import.meta.env.BASE_URL}dados/${ano}.json`);
}

export function carregarMetodologia() {
  return buscarJson(`${import.meta.env.BASE_URL}dados/metodologia.json`);
}
