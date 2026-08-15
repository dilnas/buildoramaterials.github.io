"""
Buildora Materials — Wire Catalogue Cards to Product Detail Pages

Rewrites each of the 107 .item-card blocks in products.html so the whole
card links to its new products/<slug>.html detail page, while the
existing "Request Quote ->" element keeps firing WhatsApp directly via
its own onclick (event.preventDefault + stopPropagation), preserving the
one-click quote shortcut alongside the new detail-page navigation.

Run after generate-product-pages.py.

Usage:
  python3 wire-product-links.py
"""
import re
from pathlib import Path

from products_data import PRODUCTS

PRODUCTS_HTML = Path("products.html")
WA_TO_SLUG = {p["wa_name"]: p["slug"] for p in PRODUCTS}

CARD_RE = re.compile(
    r'<div class="item-card" onclick="openWA\(\'(.*?)\'\)">(.*?)'
    r'</div><span class="item-quote">Request Quote →</span>\s*</div>',
    re.S,
)


def repl(m):
    wa_name = m.group(1)
    inner = m.group(2)
    slug = WA_TO_SLUG.get(wa_name)
    if slug is None:
        raise SystemExit(f"No slug found for openWA name: {wa_name!r}")
    quote_onclick = f"event.preventDefault(); event.stopPropagation(); openWA('{wa_name}')"
    return (
        f'<a class="item-card" href="products/{slug}.html">{inner}</div>'
        f'<span class="item-quote" onclick="{quote_onclick}">Request Quote →</span>\n        </a>'
    )


def main():
    html = PRODUCTS_HTML.read_text(encoding="utf-8")
    matches = CARD_RE.findall(html)
    print(f"Found {len(matches)} item-card blocks")
    assert len(matches) == 107, f"Expected 107 item-card blocks, found {len(matches)}"

    new_html, count = CARD_RE.subn(repl, html)
    assert count == 107, f"Expected 107 replacements, made {count}"

    PRODUCTS_HTML.write_text(new_html, encoding="utf-8")
    print(f"Wired {count} product cards to their detail pages in {PRODUCTS_HTML}")


if __name__ == "__main__":
    main()
