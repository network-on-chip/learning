#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote

def check_site(site_dir: Path):
    if not site_dir.exists():
        print(f"Site dir {site_dir} does not exist.")
        return 1

    all_html = list(site_dir.glob("**/*.html"))
    broken = []
    checked = 0

    for html in all_html:
        rel_html = html.relative_to(site_dir)
        content = html.read_text(encoding="utf-8")
        
        # Match href and src attributes
        matches = re.findall(r'(?:href|src)=["\']([^"\'\s>]+)["\']', content)
        for ref in matches:
            if ref.startswith(("http://", "https://", "mailto:", "javascript:", "data:", "#")):
                continue
            checked += 1
            
            # Parse URL to remove fragment and query
            parsed = urlparse(ref)
            path_part = unquote(parsed.path)
            if not path_part:
                continue

            # Handle base path /learning/
            if path_part.startswith("/learning/"):
                clean_path = path_part[len("/learning/"):]
                target = site_dir / clean_path
            elif path_part.startswith("/"):
                target = site_dir / path_part.lstrip("/")
            else:
                target = (html.parent / path_part).resolve()

            # Check existence
            if not target.exists():
                # If target without trailing slash was meant to be a directory
                if not (target / "index.html").exists():
                    broken.append((str(rel_html), ref, str(target)))

    print(f"Checked {checked} internal links/assets across {len(all_html)} HTML pages.")
    print(f"Broken links/assets found: {len(broken)}")
    if broken:
        for page, ref, tgt in broken[:50]:
            print(f"  [BROKEN] {page} -> {ref}")
        return 1
    else:
        print("ALL INTERNAL LINKS & ASSETS ARE VALID!")
        return 0

if __name__ == "__main__":
    site = Path(__file__).resolve().parent.parent / "site"
    sys.exit(check_site(site))
