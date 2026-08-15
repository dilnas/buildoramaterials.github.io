"""
Buildora Materials — Extra Product Gallery Photos (Pexels API, Phase B)

Downloads 2 additional, distinct photos per product for the product
detail page gallery, overwriting the Phase A placeholder copies made by
generate-product-pages.py at assets/images/products/extra/<slug>-2.jpg
and <slug>-3.jpg. Filenames are unchanged, so no HTML regeneration is
needed after running this.

Reuses each product's existing Pexels search query (from
download-product-images.py) but pulls a different result index per file
(photos[1] and photos[2] instead of photos[0]) so the two extra photos
look distinct from the main image and from each other.

Usage:
  export PEXELS_API_KEY="your-key-here"
  python3 download-extra-product-images.py

Get a FREE key at: https://www.pexels.com/api/  (no credit card needed)
"""

import os, sys, time, warnings
warnings.filterwarnings("ignore")
import requests
from pathlib import Path

from products_data import PRODUCTS

API_KEY = os.environ.get("PEXELS_API_KEY", "")
if not API_KEY:
    print("ERROR: PEXELS_API_KEY not set.")
    print("Get a FREE key at: https://www.pexels.com/api/")
    print('Then run:  export PEXELS_API_KEY="your-key"')
    sys.exit(1)

