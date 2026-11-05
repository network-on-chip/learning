/**
 * High-Readability Callout & Blockquote Enhancer
 * Converts GitHub-style markdown callouts (> [!TIP], > [!NOTE], etc.)
 * into submission-grade Material for MkDocs Admonition blocks.
 */
(function () {
  const TYPE_MAP = {
    NOTE: { cls: "note", title: "Note" },
    TIP: { cls: "tip", title: "Key Insight / Problem Statement" },
    IMPORTANT: { cls: "important", title: "Important" },
    WARNING: { cls: "warning", title: "Warning" },
    CAUTION: { cls: "danger", title: "Caution" }
  };

  function transformCallouts(root) {
    const container = root || document.body;
    const bqs = container.querySelectorAll(".md-typeset blockquote");
    bqs.forEach((bq) => {
      const firstP = bq.querySelector("p");
      if (!firstP) return;

      const inner = firstP.innerHTML;
      const match = inner.match(/^\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\](?:\s*<br\s*\/?>|\s+)?([\s\S]*)$/i);
      if (match) {
        const typeKey = match[1].toUpperCase();
        const conf = TYPE_MAP[typeKey] || { cls: "note", title: "Note" };

        // Clean first paragraph content
        firstP.innerHTML = match[2];

        // Create admonition element
        const adm = document.createElement("div");
        adm.className = "admonition " + conf.cls;

        const titleP = document.createElement("p");
        titleP.className = "admonition-title";
        titleP.textContent = conf.title;
        adm.appendChild(titleP);

        // Move all children of blockquote into the admonition
        while (bq.firstChild) {
          adm.appendChild(bq.firstChild);
        }

        bq.parentNode.replaceChild(adm, bq);
      }
    });
  }

  // Support instant navigation
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe((args) => {
      const el = args && args.body ? args.body : document.body;
      transformCallouts(el);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => transformCallouts(document.body));
  } else {
    transformCallouts(document.body);
  }

  window.addEventListener("load", () => transformCallouts(document.body));
})();
