const fs = require('node:fs');
const path = require('node:path');

const mode = process.argv.includes('--local') ? 'local' : 'dependency';
const root = process.cwd();
const source = mode === 'local'
  ? path.resolve(root, '..', 'ssg', 'templates')
  : path.resolve(root, 'node_modules', 'ssg', 'templates');
const target = path.resolve(root, 'templates');

if (!fs.existsSync(source) || !fs.statSync(source).isDirectory()) {
  console.error(`[sync-templates] template source not found: ${source}`);
  process.exit(1);
}

fs.rmSync(target, { recursive: true, force: true });
fs.cpSync(source, target, { recursive: true });
console.log(`[sync-templates] copied ${source} -> ${target}`);