OUT_DIR = Path("assets/images/products/extra")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Same (filename -> search query) queries used by download-product-images.py
# for each product's main photo, keyed here by main image filename.
IMAGE_QUERIES = {
    "prod-dist-board.jpg":       "electrical distribution board panel",
    "prod-circuit-breaker.jpg":  "circuit breaker electrical panel",
    "prod-isolator.jpg":         "electrical isolator switch industrial",
    "prod-control-panel.jpg":    "electrical control panel components",
    "prod-capacitor.jpg":        "power capacitor bank industrial electrical",
    "prod-enclosure.jpg":        "electrical metal enclosure cabinet panel",
    "prod-panel-acc.jpg":        "electrical panel accessories din rail",
    "prod-cable-gland.jpg":      "cable gland connector electrical",
    "prod-cable-tray.jpg":       "cable tray ladder perforated steel",
    "prod-steel-support.jpg":    "steel cable support bracket system",
    "prod-conduit-pvc.jpg":      "PVC conduit pipe trunking electrical",
    "prod-cable-ties.jpg":       "nylon cable ties bundle",
    "prod-floor-dist.jpg":       "floor box electrical socket distribution",
    "prod-cable-joint.jpg":      "cable jointing splice connector",
    "prod-steel-conduit.jpg":    "steel conduit pipe wiring box",
    "prod-solar-cable.jpg":      "solar cable DC photovoltaic",
    "prod-coaxial.jpg":          "coaxial cable RF antenna",
    "prod-single-wire.jpg":      "single core copper electrical wire coloured",
    "prod-xlpe-cable.jpg":       "XLPE armoured electrical cable cross section",
    "prod-fire-cable.jpg":       "fire resistant cable red",
    "prod-multicore.jpg":        "multicore industrial cable",
    "prod-welding-cable.jpg":    "welding cable rubber flexible",
    "prod-battery-cable.jpg":    "battery cable heavy copper lug",
    "prod-fiber-optic.jpg":      "fiber optic cable data communication",
    "prod-ppr-pipe.jpg":         "PPR green pipe fitting plumbing",
    "prod-upvc-pipe.jpg":        "UPVC white pipe fitting plumbing",
    "prod-hdpe-pipe.jpg":        "HDPE black pipe fitting polyethylene",
    "prod-pex-pipe.jpg":         "PEX flexible pipe red blue plumbing",
    "prod-pvc-pipe.jpg":         "PVC water pipe fitting white",
    "prod-hp-pipe.jpg":          "high pressure steel pipe industrial",
    "prod-drainage.jpg":         "drainage pipe channel system",
    "prod-switch-wp.jpg":        "waterproof electrical switch socket IP65",
    "prod-popup-switch.jpg":     "pop up floor electrical socket chrome",
    "prod-socket.jpg":           "wall electrical switch socket plate white",
    "prod-smart-switch.jpg":     "smart WiFi touch switch panel",
    "prod-grid-switch.jpg":      "modular grid switch socket module",
    "prod-metal-switch.jpg":     "metal clad industrial switch socket",
    "prod-sw-isolator.jpg":      "rotary isolator switch electrical",
    "prod-antifungal-paint.jpg": "anti fungal paint tin can wall",
    "prod-exterior-paint.jpg":   "exterior wall emulsion paint bucket",
    "prod-interior-paint.jpg":   "interior emulsion paint tin roller",
    "prod-fenomastic.jpg":       "premium paint tin can wall",
    "prod-emulsion.jpg":         "emulsion paint bucket roller tray",
    "prod-texture-paint.jpg":    "texture paint bucket wall",
    "prod-enamel-paint.jpg":     "enamel paint tin can metal",
    "prod-primer.jpg":           "primer undercoat paint can",
    "prod-wall-putty.jpg":       "wall putty powder bag",
    "prod-impact-wrench.jpg":    "cordless impact wrench power tool",
    "prod-angle-grinder.jpg":    "angle grinder power tool",
    "prod-power-tools.jpg":      "power tools set drill grinder",
    "prod-hand-tools.jpg":       "hand tools set hammer screwdriver pliers",
    "prod-tool-acc.jpg":         "power tool accessories drill bits",
    "prod-drill.jpg":            "hammer drill SDS power tool",
    "prod-router.jpg":           "wood router power tool",
    "prod-miter-saw.jpg":        "miter chop saw power tool",
    "prod-jigsaw.jpg":           "jigsaw power tool blade",
    "prod-hilti.jpg":            "Hilti professional drilling tool red",
    "prod-lightning.jpg":        "lightning protection air terminal rod",
    "prod-earthing.jpg":         "earthing rod grounding copper",
    "prod-copper-tape.jpg":      "copper tape earthing roll",
    "prod-air-terminal.jpg":     "lightning air terminal spike",
    "prod-prot-acc.jpg":         "earthing protection accessories clamps",
    "prod-sanitary.jpg":         "sanitary ware toilet basin bathroom",
    "prod-water-heater.jpg":     "electric water heater tank",
    "prod-sensor-tap.jpg":       "touchless sensor tap faucet chrome",
    "prod-shower.jpg":           "shower mixer tap set overhead chrome",
    "prod-tiles.jpg":            "ceramic floor wall tiles",
    "prod-valve.jpg":            "plumbing valve ball gate fitting",
    "prod-safety-shoes.jpg":     "steel toe safety boots shoes",
    "prod-harness.jpg":          "full body safety harness fall protection",
    "prod-helmet.jpg":           "construction safety hard hat helmet",
    "prod-ear-plug.jpg":         "ear plugs protectors safety",
    "prod-gloves.jpg":           "safety work gloves",
    "prod-hi-vis.jpg":           "high visibility vest coverall orange",
    "prod-copper-coil.jpg":      "copper tube coil refrigeration HVAC",
    "prod-insulation.jpg":       "pipe insulation foam tube black",
    "prod-sheet-ins.jpg":        "thermal sheet insulation foam panel",
    "prod-refrigerant.jpg":      "refrigerant gas cylinder air conditioning",
    "prod-hvac-control.jpg":     "HVAC thermostat control panel",
    "prod-hvac-acc.jpg":         "HVAC duct fitting diffuser grille",
    "prod-track-light.jpg":      "ceiling track light spotlight adjustable",
    "prod-panel-light.jpg":      "LED ceiling panel light flat",
    "prod-downlight.jpg":        "recessed LED downlight ceiling",
    "prod-spotlight.jpg":        "LED spotlight ceiling mounted",
    "prod-led-strip.jpg":        "LED strip light aluminium profile",
    "prod-linear-light.jpg":     "linear LED batten light fixture",
    "prod-centrifugal-pump.jpg": "centrifugal water pump industrial",
    "prod-pressure-pump.jpg":    "pressure booster pump set tank",
    "prod-transfer-pump.jpg":    "water transfer pump portable",
    "prod-booster-pump.jpg":     "water booster pump pressure vessel",
    "prod-pump-panel.jpg":       "pump motor control panel electrical",
    "prod-submersible.jpg":      "submersible water pump stainless steel",
    "prod-nails.jpg":            "steel nails construction assortment",
    "prod-screws.jpg":           "wood metal screws assortment box",
    "prod-nuts-bolts.jpg":       "hex nuts bolts hardware stainless steel",
    "prod-anchor-bolt.jpg":      "concrete anchor bolt expansion",
    "prod-wire-rope.jpg":        "wire rope clips shackles rigging",
    "prod-ladder.jpg":           "aluminium ladder extension",
    "prod-wheelbarrow.jpg":      "construction wheelbarrow trolley",
    "prod-steel-tube.jpg":       "steel hollow tube section profile",
    "prod-tarpaulin.jpg":        "blue tarpaulin polythene sheet",
    "prod-thermocol.jpg":        "thermocol foam sheet polystyrene",
    "prod-masking-tape.jpg":     "masking tape roll yellow",
    "prod-duct-tape.jpg":        "duct tape roll silver grey",
    "prod-ins-tape.jpg":         "electrical insulation tape coloured",
    "prod-spanner.jpg":          "spanner wrench hand tools set",
    "prod-spirit-level.jpg":     "spirit level tool builder",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
}


