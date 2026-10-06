import mermaid from 'mermaid';

const diagrams = document.querySelectorAll('.article-content pre > code.language-mermaid');
async function renderDiagrams() {
  const style = getComputedStyle(document.documentElement);
  const background = style.getPropertyValue('--background').trim();
  const text = style.getPropertyValue('--text').trim();
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'strict',
    htmlLabels: false,
    suppressErrorRendering: true,
    secure: ['securityLevel', 'startOnLoad', 'maxTextSize', 'maxEdges', 'htmlLabels', 'suppressErrorRendering'],
    theme: 'base',
    themeVariables: {
      darkMode: true,
      background,
      primaryColor: background,
      primaryTextColor: text,
      primaryBorderColor: text,
      secondaryColor: background,
      tertiaryColor: background,
      lineColor: text,
      textColor: text,
      fontFamily: style.getPropertyValue('--mono').trim(),
    },
  });

  await document.fonts.ready;
  let index = 0;
  for (const code of diagrams) {
    const source = code.parentElement;
    try {
      const { svg, bindFunctions } = await mermaid.render(`article-diagram-${index++}`, code.textContent);
      const figure = document.createElement('figure');
      figure.className = 'mermaid-diagram';
      figure.innerHTML = svg;
      source.replaceWith(figure);
      bindFunctions?.(figure);
    } catch (error) {
      const message = document.createElement('p');
      message.className = 'diagram-error';
      message.setAttribute('role', 'alert');
      message.textContent = 'The diagram could not be drawn. Its source is shown below.';
      source.before(message);
      console.error('Cannot render Mermaid diagram:', error);
    }
  }
}

if (diagrams.length) renderDiagrams();
