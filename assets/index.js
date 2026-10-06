import { createLinkedView } from './map.js';

const root = document.querySelector('body.index-page');
if (root) {
  const linked = createLinkedView(root);
  linked.setSelectable(new Set([...root.querySelectorAll('a.map-point[href]')].map(point => point.dataset.post)));
}
