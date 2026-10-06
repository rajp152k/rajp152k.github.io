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
    const link = (!pointerDismissed && postLink(pointerLink)) || postLink(focusedLink);
    const slug = link ? link.dataset.post : null;
    if (slug !== activeSlug) {
      if (activeSlug !== null) {
        for (const previous of linksByPost.get(activeSlug)) previous.classList.remove('is-active');
      }
      if (slug !== null) {
        for (const current of linksByPost.get(slug)) current.classList.add('is-active');
      }
      activeSlug = slug;
    }
    if (identifier) identifier.textContent = link ? link.dataset.postId : '—';
    if (title) title.textContent = link ? link.dataset.title : '';
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

  function refresh() {
    focusedLink = postLink(document.activeElement);
    pointerLink = pointerPosition
      ? postLink(document.elementFromPoint(pointerPosition.x, pointerPosition.y)) : null;
    render();
  }

  root.addEventListener('pointerover', (event) => {
    if (event.pointerType === 'touch') return;
    rememberPointer(event);
    setPointerLink(postLink(event.target));
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
    setPointerLink(postLink(event.target));
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
    if (event.key !== 'Escape' || event.target.closest('.search-form')) return;
    pointerDismissed = true;
    render();
  });

  refresh();
  return {
    setSelectable(slugs) {
      selectable = slugs;
      refresh();
    },
    refresh,
    clear() {
      pointerLink = null;
      focusedLink = null;
      pointerDismissed = true;
      render();
    },
  };
}
