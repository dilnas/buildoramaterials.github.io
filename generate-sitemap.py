"""
Buildora Materials — sitemap.xml generator

Lists the site pages, every blog post in blog/, and every product page that is
indexed (see site_seo.in_sitemap). Product pages marked noindex stay live on
the site; they are just not submitted to search engines.

Usage:
  python3 generate-sitemap.py            # lastmod = today
  python3 generate-sitemap.py 2026-10-27 # lastmod = given date
"""
import sys
from datetime import date
from pathlib import Path

from products_data import PRODUCTS
from site_seo import SITE_URL, in_sitemap

ROOT = Path(__file__).parent
LASTMOD = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()

PAGES = [
    ("/", "weekly", "1.0"),
    ("/products.html", "weekly", "0.9"),
    ("/about.html", "monthly", "0.8"),
    ("/contact.html", "monthly", "0.8"),
    ("/brands.html", "monthly", "0.7"),
    ("/why-us.html", "monthly", "0.7"),
    ("/blog.html", "weekly", "0.7"),
    ("/privacy.html", "yearly", "0.3"),
]


def url(loc, changefreq, priority):
    return (f"  <url>\n    <loc>{SITE_URL}{loc}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n"
            f"    <changefreq>{changefreq}</changefreq>\n    <priority>{priority}</priority>\n  </url>\n")


def main():
    entries = [url(*p) for p in PAGES]
    for post in sorted((ROOT / "blog").glob("*.html")):
        entries.append(url(f"/blog/{post.name}", "monthly", "0.7"))
    products = [p for p in PRODUCTS if in_sitemap(p)]
    for p in products:
        entries.append(url(f"/products/{p['slug']}.html", "monthly", "0.6"))

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "".join(entries) + "</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"sitemap.xml: {len(entries)} URLs ({len(products)} products, "
          f"{len(PRODUCTS) - len(products)} product pages live but not submitted)")


if __name__ == "__main__":
    main()
