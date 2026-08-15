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
    ("prod-dist-board.jpg",       "electrical distribution board panel"),
    ("prod-circuit-breaker.jpg",  "circuit breaker electrical panel"),
    ("prod-isolator.jpg",         "electrical isolator switch industrial"),
    ("prod-control-panel.jpg",    "electrical control panel components"),
    ("prod-capacitor.jpg",        "power capacitor bank industrial electrical"),
    ("prod-enclosure.jpg",        "electrical metal enclosure cabinet panel"),
    ("prod-panel-acc.jpg",        "electrical panel accessories din rail"),
    # CABLE MANAGEMENT
    ("prod-cable-gland.jpg",      "cable gland connector electrical"),
    ("prod-cable-tray.jpg",       "cable tray ladder perforated steel"),
    ("prod-steel-support.jpg",    "steel cable support bracket system"),
    ("prod-conduit-pvc.jpg",      "PVC conduit pipe trunking electrical"),
    ("prod-cable-ties.jpg",       "nylon cable ties bundle"),
    ("prod-floor-dist.jpg",       "floor box electrical socket distribution"),
    ("prod-cable-joint.jpg",      "cable jointing splice connector"),
    ("prod-steel-conduit.jpg",    "steel conduit pipe wiring box"),
    # CABLES
    ("prod-solar-cable.jpg",      "solar cable DC photovoltaic"),
    ("prod-coaxial.jpg",          "coaxial cable RF antenna"),
    ("prod-single-wire.jpg",      "single core copper electrical wire coloured"),
    ("prod-xlpe-cable.jpg",       "XLPE armoured electrical cable cross section"),
    ("prod-fire-cable.jpg",       "fire resistant cable red"),
    ("prod-multicore.jpg",        "multicore industrial cable"),
    ("prod-welding-cable.jpg",    "welding cable rubber flexible"),
    ("prod-battery-cable.jpg",    "battery cable heavy copper lug"),
    ("prod-fiber-optic.jpg",      "fiber optic cable data communication"),
    # PLUMBING
    ("prod-ppr-pipe.jpg",         "PPR green pipe fitting plumbing"),
    ("prod-upvc-pipe.jpg",        "UPVC white pipe fitting plumbing"),
    ("prod-hdpe-pipe.jpg",        "HDPE black pipe fitting polyethylene"),
    ("prod-pex-pipe.jpg",         "PEX flexible pipe red blue plumbing"),
    ("prod-pvc-pipe.jpg",         "PVC water pipe fitting white"),
    ("prod-hp-pipe.jpg",          "high pressure steel pipe industrial"),
    ("prod-drainage.jpg",         "drainage pipe channel system"),
    # SWITCHES & SOCKETS
    ("prod-switch-wp.jpg",        "waterproof electrical switch socket IP65"),
    ("prod-popup-switch.jpg",     "pop up floor electrical socket chrome"),
    ("prod-socket.jpg",           "wall electrical switch socket plate white"),
    ("prod-smart-switch.jpg",     "smart WiFi touch switch panel"),
    ("prod-grid-switch.jpg",      "modular grid switch socket module"),
    ("prod-metal-switch.jpg",     "metal clad industrial switch socket"),
    ("prod-sw-isolator.jpg",      "rotary isolator switch electrical"),
    # PAINTING
    ("prod-antifungal-paint.jpg", "anti fungal paint tin can wall"),
    ("prod-exterior-paint.jpg",   "exterior wall emulsion paint bucket"),
    ("prod-interior-paint.jpg",   "interior emulsion paint tin roller"),
    ("prod-fenomastic.jpg",       "premium paint tin can wall"),
    ("prod-emulsion.jpg",         "emulsion paint bucket roller tray"),
    ("prod-texture-paint.jpg",    "texture paint bucket wall"),
    ("prod-enamel-paint.jpg",     "enamel paint tin can metal"),
    ("prod-primer.jpg",           "primer undercoat paint can"),
    ("prod-wall-putty.jpg",       "wall putty powder bag"),
    # TOOLS
    ("prod-impact-wrench.jpg",    "cordless impact wrench power tool"),
    ("prod-angle-grinder.jpg",    "angle grinder power tool"),
    ("prod-power-tools.jpg",      "power tools set drill grinder"),
    ("prod-hand-tools.jpg",       "hand tools set hammer screwdriver pliers"),
    ("prod-tool-acc.jpg",         "power tool accessories drill bits"),
    ("prod-drill.jpg",            "hammer drill SDS power tool"),
    ("prod-router.jpg",           "wood router power tool"),
    ("prod-miter-saw.jpg",        "miter chop saw power tool"),
    ("prod-jigsaw.jpg",           "jigsaw power tool blade"),
    ("prod-hilti.jpg",            "Hilti professional drilling tool red"),
    # EARTHING & LIGHTNING
    ("prod-lightning.jpg",        "lightning protection air terminal rod"),
    ("prod-earthing.jpg",         "earthing rod grounding copper"),
    ("prod-copper-tape.jpg",      "copper tape earthing roll"),
    ("prod-air-terminal.jpg",     "lightning air terminal spike"),
    ("prod-prot-acc.jpg",         "earthing protection accessories clamps"),
    # SANITARY
    ("prod-sanitary.jpg",         "sanitary ware toilet basin bathroom"),
    ("prod-water-heater.jpg",     "electric water heater tank"),
    ("prod-sensor-tap.jpg",       "touchless sensor tap faucet chrome"),
    ("prod-shower.jpg",           "shower mixer tap set overhead chrome"),
    ("prod-tiles.jpg",            "ceramic floor wall tiles"),
    ("prod-valve.jpg",            "plumbing valve ball gate fitting"),
    # SAFETY
    ("prod-safety-shoes.jpg",     "steel toe safety boots shoes"),
    ("prod-harness.jpg",          "full body safety harness fall protection"),
    ("prod-helmet.jpg",           "construction safety hard hat helmet"),
    ("prod-ear-plug.jpg",         "ear plugs protectors safety"),
    ("prod-gloves.jpg",           "safety work gloves"),
    ("prod-hi-vis.jpg",           "high visibility vest coverall orange"),
    # HVAC
    ("prod-copper-coil.jpg",      "copper tube coil refrigeration HVAC"),
    ("prod-insulation.jpg",       "pipe insulation foam tube black"),
    ("prod-sheet-ins.jpg",        "thermal sheet insulation foam panel"),
    ("prod-refrigerant.jpg",      "refrigerant gas cylinder air conditioning"),
    ("prod-hvac-control.jpg",     "HVAC thermostat control panel"),
    ("prod-hvac-acc.jpg",         "HVAC duct fitting diffuser grille"),
    # LIGHTING
    ("prod-track-light.jpg",      "ceiling track light spotlight adjustable"),
    ("prod-panel-light.jpg",      "LED ceiling panel light flat"),
    ("prod-downlight.jpg",        "recessed LED downlight ceiling"),
    ("prod-spotlight.jpg",        "LED spotlight ceiling mounted"),
    ("prod-led-strip.jpg",        "LED strip light aluminium profile"),
    ("prod-linear-light.jpg",     "linear LED batten light fixture"),
    # PUMPS
    ("prod-centrifugal-pump.jpg", "centrifugal water pump industrial"),
    ("prod-pressure-pump.jpg",    "pressure booster pump set tank"),
    ("prod-transfer-pump.jpg",    "water transfer pump portable"),
    ("prod-booster-pump.jpg",     "water booster pump pressure vessel"),
    ("prod-pump-panel.jpg",       "pump motor control panel electrical"),
    ("prod-submersible.jpg",      "submersible water pump stainless steel"),
    # HARDWARE
    ("prod-nails.jpg",            "steel nails construction assortment"),
    ("prod-screws.jpg",           "wood metal screws assortment box"),
    ("prod-nuts-bolts.jpg",       "hex nuts bolts hardware stainless steel"),
    ("prod-anchor-bolt.jpg",      "concrete anchor bolt expansion"),
    ("prod-wire-rope.jpg",        "wire rope clips shackles rigging"),
    ("prod-ladder.jpg",           "aluminium ladder extension"),
    ("prod-wheelbarrow.jpg",      "construction wheelbarrow trolley"),
    ("prod-steel-tube.jpg",       "steel hollow tube section profile"),
    ("prod-tarpaulin.jpg",        "blue tarpaulin polythene sheet"),
    ("prod-thermocol.jpg",        "thermocol foam sheet polystyrene"),
    ("prod-masking-tape.jpg",     "masking tape roll yellow"),
    ("prod-duct-tape.jpg",        "duct tape roll silver grey"),
    ("prod-ins-tape.jpg",         "electrical insulation tape coloured"),
    ("prod-spanner.jpg",          "spanner wrench hand tools set"),
    ("prod-spirit-level.jpg",     "spirit level tool builder"),
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
        out_path.write_bytes(img_r.content)
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
