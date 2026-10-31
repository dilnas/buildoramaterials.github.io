"""
Shared SEO rules for Buildora Materials — used by generate-product-pages.py
and generate-sitemap.py so both agree on host, address and which product
pages are indexed.

Nothing here deletes or renames a product. Every product in products_data.py
keeps its page, URL, catalogue card and WhatsApp quote button. These rules
only decide how brands are labelled and whether Google is asked to index a page.
"""
import re

from products_data import PRODUCTS

# One canonical host. GitHub Pages serves the bare domain (see CNAME), so every
# canonical, Open Graph URL, JSON-LD URL and sitemap entry uses it.
SITE_URL = "https://buildoramaterials.com"

# Business address (moved from Al Quoz, Dubai to Ajman in October 2026).
ADDRESS_SHORT = "Amber Gem Tower, Ajman, UAE"
ADDRESS_FULL = "CWS-1V-228162, 26th Floor, Amber Gem Tower, Ajman, UAE"
MAPS_URL = "https://maps.google.com/?q=Amber+Gem+Tower+Ajman+UAE"
GEO_REGION = "AE-AJ"

# Generic "type" pages (e.g. "MCB, C Curve", "Compact PLC") had a brand assigned
# by rotation rather than one we actually supply. They stay live and linked, but
# are marked noindex until each is replaced with a real SKU. Set to False to
# index them again — no other change needed.
NOINDEX_GENERIC = False

# The first 107 products are the hand-written core catalogue (also in
# zoho_products_import.csv); their brand lists were chosen deliberately.
CURATED_COUNT = 107

UNBRANDED = {"Buildora Materials", "General"}

# Manufacturers we can recognise when they are named in a product's own
# name or spec line (used to show honest brands on generic pages).
_EXTRA_MAKERS = {
    "Siemens", "Allen-Bradley", "Omron", "Finder", "Rittal",
    "Phoenix Contact", "Eaton", "Mitsubishi", "Pilz", "SICK",
    "Hirschmann", "Weidmüller", "Pepperl+Fuchs", "Socomec", "Lovato",
}
# Brand names that are also ordinary words in specs ("Star-Delta", "Master
# Trip", "Touch protection") — never inferred from text.
_AMBIGUOUS = {"Delta", "Master", "Touch", "National", "Prime", "Atlas",
              "Terrain", "General", "Selex", "Milano", "Paige"}
KNOWN_MAKERS = sorted(
    (({b for p in PRODUCTS for b in p["brands"]} - UNBRANDED) | _EXTRA_MAKERS) - _AMBIGUOUS,
    key=len, reverse=True,
)

_INDEX = {p["slug"]: i for i, p in enumerate(PRODUCTS)}


def _words(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _brand_named_in_product(product, brand):
    """True when the brand (or its first word, e.g. 'RR' for 'RR Cables')
    appears in the product's own name — i.e. it is a specific branded item."""
    first = re.findall(r"[a-z0-9]+", brand.lower())
    if not first:
        return False
    return first[0] in _words(product["name"] + " " + product["wa_name"])


def brand_status(product):
    """'curated' | 'named' | 'unbranded' | 'generic'"""
    if _INDEX[product["slug"]] < CURATED_COUNT:
        return "curated"
    brands = product["brands"]
    if any(_brand_named_in_product(product, b) for b in brands if b not in UNBRANDED):
        return "named"
    if all(b in UNBRANDED for b in brands):
        return "unbranded"
    return "generic"


def makers_mentioned(product):
    """Manufacturers actually named in the product's name or spec line."""
    text = product["name"] + " " + product["detail"]
    found = []
    for m in KNOWN_MAKERS:
        if re.search(rf"(?<![A-Za-z]){re.escape(m)}(?![A-Za-z])", text) and m not in found:
            found.append(m)
    return found


def display_brands(product):
    """Brands that are honest to show for this product (may be empty)."""
    status = brand_status(product)
    if status == "curated":
        return list(product["brands"])
    if status == "named":
        return [b for b in product["brands"] if b not in UNBRANDED]
    if status == "unbranded":
        return []
    return makers_mentioned(product)


def assigned_brands(product):
    """Brands attached to a generic page that are NOT genuinely tied to it."""
    if brand_status(product) != "generic":
        return []
    shown = set(display_brands(product))
    return [b for b in product["brands"] if b not in UNBRANDED and b not in shown]


def clean_description(product):
    text = product["description"]
    for b in assigned_brands(product):
        eb = re.escape(b)
        text = re.sub(rf",? supplied by {eb} for ", ", sourced from leading manufacturers for ", text)
        text = re.sub(rf" from {eb}([,.])", r"\1", text)
        text = re.sub(rf" from {eb} — ", " — ", text)
    return text


def clean_sizes(product):
    drop = {f"Brand: {b}" for b in assigned_brands(product)}
    return [s for s in product["sizes"] if s not in drop]


# Same product listed twice under different spellings. Both pages stay live;
# the duplicate's canonical points at the primary so Google sees one page.
CANONICAL_OVERRIDES = {
    "fibre-glass-plaster-mesh-1-x50mtr": "fiber-glass-plaster-mesh-1-x50mtr",
}


def canonical_slug(product):
    return CANONICAL_OVERRIDES.get(product["slug"], product["slug"])


def is_indexed(product):
    return not (NOINDEX_GENERIC and brand_status(product) == "generic")


def in_sitemap(product):
    return is_indexed(product) and canonical_slug(product) == product["slug"]
