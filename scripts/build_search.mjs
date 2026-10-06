import MiniSearch from 'minisearch';
import { indexOptions } from '../assets/search-core.js';

let input = '';
for await (const chunk of process.stdin) input += chunk;
const source = JSON.parse(input);
source.sort((a, b) => a.slug < b.slug ? -1 : a.slug > b.slug ? 1 : 0);
const documents = Object.create(null);
const engine = new MiniSearch(indexOptions);
for (const document of source) {
  documents[document.slug] = document;
  engine.add({
    slug: document.slug,
    title: document.title,
    headings: document.blocks.filter((block) => block.kind === 'heading').map((block) => block.text).join('\n'),
    body: document.blocks.filter((block) => block.kind !== 'heading').map((block) => block.text).join('\n'),
  });
}
process.stdout.write(JSON.stringify({
  schemaVersion: 1,
  tokenizerVersion: 'word-prefix-1',
  engineVersion: '7.2.0',
  documents,
  index: engine.toJSON(),
}) + '\n');