def search_pexels(query, api_key, per_page=5):
    url = "https://api.pexels.com/v1/search"
    r = requests.get(url, params={"query": query, "per_page": per_page, "orientation": "landscape"},
                      headers={**HEADERS, "Authorization": api_key}, timeout=15)
    r.raise_for_status()
    photos = r.json().get("photos", [])
    return [p["src"]["medium"] for p in photos]


def download(url, out_path):
    r = requests.get(url, headers={**HEADERS, "Referer": "https://www.pexels.com/"}, timeout=20)
    r.raise_for_status()
    out_path.write_bytes(r.content)
    return out_path.stat().st_size


total = len(PRODUCTS) * 2
done = 0
failed = []

print(f"Downloading {total} extra gallery photos from Pexels ({len(PRODUCTS)} products x 2)...\n")

for i, product in enumerate(PRODUCTS, 1):
    slug = product["slug"]
    query = IMAGE_QUERIES.get(product["image"])
    if not query:
        print(f"[{i}/{len(PRODUCTS)}] SKIP (no query mapped): {slug}")
        failed.append(slug)
        continue

    print(f"[{i}/{len(PRODUCTS)}] Searching: {query}  ({slug})")
    try:
        urls = search_pexels(query, API_KEY)
        if len(urls) < 2:
            print(f"         WARNING: only {len(urls)} results, reusing what's available")
        for n, suffix in enumerate(("2", "3"), start=1):
            out_path = OUT_DIR / f"{slug}-{suffix}.jpg"
            pick = urls[n] if n < len(urls) else (urls[-1] if urls else None)
            if not pick:
                print(f"         FAILED: no photo available for {out_path.name}")
                failed.append(out_path.name)
                continue
            size = download(pick, out_path)
            print(f"         Saved {size // 1024}KB -> {out_path.name}")
            done += 1
    except Exception as e:
        print(f"         ERROR: {e}")
        failed.append(slug)

    time.sleep(0.4)  # Pexels free tier: 200 requests/hour

print(f"\n{'=' * 50}")
print(f"Done: {done}/{total} downloaded, {len(failed)} failed")
if failed:
    print(f"Failed: {', '.join(failed)}")
