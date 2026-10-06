import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import MiniSearch from 'minisearch';
import { excerpt, highlightRanges, indexOptions, queryTerms, runSearch } from '../assets/search-core.js';

const root = fileURLToPath(new URL('..', import.meta.url));
const doc = (slug, title, blocks, date = '2026-10-01', kind = 'meditations') => ({
  key: `${kind}:${slug}`, slug, kind, title, date, url: kind === 'logs' ? `/logs/${slug}/` : `/${slug}/`, postId: slug, blocks,
});
const body = (text) => ({ kind: 'body', text });
const heading = (text) => ({ kind: 'heading', text });
function build(documents) {
  const result = spawnSync(process.execPath, ['scripts/build_search.mjs'], {
    cwd: root, input: JSON.stringify(documents), encoding: 'utf8',
  });
  assert.equal(result.status, 0, result.stderr);
  const payload = JSON.parse(result.stdout);
  return { payload, bytes: result.stdout, engine: MiniSearch.loadJSON(JSON.stringify(payload.index), indexOptions) };
}
const ids = (fixture, query) => runSearch(fixture.engine, query, fixture.payload.documents).map((result) => fixture.payload.documents[result.id].slug);

test('normalization handles canonical and compatibility Unicode without erasing word boundaries', () => {
  assert.deepEqual(queryTerms('CAFÉ cafe\u0301 ＡＢＣ ﬃ 中文 १२३ C++ C# foo_bar foo-bar Don’t don\'t'),
    ['abc', 'bar', 'c#', 'c++', 'café', "don't", 'ffi', 'foo', '१२३', '中文']);
  assert.deepEqual(queryTerms('---___ 😀 !'), []);
  assert.deepEqual(queryTerms('alpha AND "beta" -gamma'), ['alpha', 'and', 'beta', 'gamma']);
});

test('AND spans fields; short words are exact; prefixes need three codepoints; no fuzzy or stemming', () => {
  const fixture = build([
    doc('cross', 'Graph', [heading('Neural systems'), body('on 中文字 𐐀𐐁𐐂')]),
    doc('one-term', 'Graph', [body('unrelated')]),
    doc('short-prefix', 'Only', [body('graphic neurals')]),
  ]);
  assert.deepEqual(ids(fixture, 'graph neu'), ['cross', 'short-prefix']);
  assert.deepEqual(ids(fixture, 'on'), ['cross']);
  assert.deepEqual(ids(fixture, 'ne'), []);
  assert.deepEqual(ids(fixture, '中文'), []);
  assert.deepEqual(ids(fixture, '中文字'), ['cross']);
  assert.deepEqual(ids(fixture, '𐐀𐐁'), []);
  assert.deepEqual(ids(fixture, '𐐀𐐁𐐂'), ['cross']);
  assert.deepEqual(ids(fixture, 'grph'), []);
  assert.deepEqual(ids(fixture, 'systems'), ['cross']);
  assert.deepEqual(ids(fixture, 'systematic'), []);
  assert.deepEqual(ids(fixture, 'graph graph'), ids(fixture, 'graph'));
  assert.deepEqual(ids(fixture, '---'), []);
});

test('title ranks above heading above body without double-counting headings', () => {
  const fixture = build([
    doc('title', 'Needle', [heading('Other'), body('Other')]),
    doc('heading', 'Other', [heading('Needle'), body('Other')]),
    doc('body', 'Other', [heading('Other'), body('Needle')]),
  ]);
  assert.deepEqual(ids(fixture, 'needle'), ['title', 'heading', 'body']);
  const scores = runSearch(fixture.engine, 'needle', fixture.payload.documents).map((result) => result.score);
  assert.ok(scores[0] > scores[1] && scores[1] > scores[2]);
  assert.ok(Math.abs(scores[0] / scores[1] - 2.5) < 1e-10);
  assert.ok(Math.abs(scores[1] / scores[2] - 2) < 1e-10);
});

test('equal scores break ties by newest date and binary slug', () => {
  const fixture = build([
    doc('z', 'Needle', [], '2026-10-02'),
    doc('a', 'Needle', [], '2026-10-02'),
    doc('A', 'Needle', [], '2026-10-02'),
    doc('old', 'Needle', [], '2026-10-01'),
  ]);
  assert.deepEqual(ids(fixture, 'needle'), ['A', 'a', 'z', 'old']);
});

