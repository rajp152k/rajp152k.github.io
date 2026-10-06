import { build } from 'esbuild';
import { dirname, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
if (process.argv.length !== 3) throw new Error('Usage: node scripts/build_assets.mjs OUTPUT_DIRECTORY');
const outdir = resolve(process.argv[2]);
const entries = { index: 'assets/index.js', search: 'assets/search.js', article: 'assets/article.js', style: 'assets/site.css' };
const result = await build({
  absWorkingDir: root,
  entryPoints: Object.values(entries),
  outdir,
  bundle: true,
  splitting: true,
  minify: true,
  format: 'esm',
  target: 'es2020',
  entryNames: '[name].[hash]',
  assetNames: '[name].[hash]',
  loader: { '.ttf': 'file' },
  metafile: true,
  logLevel: 'warning',
});
const manifest = {};
for (const [key, entry] of Object.entries(entries)) {
  const output = Object.entries(result.metafile.outputs).find(([, metadata]) =>
    metadata.entryPoint && resolve(root, metadata.entryPoint) === resolve(root, entry));
  if (!output) throw new Error(`Missing built entry point: ${entry}`);
  manifest[key] = '/' + relative(outdir, resolve(root, output[0])).split('\\').join('/');
}
process.stdout.write(JSON.stringify(manifest) + '\n');
