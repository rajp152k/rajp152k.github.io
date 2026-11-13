// Theme-owned select-only combobox. Focus stays on the trigger while browsing.
export function createPostPicker(root, onChoose) {
  const trigger = root.querySelector('#map-inspect');
  if (!trigger) return null;
  const picker = trigger.closest('.map-picker');
  const list = root.querySelector('#map-inspect-options');
  const label = root.querySelector('#map-inspect-value');
  const options = [...list.querySelectorAll('[role="option"]')];
  let value = null;
  let active = null;
  let typed = '';
  let typedAt = 0;
  const enabled = () => options.filter(option => option.getAttribute('aria-disabled') !== 'true');

  function highlight(option) {
    active?.classList.remove('is-highlighted');
    active = option || null;
    if (active) {
      active.classList.add('is-highlighted');
      trigger.setAttribute('aria-activedescendant', active.id);
      active.scrollIntoView({ block: 'nearest' });
    } else trigger.removeAttribute('aria-activedescendant');
  }

  function close() {
    list.hidden = true;
    trigger.setAttribute('aria-expanded', 'false');
    highlight(null);
    typed = '';
  }

  function open() {
    list.hidden = false;
    trigger.setAttribute('aria-expanded', 'true');
    const available = enabled();
    highlight(available.find(option => option.dataset.value === value) || available[0]);
  }

  function setValue(slug) {
    value = slug;
    const selected = options.find(option => option.dataset.value === slug);
    label.textContent = selected?.textContent || 'Choose a post';
    for (const option of options) option.setAttribute('aria-selected', String(option === selected));
    close();
  }

  function choose(option) {
    if (!option || option.getAttribute('aria-disabled') === 'true') return;
    onChoose(option.dataset.value);
    trigger.focus();
  }

  trigger.addEventListener('click', () => list.hidden ? open() : close());
  // Keep focus on the trigger until the option click completes.
  list.addEventListener('pointerdown', event => event.preventDefault());
  list.addEventListener('click', event => choose(event.target.closest('[role="option"]')));
  picker.addEventListener('focusout', event => {
    if (!picker.contains(event.relatedTarget)) close();
  });
  document.addEventListener('pointerdown', event => {
    if (!picker.contains(event.target)) close();
  });
  trigger.addEventListener('keydown', event => {
    const { key } = event;
    if (key === 'Tab') {
      close();
      return;
    }
    if (key === 'Escape' && !list.hidden) {
      event.preventDefault();
      event.stopPropagation();
      close();
    } else if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(key)) {
      event.preventDefault();
      const wasClosed = list.hidden;
      if (wasClosed) open();
      const available = enabled();
      let index = available.indexOf(active);
      if (key === 'Home') index = 0;
      else if (key === 'End') index = available.length - 1;
      else if (!wasClosed) index = Math.max(0, Math.min(available.length - 1, index + (key === 'ArrowDown' ? 1 : -1)));
      else if (key === 'ArrowUp' && !value) index = available.length - 1;
      highlight(available[index]);
    } else if (key === 'Enter' || key === ' ') {
      event.preventDefault();
      if (list.hidden) open();
      else choose(active);
    } else if (key.length === 1 && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault();
      if (list.hidden) open();
      const now = performance.now();
      typed = (now - typedAt > 700 ? '' : typed) + key.toLowerCase();
      typedAt = now;
      const match = enabled().find(option => option.textContent.toLowerCase().includes(typed));
      if (match) highlight(match);
    }
  });

  return {
    setValue,
    close,
    setSelectable(slugs) {
      for (const option of options) {
        option.setAttribute('aria-disabled', String(slugs !== null && !slugs.has(option.dataset.value)));
      }
      if (active && !list.hidden) highlight(enabled().find(option => option === active) || enabled()[0]);
    },
  };
}