test('serialized build is input-order-independent and restores actual search behavior', () => {
  const documents = [
    doc('z', 'Compiler', [{ kind: 'code', text: 'value_cache C++ C#' }]),
    doc('a', 'Math', [body('café vector')]),
  ];
  const first = build(documents);
  const second = build([...documents].reverse());
  assert.equal(first.bytes, second.bytes);
  assert.deepEqual(first.payload.documents, Object.fromEntries([...documents].reverse().map((document) => [document.key, document])));
  assert.deepEqual(ids(first, 'cache C++'), ['z']);
  assert.deepEqual(ids(first, 'compiler C#'), ['z']);
  assert.deepEqual(ids(first, 'cafe\u0301 vec'), ['a']);
});

test('same-slug sources remain distinct and filtering retains global ranking', () => {
  const fixture = build([
    doc('shared', 'Needle', [body('archive')], '2026-10-02', 'meditations'),
    doc('shared', 'Needle', [body('archive')], '2026-10-01', 'logs'),
  ]);
  const search = kind => runSearch(fixture.engine, 'needle archive', fixture.payload.documents, kind);
  assert.deepEqual(search('all').map(result => result.id), ['meditations:shared', 'logs:shared']);
  for (const kind of ['meditations', 'logs']) {
    const filtered = search(kind);
    assert.deepEqual(filtered.map(result => result.id), [`${kind}:shared`]);
    assert.equal(filtered[0].score, search('all').find(result => result.id === filtered[0].id).score);
  }
  assert.deepEqual(search('invalid'), search('all'));
});

test('raw highlights preserve UTF-16 spans and entire prefix tokens across Unicode normalization', () => {
  const text = '😀 Cafe\u0301 DON’T ＡＢＣＤ ﬃ C++ C# alpha_beta';
  const ranges = highlightRanges(text, queryTerms("café don't abc ffi C++ C# beta"));
  assert.deepEqual(ranges.map(({ start, end }) => text.slice(start, end)),
    ['Cafe\u0301', 'DON’T', 'ＡＢＣＤ', 'ﬃ', 'C++', 'C#', 'beta']);
  assert.equal(ranges[0].start, 3);
  assert.deepEqual(highlightRanges('cat concatenate catapult', queryTerms('cat')),
    [{ start: 0, end: 3 }, { start: 16, end: 24 }]);
  assert.deepEqual(highlightRanges('on only', queryTerms('on')), [{ start: 0, end: 2 }]);
});

test('excerpt prefers distinct coverage, then exact counts, then earliest block', () => {
  const document = doc('excerpt', 'Title', [
    body('alpha alpha alpha'),
    body('alphabet betamax'),
    { kind: 'code', text: 'alpha beta = first' },
    body('alpha beta = later'),
  ]);
  const result = excerpt(document, queryTerms('alpha beta'));
  assert.equal(result.text, 'alpha beta = first');
  assert.deepEqual(result.ranges, [{ start: 0, end: 5 }, { start: 6, end: 10 }]);
});

test('excerpt chooses matching window without crossing blocks or splitting astral characters', () => {
  const text = '😀 '.repeat(160) + 'alpha beta ' + 'tail '.repeat(100);
  const result = excerpt(doc('window', 'Title', [body(text), body('alpha')]), queryTerms('alpha beta'));
  assert.ok(result.text.includes('alpha beta'));
  assert.ok([...result.text].length <= 222);
  assert.ok(!/[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]/u.test(result.text));
  assert.deepEqual(result.ranges.map(({ start, end }) => result.text.slice(start, end)), ['alpha', 'beta']);
});

test('title-only matches show opening body, with no invented highlight or block joining', () => {
  const document = doc('opening', 'Title-only needle', [heading('Heading'), body('Opening paragraph.'), body('Second paragraph.')]);
  assert.deepEqual(excerpt(document, queryTerms('needle')), { text: 'Opening paragraph.', ranges: [] });
  assert.deepEqual(excerpt(doc('empty', 'Needle', []), queryTerms('needle')), { text: '', ranges: [] });
});

test('excerpt keeps complete words at both cut edges, including opening-body fallbacks', () => {
  const text = 'beforeword '.repeat(30) + 'needle ' + 'afterword '.repeat(40);
  for (const terms of [queryTerms('needle'), queryTerms('titleonly')]) {
    const result = excerpt(doc('boundaries', 'Titleonly', [body(text)]), terms);
    const words = result.text.replace(/^…|…$/g, '').trim().split(/\s+/u);
    assert.ok(words.every(word => ['beforeword', 'needle', 'afterword'].includes(word)));
    assert.ok([...result.text].length <= 222);
    if (terms[0] === 'needle') assert.deepEqual(result.ranges.map(({ start, end }) => result.text.slice(start, end)), ['needle']);
  }
});
