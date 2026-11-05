// Dynamic theme adapter for Mermaid diagrams in Material for MkDocs
(function () {
  const shadowCss = `
    /* Node labels and typography */
    .nodeLabel, .nodeLabel p, .nodeLabel span,
    .label, .label span, .label div, .label text,
    .cluster text, .cluster span, text, tspan, .flowchartTitleText {
      color: var(--md-mermaid-label-fg-color, #0f172a) !important;
      fill: var(--md-mermaid-label-fg-color, #0f172a) !important;
      font-family: 'Inter', -apple-system, sans-serif !important;
      font-weight: 600 !important;
    }

    /* Node shapes */
    .node rect, .node circle, .node ellipse, .node polygon,
    .node path:not(.flowchart-link) {
      fill: var(--md-mermaid-node-bg-color, #ffffff) !important;
      stroke: var(--md-mermaid-node-fg-color, #2563eb) !important;
      stroke-width: 1.75px !important;
    }

    /* Connecting paths, lines & arrows */
    .edgePath .path, .flowchart-link, .relation, .transition {
      stroke: var(--md-mermaid-edge-color, #334155) !important;
      stroke-width: 1.75px !important;
    }
    marker path, .marker, .arrowheadPath,
    .arrowMarkerPath {
      fill: var(--md-mermaid-edge-color, #334155) !important;
      stroke: var(--md-mermaid-edge-color, #334155) !important;
    }

    /* Clusters / Subgraphs */
    .cluster rect {
      fill: var(--md-default-bg-color--lighter, rgba(127, 127, 127, 0.08)) !important;
      stroke: var(--md-default-fg-color--lighter, #94a3b8) !important;
    }

    /* Edge labels */
    .edgeLabel, .edgeLabel rect, .edgeLabel p {
      background-color: var(--md-default-bg-color, #ffffff) !important;
      fill: var(--md-default-bg-color, #ffffff) !important;
      color: var(--md-mermaid-label-fg-color, #0f172a) !important;
    }
  `;

  function injectStyle(shadow) {
    if (!shadow) return;
    let styleTag = shadow.querySelector('#noc-mermaid-shadow-style');
    if (!styleTag) {
      styleTag = document.createElement('style');
      styleTag.id = 'noc-mermaid-shadow-style';
      shadow.appendChild(styleTag);
    }
    if (styleTag.textContent !== shadowCss) {
      styleTag.textContent = shadowCss;
    }
  }

  // Intercept attachShadow if not already intercepted
  if (!window.__noc_attachShadow_intercepted) {
    window.__noc_attachShadow_intercepted = true;
    const origAttach = Element.prototype.attachShadow;
    Element.prototype.attachShadow = function (init) {
      const shadow = origAttach.call(this, { mode: 'open' });
      const observer = new MutationObserver(() => injectStyle(shadow));
      observer.observe(shadow, { childList: true, subtree: true });
      setTimeout(() => injectStyle(shadow), 0);
      return shadow;
    };
  }

  // Also scan for any existing mermaid hosts or shadow roots
  function scanAndApply() {
    document.querySelectorAll('.mermaid').forEach((el) => {
      if (el.shadowRoot) {
        injectStyle(el.shadowRoot);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scanAndApply);
  } else {
    scanAndApply();
  }
})();
