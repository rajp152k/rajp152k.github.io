// Enhance references only on desktop. The source spans are plain text elsewhere.
export function setupTerms(root = document, viewport = window.matchMedia('(min-width: 901px)')) {
  const panel = root.querySelector('#terms-panel');
  const toggle = root.querySelector('[data-terms-toggle]');
  if (!panel || !toggle) return;
  const content = panel.querySelector('[data-terms-content]');
  const list = panel.querySelector('[data-terms-list]');
  const back = panel.querySelector('[data-terms-back]');
  const close = panel.querySelector('[data-terms-close]');
  const references = [...root.querySelectorAll('.term-reference[data-term]')];
  const templates = new Map([...root.querySelectorAll('template[data-term-card]')]
    .map(template => [template.dataset.termCard, template]));
  let selected = null;
  let returnFocus = null;

  function clearSelection() {
    selected = null;
    content.replaceChildren();
    list.hidden = false;
    back.hidden = true;
    references.forEach(reference => reference.setAttribute('aria-expanded', 'false'));
  }

  function setOpen(open, restoreFocus = false) {
    panel.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    if (viewport.matches) references.forEach(reference => {
      reference.setAttribute('aria-expanded', String(open && selected === reference.dataset.term));
    });
    root.querySelector('.reading-shell')?.classList.toggle('references-open', open);
    if (!open && restoreFocus) {
      const target = returnFocus?.isConnected && !returnFocus.closest('[hidden]') ? returnFocus : toggle;
      target.focus();
    }
  }

  function selectTerm(id, trigger) {
    if (!viewport.matches || !templates.has(id)) return;
    returnFocus = trigger;
    selected = id;
    content.replaceChildren(templates.get(id).content.cloneNode(true));
    list.hidden = true;
    back.hidden = false;
    references.forEach(reference => reference.setAttribute('aria-expanded', String(reference.dataset.term === id)));
    setOpen(true);
    // Move focus into the card so the definition follows the trigger for keyboard readers.
    content.querySelector('h3').focus({ preventScroll: true });
  }

  references.forEach(reference => {
    reference.addEventListener('click', () => selectTerm(reference.dataset.term, reference));
    reference.addEventListener('keydown', event => {
      if (viewport.matches && (event.key === 'Enter' || event.key === ' ')) {
        event.preventDefault();
        selectTerm(reference.dataset.term, reference);
      }
    });
  });
  panel.querySelectorAll('[data-select-term]').forEach(button => {
    button.addEventListener('click', () => selectTerm(button.dataset.selectTerm, button));
  });
  toggle.addEventListener('click', () => {
    returnFocus = toggle;
    setOpen(panel.hidden, true);
  });
  close.addEventListener('click', () => setOpen(false, true));
  back.addEventListener('click', () => {
    clearSelection();
    list.querySelector('button')?.focus({ preventScroll: true });
  });
  panel.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      event.preventDefault();
      setOpen(false, true);
    }
  });

  function syncViewport() {
    toggle.hidden = !viewport.matches;
    references.forEach(reference => {
      if (viewport.matches && templates.has(reference.dataset.term)) {
        reference.setAttribute('role', 'button');
        reference.setAttribute('tabindex', '0');
        reference.setAttribute('aria-controls', 'terms-panel');
        reference.setAttribute('aria-expanded', String(selected === reference.dataset.term));
        reference.setAttribute('aria-label', `${reference.textContent}: show reference`);
      } else {
        for (const name of ['role', 'tabindex', 'aria-controls', 'aria-expanded', 'aria-label']) {
          reference.removeAttribute(name);
        }
      }
    });
    if (!viewport.matches) {
      // A resize must not leave keyboard focus inside a hidden desktop panel.
      if (panel.contains(root.activeElement)) root.activeElement.blur();
      setOpen(false);
    } else {
      setOpen(window.matchMedia('(min-width: 1200px)').matches);
    }
  }
  viewport.addEventListener('change', syncViewport);
  syncViewport();
}

if (typeof document !== 'undefined') setupTerms();
