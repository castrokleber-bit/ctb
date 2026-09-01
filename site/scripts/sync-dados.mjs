// Copia dados/publicado/*.json (escrito por `uv run ctb publicar`) para site/public/dados/,
// onde o Vite serve como asset estático. Site não lê nada fora de public/ em runtime.
import { existsSync, mkdirSync, readdirSync, copyFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const aqui = dirname(fileURLToPath(import.meta.url));
const origem = join(aqui, "..", "..", "dados", "publicado");
const destino = join(aqui, "..", "public", "dados");

if (!existsSync(origem)) {
  console.error(`Não encontrei ${origem} — rode "uv run ctb publicar" antes.`);
  process.exit(1);
}

mkdirSync(destino, { recursive: true });
const arquivos = readdirSync(origem).filter((f) => f.endsWith(".json"));
for (const arquivo of arquivos) {
  copyFileSync(join(origem, arquivo), join(destino, arquivo));
}
console.log(`${arquivos.length} arquivo(s) copiado(s) de dados/publicado/ para site/public/dados/`);
