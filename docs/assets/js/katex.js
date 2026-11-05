/**
 * KaTeX Auto-Render Initializer for Material for MkDocs
 * Robust loader supporting standard DOM lifecycle and Material instant loading.
 */
(function () {
  function renderAllKaTeX(root) {
    const target = root || document.body;
    if (typeof renderMathInElement === "function" && target) {
      renderMathInElement(target, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "$", right: "$", display: false },
          { left: "\\(", right: "\\)", display: false },
          { left: "\\[", right: "\\]", display: true }
        ],
        ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
        throwOnError: false
      });
    }
  }

  // Support Material for MkDocs instant navigation when enabled
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe((args) => {
      const el = (args && args.body) ? args.body : document.body;
      renderAllKaTeX(el);
    });
  }

  // Execute on initial DOM ready or immediately if already loaded
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => renderAllKaTeX(document.body));
  } else {
    renderAllKaTeX(document.body);
  }

  // Secondary assurance on full window load
  window.addEventListener("load", () => renderAllKaTeX(document.body));
})();
