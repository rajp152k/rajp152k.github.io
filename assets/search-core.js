const WORD = /[\p{L}\p{N}][\p{L}\p{N}\p{M}]*(?:'[\p{L}\p{N}][\p{L}\p{N}\p{M}]*)*(?:\+\+|#)?/gu;
const normalize = (text) => text.normalize('NFKC').toLowerCase().replace(/[‘’]/g, "'");
const binaryCompare = (a, b) => a < b ? -1 : a > b ? 1 : 0;
const isPrefix = (term) => [...term].length >= 3;

export function tokenize(text) {
  return Array.from(normalize(text).matchAll(WORD), (match) => match[0]);
}

export function queryTerms(raw) {
  return [...new Set(tokenize(raw))].sort(binaryCompare);
}

export const indexOptions = {
  idField: 'key',
  fields: ['title', 'headings', 'body'],
  tokenize,
  processTerm: (term) => term,
  searchOptions: {
    combineWith: 'AND',
    boost: { title: 5, headings: 2, body: 1 },
    prefix: isPrefix,
    fuzzy: false,
  },
};

export function searchKind(value) {
  return value === 'meditations' || value === 'logs' ? value : 'all';
}

export function runSearch(engine, raw, documents, kind = 'all') {
  const terms = queryTerms(raw);
  if (!terms.length) return [];
  const scope = searchKind(kind);
  return engine.search(terms.join(' ')).filter(result => scope === 'all' || documents[result.id].kind === scope).sort((a, b) =>
    b.score - a.score ||
    binaryCompare(documents[b.id].date, documents[a.id].date) ||
    binaryCompare(a.id, b.id));
}

// Graphemes preserve the raw span when NFKC expands a ligature, composes marks,
// or changes a compatibility character. DOM string offsets remain UTF-16.
function matchingTokens(text, terms) {
  if (!terms.length) return [];
  const offsets = [];
  let normalized = '';
  const segments = new Intl.Segmenter(undefined, { granularity: 'grapheme' }).segment(text);
  for (const { segment, index } of segments) {
    const value = segment.normalize('NFKC');
    normalized += value;
    for (let i = 0; i < value.toLowerCase().length; i++) {
      offsets.push({ start: index, end: index + segment.length });
    }
  }
  normalized = normalize(normalized);
  const matches = [];
  for (const match of normalized.matchAll(WORD)) {
    const covered = terms.filter((term) => match[0] === term || (isPrefix(term) && match[0].startsWith(term)));
    if (covered.length) {
      matches.push({
        start: offsets[match.index].start,
        end: offsets[match.index + match[0].length - 1].end,
        terms: covered,
        exact: covered.filter((term) => term === match[0]).length,
      });
    }
  }
  return matches;
}

export function highlightRanges(text, terms) {
  const ranges = [];
  for (const { start, end } of matchingTokens(text, terms)) {
    const last = ranges[ranges.length - 1];
    if (last && start <= last.end) last.end = Math.max(last.end, end);
    else ranges.push({ start, end });
  }
  return ranges;
}

function codepointOffsets(text) {
  const offsets = [0];
  let offset = 0;
  for (const point of text) {
    offset += point.length;
    offsets.push(offset);
  }
  return offsets;
}

function boundedWindow(text, offsets, start, end) {
  const space = (index) => /\s/u.test(text.slice(offsets[index], offsets[index + 1]));
  let first = start;
  let last = end;
  if (first > 0 && !space(first - 1) && !space(first)) {
    while (first < last && !space(first)) first++;
  }
  if (last < offsets.length - 1 && !space(last - 1) && !space(last)) {
    while (last > first && !space(last - 1)) last--;
  }
  while (first < last && space(first)) first++;
  while (last > first && space(last - 1)) last--;
  // A single unbroken token may exceed the cap; retain its bounded raw slice.
  return first < last ? [first, last] : [start, end];
}

export function excerpt(document, terms) {
  const limit = 220;
  let best = null;
  for (const block of document.blocks) {
    const matches = matchingTokens(block.text, terms);
    if (!matches.length) continue;
    const offsets = codepointOffsets(block.text);
    const length = offsets.length - 1;
    const candidates = new Set([0, Math.max(0, length - limit)]);
    for (const match of matches) {
      const start = offsets.indexOf(match.start);
      const end = offsets.indexOf(match.end);
      candidates.add(Math.max(0, start - 60));
      candidates.add(start);
      candidates.add(Math.max(0, end - limit));
    }
    for (const candidate of [...candidates].sort((a, b) => a - b)) {
      const candidateStart = Math.min(candidate, Math.max(0, length - limit));
      const [start, end] = boundedWindow(block.text, offsets, candidateStart, Math.min(length, candidateStart + limit));
      const included = matches.filter((match) => match.start >= offsets[start] && match.end <= offsets[end]);
      const coverage = new Set(included.flatMap((match) => match.terms)).size;
      const exact = included.reduce((sum, match) => sum + match.exact, 0);
      if (!best || coverage > best.coverage || (coverage === best.coverage && exact > best.exact)) {
        best = { text: block.text, offsets, start, end, coverage, exact };
      }
    }
  }
  if (!best || !best.coverage) {
    const block = document.blocks.find((block) => block.kind === 'body') || document.blocks[0];
    if (!block) return { text: '', ranges: [] };
    const offsets = codepointOffsets(block.text);
    const [start, end] = boundedWindow(block.text, offsets, 0, Math.min(limit, offsets.length - 1));
    best = { text: block.text, offsets, start, end };
  }
  const { text, offsets, start, end } = best;
  const leading = start > 0 ? '…' : '';
  const trailing = end < offsets.length - 1 ? '…' : '';
  const result = leading + text.slice(offsets[start], offsets[end]) + trailing;
  return { text: result, ranges: highlightRanges(result, terms) };
}
