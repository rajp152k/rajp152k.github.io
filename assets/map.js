export function createLinkedView(root) {
  const selector = 'a.post-link, a.map-point';
  const linksByPost = new Map();
  for (const link of root.querySelectorAll(selector)) {
    const slug = link.dataset.post;
    if (slug === undefined) continue;
    let links = linksByPost.get(slug);
    if (!links) {
      links = [];
      linksByPost.set(slug, links);
    }
    links.push(link);
  }

  const identifier = root.querySelector('.map-readout-id');
  const title = root.querySelector('.map-readout-title');
  const date = root.querySelector('.map-readout-date');
  const edges = [...root.querySelectorAll('.map-reference')];
  const points = [...root.querySelectorAll('a.map-point')];
  const map = root.querySelector('.embedding-map');
  map?.classList.add('is-interactive');
  for (const point of points) {
    point.setAttribute('role', 'button');
    point.setAttribute('aria-controls', 'map-details');
    point.setAttribute('aria-expanded', 'false');
  }
  const inspector = root.querySelector('.map-inspector');
  const status = root.querySelector('.map-inspection-status');
  const details = root.querySelector('.map-details');
  const templates = new Map([...root.querySelectorAll('template[data-map-note]')]
    .map(template => [template.dataset.mapNote, template]));
  let pinnedSlug = null;

  function showDetails(slug) {
    if (slug === pinnedSlug) return;
    pinnedSlug = slug;
    if (inspector) inspector.hidden = !slug;
    for (const point of points) {
      const selected = point.dataset.post === slug;
      point.classList.toggle('is-selected', selected);
      point.setAttribute('aria-expanded', String(selected));
    }
    if (status) status.textContent = slug
      ? `Inspecting ${linksByPost.get(slug)?.[0].dataset.title}` : 'Inspection cleared.';
    if (details) {
      details.replaceChildren();
      const template = templates.get(slug);
      if (template) details.append(template.content.cloneNode(true));
      details.hidden = !template;
    }
  }
  let selectable = null;
  let pointerLink = null;
  let focusedLink = null;
  let pointerDismissed = false;
  let pointerPosition = null;
  let activeSlug = null;

  function postLink(node) {
    if (!(node instanceof Element)) return null;
    const link = node.closest(selector);
    const slug = link?.dataset.post;
    return link && root.contains(link) && linksByPost.has(slug)
      && (selectable === null || selectable.has(slug)) ? link : null;
  }

  function render() {
    const pinned = pinnedSlug ? postLink(linksByPost.get(pinnedSlug)?.[0]) : null;
    // Preview a hovered or keyboard-focused post without changing the Inspect card.
    const focused = postLink(focusedLink);
    const link = (focused?.matches(':focus-visible') && focused)
      || (!pointerDismissed && postLink(pointerLink)) || pinned || focused;
    const slug = link ? link.dataset.post : null;
    if (slug !== activeSlug) {
      if (activeSlug !== null) {
        for (const previous of linksByPost.get(activeSlug)) previous.classList.remove('is-active');
      }
      if (slug !== null) {
        for (const current of linksByPost.get(slug)) current.classList.add('is-active');
      }
      activeSlug = slug;
      for (const edge of edges) {
        edge.classList.toggle('is-active', slug !== null
          && (edge.dataset.source === slug || edge.dataset.target === slug));
      }
    }
    if (identifier) identifier.textContent = link ? link.dataset.postId : '—';
    root.querySelector('.map-readout')?.classList.toggle('is-active', slug !== null);
    if (title) title.textContent = link ? link.dataset.title : 'Click a circle to inspect';
    if (date) date.textContent = link ? link.dataset.displayDate : '';
  }

  function setPointerLink(link) {
    if (link === pointerLink) return;
    pointerLink = link;
    pointerDismissed = false;
    render();
  }

  function rememberPointer(event) {
    pointerPosition = { x: event.clientX, y: event.clientY };
  }

  // Resolve overlapping hit areas by distance, not SVG paint order.
  function pointerPost(target, x, y) {
    if (!map?.contains(target)) return postLink(target);
    const matrix = map.getScreenCTM();
    if (!matrix) return null;
    const position = new DOMPoint(x, y).matrixTransform(matrix.inverse());
    let nearest = null;
    let distance = Infinity;
    for (const point of points) {
      const dot = point.querySelector('.map-dot');
      const squared = (position.x - dot.cx.baseVal.value) ** 2
        + (position.y - dot.cy.baseVal.value) ** 2;
      const radius = parseFloat(getComputedStyle(point.querySelector('.map-hit')).r);
      if (squared <= radius ** 2 && squared < distance) {
        nearest = point;
        distance = squared;
      }
    }
    return postLink(nearest);
  }

  function refresh() {
    focusedLink = postLink(document.activeElement);
    pointerLink = pointerPosition
      ? pointerPost(document.elementFromPoint(pointerPosition.x, pointerPosition.y), pointerPosition.x, pointerPosition.y) : null;
    render();
  }

  function inspectPoint(point, keyboard = false) {
    showDetails(point.dataset.post);
    render();
    if (keyboard) details?.querySelector('h3 a')?.focus();
  }

  function dismiss() {
    const previous = points.find(point => point.dataset.post === pinnedSlug);
    const returnFocus = inspector?.contains(document.activeElement);
    showDetails(null);
    pointerDismissed = true;
    if (returnFocus) previous?.focus({ preventScroll: true });
    render();
  }

  root.addEventListener('click', event => {
    const point = event.detail === 0 ? postLink(event.target)
      : pointerPost(event.target, event.clientX, event.clientY);
    if (!point?.matches('.map-point') || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    inspectPoint(point, event.detail === 0);
  });

  root.querySelector('[data-map-reset]')?.addEventListener('click', () => {
    dismiss();
  });
  root.addEventListener('pointerover', (event) => {
    if (event.pointerType === 'touch') return;
    rememberPointer(event);
    setPointerLink(pointerPost(event.target, event.clientX, event.clientY));
  });
  root.addEventListener('pointerout', (event) => {
    if (event.pointerType === 'touch') return;
    if (event.relatedTarget instanceof Node && root.contains(event.relatedTarget)) rememberPointer(event);
    else pointerPosition = null;
    setPointerLink(postLink(event.relatedTarget));
  });
  root.addEventListener('pointermove', (event) => {
    if (event.pointerType === 'touch') return;
    rememberPointer(event);
    setPointerLink(pointerPost(event.target, event.clientX, event.clientY));
  }, { passive: true });
  root.addEventListener('scroll', refresh, { capture: true, passive: true });
  root.addEventListener('focusin', (event) => {
    focusedLink = postLink(event.target);
    render();
  });
  root.addEventListener('focusout', (event) => {
    focusedLink = postLink(event.relatedTarget);
    render();
  });
  root.addEventListener('keydown', (event) => {
    const point = postLink(event.target);
    if (point?.matches('.map-point') && (event.key === ' ' || event.key === 'Enter')) {
      event.preventDefault();
      inspectPoint(point, true);
      return;
    }
    if (event.key !== 'Escape' || event.target.closest('.search-form')) return;
    dismiss();
  });

  refresh();
  return {
    setSelectable(slugs) {
      selectable = slugs;
      for (const edge of edges) {
        edge.classList.toggle('is-context', slugs !== null
          && !slugs.has(edge.dataset.source) && !slugs.has(edge.dataset.target));
      }
      if (pinnedSlug && slugs !== null && !slugs.has(pinnedSlug)) showDetails(null);
      refresh();
    },
    refresh,
    clear() {
      pointerLink = null;
      focusedLink = null;
      pointerDismissed = true;
      showDetails(null);
      render();
    },
  };
}
