"""
Buildora Materials — Extra Product Gallery Photos (Pexels API, Phase B)

Downloads 2 additional, distinct photos per product for the product
detail page gallery, overwriting the Phase A placeholder copies made by
generate-product-pages.py at assets/images/products/extra/<slug>-2.webp
and <slug>-3.webp. Filenames are unchanged, so no HTML regeneration is
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
from io import BytesIO
from PIL import Image

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
    "prod-dist-board.webp":       "electrical distribution board panel",
    "prod-circuit-breaker.webp":  "circuit breaker electrical panel",
    "prod-isolator.webp":         "electrical isolator switch industrial",
    "prod-control-panel.webp":    "electrical control panel components",
    "prod-capacitor.webp":        "power capacitor bank industrial electrical",
    "prod-enclosure.webp":        "electrical metal enclosure cabinet panel",
    "prod-panel-acc.webp":        "electrical panel accessories din rail",
    "prod-cable-gland.webp":      "cable gland connector electrical",
    "prod-cable-tray.webp":       "cable tray ladder perforated steel",
    "prod-steel-support.webp":    "steel cable support bracket system",
    "prod-conduit-pvc.webp":      "PVC conduit pipe trunking electrical",
    "prod-cable-ties.webp":       "nylon cable ties bundle",
    "prod-floor-dist.webp":       "floor box electrical socket distribution",
    "prod-cable-joint.webp":      "cable jointing splice connector",
    "prod-steel-conduit.webp":    "steel conduit pipe wiring box",
    "prod-solar-cable.webp":      "solar cable DC photovoltaic",
    "prod-coaxial.webp":          "coaxial cable RF antenna",
    "prod-single-wire.webp":      "single core copper electrical wire coloured",
    "prod-xlpe-cable.webp":       "XLPE armoured electrical cable cross section",
    "prod-fire-cable.webp":       "fire resistant cable red",
    "prod-multicore.webp":        "multicore industrial cable",
    "prod-welding-cable.webp":    "welding cable rubber flexible",
    "prod-battery-cable.webp":    "battery cable heavy copper lug",
    "prod-fiber-optic.webp":      "fiber optic cable data communication",
    "prod-ppr-pipe.webp":         "PPR green pipe fitting plumbing",
    "prod-upvc-pipe.webp":        "UPVC white pipe fitting plumbing",
    "prod-hdpe-pipe.webp":        "HDPE black pipe fitting polyethylene",
    "prod-pex-pipe.webp":         "PEX flexible pipe red blue plumbing",
    "prod-pvc-pipe.webp":         "PVC water pipe fitting white",
    "prod-hp-pipe.webp":          "high pressure steel pipe industrial",
    "prod-drainage.webp":         "drainage pipe channel system",
    "prod-switch-wp.webp":        "waterproof electrical switch socket IP65",
    "prod-popup-switch.webp":     "pop up floor electrical socket chrome",
    "prod-socket.webp":           "wall electrical switch socket plate white",
    "prod-smart-switch.webp":     "smart WiFi touch switch panel",
    "prod-grid-switch.webp":      "modular grid switch socket module",
    "prod-metal-switch.webp":     "metal clad industrial switch socket",
    "prod-sw-isolator.webp":      "rotary isolator switch electrical",
    "prod-antifungal-paint.webp": "anti fungal paint tin can wall",
    "prod-exterior-paint.webp":   "exterior wall emulsion paint bucket",
    "prod-interior-paint.webp":   "interior emulsion paint tin roller",
    "prod-fenomastic.webp":       "premium paint tin can wall",
    "prod-emulsion.webp":         "emulsion paint bucket roller tray",
    "prod-texture-paint.webp":    "texture paint bucket wall",
    "prod-enamel-paint.webp":     "enamel paint tin can metal",
    "prod-primer.webp":           "primer undercoat paint can",
    "prod-wall-putty.webp":       "wall putty powder bag",
    "prod-impact-wrench.webp":    "cordless impact wrench power tool",
    "prod-angle-grinder.webp":    "angle grinder power tool",
    "prod-power-tools.webp":      "power tools set drill grinder",
    "prod-hand-tools.webp":       "hand tools set hammer screwdriver pliers",
    "prod-tool-acc.webp":         "power tool accessories drill bits",
    "prod-drill.webp":            "hammer drill SDS power tool",
    "prod-router.webp":           "wood router power tool",
    "prod-miter-saw.webp":        "miter chop saw power tool",
    "prod-jigsaw.webp":           "jigsaw power tool blade",
    "prod-hilti.webp":            "Hilti professional drilling tool red",
    "prod-lightning.webp":        "lightning protection air terminal rod",
    "prod-earthing.webp":         "earthing rod grounding copper",
    "prod-copper-tape.webp":      "copper tape earthing roll",
    "prod-air-terminal.webp":     "lightning air terminal spike",
    "prod-prot-acc.webp":         "earthing protection accessories clamps",
    "prod-sanitary.webp":         "sanitary ware toilet basin bathroom",
    "prod-water-heater.webp":     "electric water heater tank",
    "prod-sensor-tap.webp":       "touchless sensor tap faucet chrome",
    "prod-shower.webp":           "shower mixer tap set overhead chrome",
    "prod-tiles.webp":            "ceramic floor wall tiles",
    "prod-valve.webp":            "plumbing valve ball gate fitting",
    "prod-safety-shoes.webp":     "steel toe safety boots shoes",
    "prod-harness.webp":          "full body safety harness fall protection",
    "prod-helmet.webp":           "construction safety hard hat helmet",
    "prod-ear-plug.webp":         "ear plugs protectors safety",
    "prod-gloves.webp":           "safety work gloves",
    "prod-hi-vis.webp":           "high visibility vest coverall orange",
    "prod-copper-coil.webp":      "copper tube coil refrigeration HVAC",
    "prod-insulation.webp":       "pipe insulation foam tube black",
    "prod-sheet-ins.webp":        "thermal sheet insulation foam panel",
    "prod-refrigerant.webp":      "refrigerant gas cylinder air conditioning",
    "prod-hvac-control.webp":     "HVAC thermostat control panel",
    "prod-hvac-acc.webp":         "HVAC duct fitting diffuser grille",
    "prod-track-light.webp":      "ceiling track light spotlight adjustable",
    "prod-panel-light.webp":      "LED ceiling panel light flat",
    "prod-downlight.webp":        "recessed LED downlight ceiling",
    "prod-spotlight.webp":        "LED spotlight ceiling mounted",
    "prod-led-strip.webp":        "LED strip light aluminium profile",
    "prod-linear-light.webp":     "linear LED batten light fixture",
    "prod-centrifugal-pump.webp": "centrifugal water pump industrial",
    "prod-pressure-pump.webp":    "pressure booster pump set tank",
    "prod-transfer-pump.webp":    "water transfer pump portable",
    "prod-booster-pump.webp":     "water booster pump pressure vessel",
    "prod-pump-panel.webp":       "pump motor control panel electrical",
    "prod-submersible.webp":      "submersible water pump stainless steel",
    "prod-nails.webp":            "steel nails construction assortment",
    "prod-screws.webp":           "wood metal screws assortment box",
    "prod-nuts-bolts.webp":       "hex nuts bolts hardware stainless steel",
    "prod-anchor-bolt.webp":      "concrete anchor bolt expansion",
    "prod-wire-rope.webp":        "wire rope clips shackles rigging",
    "prod-ladder.webp":           "aluminium ladder extension",
    "prod-wheelbarrow.webp":      "construction wheelbarrow trolley",
    "prod-steel-tube.webp":       "steel hollow tube section profile",
    "prod-tarpaulin.webp":        "blue tarpaulin polythene sheet",
    "prod-thermocol.webp":        "thermocol foam sheet polystyrene",
    "prod-masking-tape.webp":     "masking tape roll yellow",
    "prod-duct-tape.webp":        "duct tape roll silver grey",
    "prod-ins-tape.webp":         "electrical insulation tape coloured",
    "prod-spanner.webp":          "spanner wrench hand tools set",
    "prod-spirit-level.webp":     "spirit level tool builder",
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
    img = Image.open(BytesIO(r.content)).convert("RGB")
    img.save(out_path, "WEBP", quality=82, method=6)
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
            out_path = OUT_DIR / f"{slug}-{suffix}.webp"
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
