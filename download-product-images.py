"""
Buildora Materials — Product Image Downloader (Pexels API)
Downloads real product photos for each of the 107 products.

Usage:
  export PEXELS_API_KEY="your-key-here"
  python3 download-product-images.py

Get a FREE key at: https://www.pexels.com/api/  (no credit card needed)
"""

import os, sys, time, warnings
warnings.filterwarnings("ignore")
import requests
from pathlib import Path
from io import BytesIO
from PIL import Image

API_KEY = os.environ.get("PEXELS_API_KEY", "")
if not API_KEY:
    print("ERROR: PEXELS_API_KEY not set.")
    print("Get a FREE key at: https://www.pexels.com/api/")
    print("Then run:  export PEXELS_API_KEY=\"your-key\"")
    sys.exit(1)

OUT_DIR = Path("assets/images/products")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Each product: (filename, search query for Pexels)
PRODUCTS = [
    # ELECTRICAL
    ("prod-dist-board.webp",       "electrical distribution board panel"),
    ("prod-circuit-breaker.webp",  "circuit breaker electrical panel"),
    ("prod-isolator.webp",         "electrical isolator switch industrial"),
    ("prod-control-panel.webp",    "electrical control panel components"),
    ("prod-capacitor.webp",        "power capacitor bank industrial electrical"),
    ("prod-enclosure.webp",        "electrical metal enclosure cabinet panel"),
    ("prod-panel-acc.webp",        "electrical panel accessories din rail"),
    # CABLE MANAGEMENT
    ("prod-cable-gland.webp",      "cable gland connector electrical"),
    ("prod-cable-tray.webp",       "cable tray ladder perforated steel"),
    ("prod-steel-support.webp",    "steel cable support bracket system"),
    ("prod-conduit-pvc.webp",      "PVC conduit pipe trunking electrical"),
    ("prod-cable-ties.webp",       "nylon cable ties bundle"),
    ("prod-floor-dist.webp",       "floor box electrical socket distribution"),
    ("prod-cable-joint.webp",      "cable jointing splice connector"),
    ("prod-steel-conduit.webp",    "steel conduit pipe wiring box"),
    # CABLES
    ("prod-solar-cable.webp",      "solar cable DC photovoltaic"),
    ("prod-coaxial.webp",          "coaxial cable RF antenna"),
    ("prod-single-wire.webp",      "single core copper electrical wire coloured"),
    ("prod-xlpe-cable.webp",       "XLPE armoured electrical cable cross section"),
    ("prod-fire-cable.webp",       "fire resistant cable red"),
    ("prod-multicore.webp",        "multicore industrial cable"),
    ("prod-welding-cable.webp",    "welding cable rubber flexible"),
    ("prod-battery-cable.webp",    "battery cable heavy copper lug"),
    ("prod-fiber-optic.webp",      "fiber optic cable data communication"),
    # PLUMBING
    ("prod-ppr-pipe.webp",         "PPR green pipe fitting plumbing"),
    ("prod-upvc-pipe.webp",        "UPVC white pipe fitting plumbing"),
    ("prod-hdpe-pipe.webp",        "HDPE black pipe fitting polyethylene"),
    ("prod-pex-pipe.webp",         "PEX flexible pipe red blue plumbing"),
    ("prod-pvc-pipe.webp",         "PVC water pipe fitting white"),
    ("prod-hp-pipe.webp",          "high pressure steel pipe industrial"),
    ("prod-drainage.webp",         "drainage pipe channel system"),
    # SWITCHES & SOCKETS
    ("prod-switch-wp.webp",        "waterproof electrical switch socket IP65"),
    ("prod-popup-switch.webp",     "pop up floor electrical socket chrome"),
    ("prod-socket.webp",           "wall electrical switch socket plate white"),
    ("prod-smart-switch.webp",     "smart WiFi touch switch panel"),
    ("prod-grid-switch.webp",      "modular grid switch socket module"),
    ("prod-metal-switch.webp",     "metal clad industrial switch socket"),
    ("prod-sw-isolator.webp",      "rotary isolator switch electrical"),
    # PAINTING
    ("prod-antifungal-paint.webp", "anti fungal paint tin can wall"),
    ("prod-exterior-paint.webp",   "exterior wall emulsion paint bucket"),
    ("prod-interior-paint.webp",   "interior emulsion paint tin roller"),
    ("prod-fenomastic.webp",       "premium paint tin can wall"),
    ("prod-emulsion.webp",         "emulsion paint bucket roller tray"),
    ("prod-texture-paint.webp",    "texture paint bucket wall"),
    ("prod-enamel-paint.webp",     "enamel paint tin can metal"),
    ("prod-primer.webp",           "primer undercoat paint can"),
    ("prod-wall-putty.webp",       "wall putty powder bag"),
    # TOOLS
    ("prod-impact-wrench.webp",    "cordless impact wrench power tool"),
    ("prod-angle-grinder.webp",    "angle grinder power tool"),
    ("prod-power-tools.webp",      "power tools set drill grinder"),
    ("prod-hand-tools.webp",       "hand tools set hammer screwdriver pliers"),
    ("prod-tool-acc.webp",         "power tool accessories drill bits"),
    ("prod-drill.webp",            "hammer drill SDS power tool"),
    ("prod-router.webp",           "wood router power tool"),
    ("prod-miter-saw.webp",        "miter chop saw power tool"),
    ("prod-jigsaw.webp",           "jigsaw power tool blade"),
    ("prod-hilti.webp",            "Hilti professional drilling tool red"),
    # EARTHING & LIGHTNING
    ("prod-lightning.webp",        "lightning protection air terminal rod"),
    ("prod-earthing.webp",         "earthing rod grounding copper"),
    ("prod-copper-tape.webp",      "copper tape earthing roll"),
    ("prod-air-terminal.webp",     "lightning air terminal spike"),
    ("prod-prot-acc.webp",         "earthing protection accessories clamps"),
    # SANITARY
    ("prod-sanitary.webp",         "sanitary ware toilet basin bathroom"),
    ("prod-water-heater.webp",     "electric water heater tank"),
    ("prod-sensor-tap.webp",       "touchless sensor tap faucet chrome"),
    ("prod-shower.webp",           "shower mixer tap set overhead chrome"),
    ("prod-tiles.webp",            "ceramic floor wall tiles"),
    ("prod-valve.webp",            "plumbing valve ball gate fitting"),
    # SAFETY
    ("prod-safety-shoes.webp",     "steel toe safety boots shoes"),
    ("prod-harness.webp",          "full body safety harness fall protection"),
    ("prod-helmet.webp",           "construction safety hard hat helmet"),
    ("prod-ear-plug.webp",         "ear plugs protectors safety"),
    ("prod-gloves.webp",           "safety work gloves"),
    ("prod-hi-vis.webp",           "high visibility vest coverall orange"),
    # HVAC
    ("prod-copper-coil.webp",      "copper tube coil refrigeration HVAC"),
    ("prod-insulation.webp",       "pipe insulation foam tube black"),
    ("prod-sheet-ins.webp",        "thermal sheet insulation foam panel"),
    ("prod-refrigerant.webp",      "refrigerant gas cylinder air conditioning"),
    ("prod-hvac-control.webp",     "HVAC thermostat control panel"),
    ("prod-hvac-acc.webp",         "HVAC duct fitting diffuser grille"),
    # LIGHTING
    ("prod-track-light.webp",      "ceiling track light spotlight adjustable"),
    ("prod-panel-light.webp",      "LED ceiling panel light flat"),
    ("prod-downlight.webp",        "recessed LED downlight ceiling"),
    ("prod-spotlight.webp",        "LED spotlight ceiling mounted"),
    ("prod-led-strip.webp",        "LED strip light aluminium profile"),
    ("prod-linear-light.webp",     "linear LED batten light fixture"),
    # PUMPS
    ("prod-centrifugal-pump.webp", "centrifugal water pump industrial"),
    ("prod-pressure-pump.webp",    "pressure booster pump set tank"),
    ("prod-transfer-pump.webp",    "water transfer pump portable"),
    ("prod-booster-pump.webp",     "water booster pump pressure vessel"),
    ("prod-pump-panel.webp",       "pump motor control panel electrical"),
    ("prod-submersible.webp",      "submersible water pump stainless steel"),
    # HARDWARE
    ("prod-nails.webp",            "steel nails construction assortment"),
    ("prod-screws.webp",           "wood metal screws assortment box"),
    ("prod-nuts-bolts.webp",       "hex nuts bolts hardware stainless steel"),
    ("prod-anchor-bolt.webp",      "concrete anchor bolt expansion"),
    ("prod-wire-rope.webp",        "wire rope clips shackles rigging"),
    ("prod-ladder.webp",           "aluminium ladder extension"),
    ("prod-wheelbarrow.webp",      "construction wheelbarrow trolley"),
    ("prod-steel-tube.webp",       "steel hollow tube section profile"),
    ("prod-tarpaulin.webp",        "blue tarpaulin polythene sheet"),
    ("prod-thermocol.webp",        "thermocol foam sheet polystyrene"),
    ("prod-masking-tape.webp",     "masking tape roll yellow"),
    ("prod-duct-tape.webp",        "duct tape roll silver grey"),
    ("prod-ins-tape.webp",         "electrical insulation tape coloured"),
    ("prod-spanner.webp",          "spanner wrench hand tools set"),
    ("prod-spirit-level.webp",     "spirit level tool builder"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
}

def search_pexels(query, api_key):
    url = "https://api.pexels.com/v1/search"
    r = requests.get(url, params={"query": query, "per_page": 3, "orientation": "landscape"},
                     headers={**HEADERS, "Authorization": api_key}, timeout=15)
    r.raise_for_status()
    photos = r.json().get("photos", [])
    if not photos:
        return None
    return photos[0]["src"]["medium"]


total = len(PRODUCTS)
success = 0
skipped = 0
failed = []

print(f"Downloading {total} product images from Pexels...\n")

for i, (filename, query) in enumerate(PRODUCTS, 1):
    out_path = OUT_DIR / filename
    if out_path.exists() and out_path.stat().st_size > 5000:
        print(f"[{i}/{total}] SKIP (exists): {filename}")
        skipped += 1
        continue

    print(f"[{i}/{total}] Searching: {query}")
    try:
        img_url = search_pexels(query, API_KEY)
        if not img_url:
            print(f"         ❌ No results for: {query}")
            failed.append(filename)
            continue
        img_r = requests.get(img_url, headers={**HEADERS, "Referer": "https://www.pexels.com/"}, timeout=20)
        img_r.raise_for_status()
        img = Image.open(BytesIO(img_r.content)).convert("RGB")
        img.save(out_path, "WEBP", quality=82, method=6)
        size = out_path.stat().st_size
        print(f"         ✅ Saved {size//1024}KB — {filename}")
        success += 1
    except Exception as e:
        print(f"         ❌ Error: {e}")
        failed.append(filename)

    # Pexels free tier: 200 requests/hour — 0.3s gap is plenty
    time.sleep(0.4)

print(f"\n{'='*50}")
print(f"Done: {success} downloaded, {skipped} skipped, {len(failed)} failed")
if failed:
    print(f"Failed: {', '.join(failed)}")
print(f"\nNext step: Wire images into products.html by running:")
print(f"  python3 wire-product-images.py")
