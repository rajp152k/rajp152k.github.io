(() => {
  const root = document.querySelector('body.index-page');
  if (!root) return;

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

  const title = root.querySelector('.map-readout-title');
  const date = root.querySelector('.map-readout-date');
  const defaultTitle = 'Hover or focus a post';
  const defaultDate = '';
  let pointerLink = null;
  let focusedLink = null;
  let pointerDismissed = false;
  let pointerPosition = null;
  let activeSlug = null;

  function postLink(node) {
    if (!(node instanceof Element)) return null;
    const link = node.closest(selector);
    return link && root.contains(link) && linksByPost.has(link.dataset.post)
      ? link
      : null;
  }

  function render() {
    const link = (!pointerDismissed && pointerLink) || focusedLink;
    const slug = link ? link.dataset.post : null;
    if (slug !== activeSlug) {
      if (activeSlug !== null) {
        for (const previous of linksByPost.get(activeSlug)) {
          previous.classList.remove('is-active');
        }
      }
      if (slug !== null) {
        for (const current of linksByPost.get(slug)) {
          current.classList.add('is-active');
        }
      }
      activeSlug = slug;
    }
    if (title) title.textContent = link ? (link.dataset.title ?? defaultTitle) : defaultTitle;
    if (date) date.textContent = link ? (link.dataset.date ?? defaultDate) : defaultDate;
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

  root.addEventListener('pointerover', (event) => {
    if (event.pointerType === 'touch') return;
    rememberPointer(event);
    setPointerLink(postLink(event.target));
  });

  root.addEventListener('pointerout', (event) => {
    if (event.pointerType === 'touch') return;
    if (event.relatedTarget instanceof Node && root.contains(event.relatedTarget)) {
      rememberPointer(event);
    } else {
      pointerPosition = null;
    }
    setPointerLink(postLink(event.relatedTarget));
  });

  root.addEventListener('pointermove', (event) => {
    if (event.pointerType !== 'touch') rememberPointer(event);
  }, { passive: true });

  // A scrolling row can leave the pointer without a physical pointer movement.
  root.addEventListener('scroll', () => {
    if (!pointerPosition) return;
    setPointerLink(postLink(document.elementFromPoint(pointerPosition.x, pointerPosition.y)));
  }, { capture: true, passive: true });

  root.addEventListener('focusin', (event) => {
    focusedLink = postLink(event.target);
    render();
  });

  root.addEventListener('focusout', (event) => {
    focusedLink = postLink(event.relatedTarget);
    render();
  });

  root.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    pointerDismissed = true;
    render();
  });

  focusedLink = postLink(document.activeElement);
  render();
})();
