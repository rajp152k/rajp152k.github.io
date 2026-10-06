import MiniSearch from 'minisearch';
import { indexOptions, queryTerms, runSearch, searchKind, highlightRanges, excerpt } from './search-core.js';
import { createLinkedView } from './map.js';

const root = document.querySelector('body.search-page');
if (root && !root.dataset.searchInitialized) {
  root.dataset.searchInitialized = 'true';
  initialize(root);
}

function initialize(root) {
  const form = root.querySelector('.search-form');
  const input = form.querySelector('input[name=q]');
  const kindInput = form.querySelector('input[name=kind]');
  const sourceLinks = [...root.querySelectorAll('.collection-nav a[data-kind]')];
  let kind = searchKind(new URL(location.href).searchParams.get('kind'));
  function syncSource() {
    root.dataset.kind = kind;
    kindInput.value = kind;
    for (const link of sourceLinks) {
      const url = new URL('/search/', location.href);
      const source = searchKind(link.dataset.kind);
      if (source !== 'all') url.searchParams.set('kind', source);
      if (input.value) url.searchParams.set('q', input.value);
      link.href = url.href;
      if (source === kind) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    }
  }
  function scopedURL(url) {
    if (kind === 'all') url.searchParams.delete('kind');
    else url.searchParams.set('kind', kind);
    return url;
  }
  const table = root.querySelector('tbody');
  const rows = new Map([...table.querySelectorAll('tr[data-post]')].map(row => [row.dataset.post, row]));
  const points = new Map([...root.querySelectorAll('a.map-point')].map(point => [point.dataset.post, point]));
  const originalOrder = [...rows.keys()];
  const linked = createLinkedView(root);
  const contextGroup = root.querySelector('.map-context');
  const matchGroup = root.querySelector('.map-matches');
  const count = root.querySelector('.search-count');
  const message = root.querySelector('.search-message');
  const scroll = root.querySelector('.archive-scroll');
  let payloadPromise;
  let loaded;
  let revision = 0;
  let renderedQuery = null;
  let resultTimer;
  let urlTimer;
  let scrollTimer;
  let composing = false;
  let restore = history.state?.search || null;
  let activatedSlug = restore?.activatedSlug || null;
  let selectable = new Set();

  function marked(node, text, ranges) {
    const fragment = document.createDocumentFragment();
    let offset = 0;
    for (const range of ranges) {
      fragment.append(document.createTextNode(text.slice(offset, range.start)));
      const mark = document.createElement('mark');
      mark.textContent = text.slice(range.start, range.end);
      fragment.append(mark);
      offset = range.end;
    }
    fragment.append(document.createTextNode(text.slice(offset)));
    node.replaceChildren(fragment);
  }

  function state() {
    return { query: input.value, kind, scrollTop: scroll.scrollTop, activatedSlug };
  }

  function saveURL() {
    clearTimeout(urlTimer);
    clearTimeout(scrollTimer);
    const url = scopedURL(new URL(location.href));
    const query = input.value.trim();
    if (query) url.searchParams.set('q', query);
    else url.searchParams.delete('q');
    history.replaceState({ ...history.state, search: state() }, '', url);
  }

  function notify(text, error = false) {
    message.replaceChildren(document.createTextNode(text));
    message.hidden = !text;
    if (error) {
      message.append(document.createTextNode(' '));
      const archive = document.createElement('a');
      archive.href = kind === 'all' ? '/' : `/${kind}/`;
      archive.textContent = 'Browse the archive';
      const reload = document.createElement('a');
      const reloadURL = scopedURL(new URL(location.href));
      if (input.value.trim()) reloadURL.searchParams.set("q", input.value.trim());
      else reloadURL.searchParams.delete("q");
      reload.href = reloadURL.href;
      reload.textContent = 'reload this page';
      message.append(archive, document.createTextNode(' or '), reload, document.createTextNode('.'));
    }
  }

  function load() {
    if (!payloadPromise) {
      payloadPromise = (async () => {
        const response = await fetch(root.dataset.searchIndex);
        if (!response.ok) throw new Error('Search index unavailable');
        const payload = await response.json();
        if (payload.schemaVersion !== 2 || payload.tokenizerVersion !== 'word-prefix-1' || payload.engineVersion !== '7.2.0') {
          throw new Error('Search index version mismatch');
        }
        const documents = payload.documents;
        if (!documents || Object.keys(documents).length !== rows.size || points.size !== rows.size) {
          throw new Error('Search archive mismatch');
        }
        for (const [slug, row] of rows) {
          const doc = documents[slug];
          const link = row.querySelector('a.post-link');
          const point = points.get(slug);
          if (!doc || !point || doc.key !== slug || doc.kind !== row.dataset.kind || doc.kind !== point.dataset.kind || !Array.isArray(doc.blocks)) throw new Error('Search document mismatch');
          for (const element of [link, point]) {
            if (doc.title !== element.dataset.title || doc.date !== element.dataset.date || String(doc.postId) !== element.dataset.postId || doc.url !== (element.dataset.url || element.getAttribute('href'))) {
              throw new Error('Search metadata mismatch');
            }
          }
        }
        const engine = MiniSearch.loadJS(payload.index, indexOptions);
        if (engine.documentCount !== rows.size || originalOrder.some(slug => !engine.has(slug))) {
          throw new Error('Search engine archive mismatch');
        }
        loaded = { documents, engine };
        return loaded;
      })();
    }
    return payloadPromise;
  }

  function render(slugs, terms, documents, status, applyRestore = true) {
    scroll.removeAttribute('aria-busy');
    const focused = document.activeElement?.closest('a.post-link, a.map-point');
    selectable = new Set(slugs);
    const fragment = document.createDocumentFragment();
    for (const slug of slugs) {
      const row = rows.get(slug);
      if (!row) throw new Error('Unknown search result');
      const link = row.querySelector('.post-link');
      marked(link.querySelector('.post-title'), link.dataset.title, highlightRanges(link.dataset.title, terms));
      const snippet = link.querySelector('.post-excerpt');
      if (terms.length) {
        const summary = excerpt(documents[slug], terms);
        marked(snippet, summary.text, summary.ranges);
        snippet.hidden = !summary.text;
        if (summary.text) link.setAttribute('aria-describedby', snippet.id);
        else link.removeAttribute('aria-describedby');
      } else {
        snippet.replaceChildren();
        snippet.hidden = true;
        link.removeAttribute('aria-describedby');
      }
      row.hidden = false;
      fragment.append(row);
    }
    table.replaceChildren(fragment);
    for (const [slug, point] of points) {
      const matches = selectable.has(slug);
      point.classList.toggle('is-context', !matches);
      if (matches) {
        point.setAttribute('href', point.dataset.url);
        point.setAttribute('tabindex', '0');
        point.removeAttribute('aria-hidden');
      } else {
        point.removeAttribute('href');
        point.setAttribute('tabindex', '-1');
        point.setAttribute('aria-hidden', 'true');
      }
      (matches ? matchGroup : contextGroup).append(point);
    }
    linked.setSelectable(selectable);
    if (focused && !selectable.has(focused.dataset.post)) input.focus();
    else if (focused && document.activeElement !== focused) focused.focus({ preventScroll: true });
    linked.refresh();
    count.textContent = status;
    if (restore && applyRestore) {
      scroll.scrollTop = restore.scrollTop || 0;
      activatedSlug = selectable.has(restore.activatedSlug) ? restore.activatedSlug : null;
      if (activatedSlug) rows.get(activatedSlug).querySelector('.post-link').focus({ preventScroll: true });
      restore = null;
      linked.refresh();
    }
  }

  async function flush() {
    clearTimeout(resultTimer);
    const raw = input.value;
    const scope = kind;
    const scopedOrder = originalOrder.filter(key => scope === 'all' || rows.get(key).dataset.kind === scope);
    syncSource();
    const current = ++revision;
    try {
      const terms = queryTerms(raw);
      if (!raw.trim()) {
        render(scopedOrder, [], null, `${scopedOrder.length} ${scopedOrder.length === 1 ? 'entry' : 'entries'}`);
        notify(scopedOrder.length ? '' : 'This collection is empty.');
      } else if (!terms.length) {
        render([], [], null, 'No searchable terms');
        notify('Enter a word or number to search; punctuation alone has no searchable terms.');
      } else {
        count.textContent = 'Searching…';
        notify('Loading search…');
        if (!loaded) render([], [], null, 'Searching…', false);
        scroll.setAttribute('aria-busy', 'true');
        const { engine, documents } = loaded || await load();
        if (current !== revision || input.value !== raw || kind !== scope) return;
        const results = runSearch(engine, raw, documents, scope);
        render(results.map(result => result.id), terms, documents, `${results.length} / ${scopedOrder.length} matches`);
        notify(!scopedOrder.length ? 'This collection is empty.' : results.length ? '' : 'No entries match all of these search terms.');
      }
      renderedQuery = raw;
    } catch (error) {
      if (current !== revision || input.value !== raw || kind !== scope) return;
      render([], [], null, 'Search unavailable');
      notify('Search could not be completed.', true);
      renderedQuery = raw;
    }
  }

  function edited() {
    revision++;
    restore = null;
    activatedSlug = null;
    clearTimeout(resultTimer);
    clearTimeout(urlTimer);
    syncSource();
    if (composing) return;
    resultTimer = setTimeout(flush, 150);
    urlTimer = setTimeout(saveURL, 400);
  }

  function reset() {
    input.value = '';
    edited();
    void flush();
    saveURL();
    input.focus();
  }

  input.addEventListener('input', edited);
  input.addEventListener('compositionstart', () => { composing = true; revision++; clearTimeout(resultTimer); clearTimeout(urlTimer); });
  input.addEventListener('compositionend', () => { composing = false; edited(); });
  input.addEventListener('keydown', event => {
    if (event.isComposing || composing) return;
    if (event.key === 'Escape') { event.preventDefault(); reset(); }
    if (event.key === 'Tab') void flush();
  });
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (composing) return;
    void flush();
    saveURL();
  });
  root.querySelector('.search-clear').addEventListener('click', reset);

  function navigate(event) {
    const link = event.target.closest('a.post-link, a.map-point');
    if (!link || (event.type === 'auxclick' && event.button !== 1)) return;
    const slug = link.dataset.post;
    if (input.value !== renderedQuery) {
      const raw = input.value;
      void flush();
      if (renderedQuery === raw) {
        if (!selectable.has(slug)) event.preventDefault();
        else { activatedSlug = slug; saveURL(); }
        return;
      }
      event.preventDefault();
    } else if (selectable.has(slug)) {
      activatedSlug = slug;
      saveURL();
    } else event.preventDefault();
  }
  root.addEventListener('click', navigate, true);
  root.addEventListener('auxclick', navigate, true);
  scroll.addEventListener('scroll', () => {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(() => history.replaceState({ ...history.state, search: state() }, ""), 400);
  }, { passive: true });
  window.addEventListener('popstate', () => {
    clearTimeout(urlTimer);
    clearTimeout(scrollTimer);
    restore = history.state?.search || null;
    input.value = restore?.query ?? new URL(location.href).searchParams.get('q') ?? '';
    kind = searchKind(new URL(location.href).searchParams.get('kind'));
    renderedQuery = null;
    void flush();
  });
  window.addEventListener("pagehide", () => { saveURL(); clearTimeout(resultTimer); revision++; });
  window.addEventListener("pageshow", event => {
    if (!event.persisted) return;
    restore = history.state?.search || null;
    input.value = restore?.query ?? input.value;
    kind = searchKind(new URL(location.href).searchParams.get('kind'));
    void flush();
  });
  function viewport() {
    root.classList.toggle('is-short-viewport', (window.visualViewport?.height ?? window.innerHeight) < 480);
  }
  window.visualViewport?.addEventListener('resize', viewport);
  window.addEventListener('resize', viewport);
  viewport();
  input.value = restore?.query ?? new URL(location.href).searchParams.get('q') ?? '';
  void flush();
}
