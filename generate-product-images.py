"""
Buildora Materials — Product Image Generator
Uses Google Gemini AI to generate a proper product photo for each of the 107 products.

Usage:
  export GEMINI_API_KEY="your-key-here"
  python3 generate-product-images.py

Get a free key at: https://aistudio.google.com/apikey
"""

import os, re, time, sys
from pathlib import Path
from io import BytesIO
from PIL import Image
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not set.")
    print("Get a free key at: https://aistudio.google.com/apikey")
    print("Then run:  export GEMINI_API_KEY=\"your-key\"")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
OUT_DIR = Path("assets/images/products")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Each product: (filename, prompt for Gemini)
PRODUCTS = [
    # ELECTRICAL
    ("prod-dist-board.webp",    "Professional product photo of a modular electrical distribution board with MCB circuit breakers mounted inside, white background, studio lighting"),
    ("prod-circuit-breaker.webp","Professional product photo of industrial MCCB main circuit breaker for distribution panel, white background, studio lighting"),
    ("prod-isolator.webp",      "Professional product photo of an electrical load break isolator switch, grey enclosure, white background, studio lighting"),
    ("prod-control-panel.webp", "Professional product photo of electrical control panel components: contactors, relays, terminal blocks, white background, studio lighting"),
    ("prod-capacitor.webp",     "Professional product photo of power factor correction capacitor bank unit, industrial equipment, white background, studio lighting"),
    ("prod-enclosure.webp",     "Professional product photo of a metal electrical enclosure panel board cabinet, grey steel, white background, studio lighting"),
    ("prod-panel-acc.webp",     "Professional product photo of electrical panel board accessories: DIN rail, cable duct, terminal blocks, white background, studio lighting"),
    # CABLE MANAGEMENT
    ("prod-cable-gland.webp",   "Professional product photo of cable glands, lugs and connectors assortment on white background, studio lighting"),
    ("prod-cable-tray.webp",    "Professional product photo of steel perforated cable tray ladder system, galvanised, white background, studio lighting"),
    ("prod-steel-support.webp", "Professional product photo of steel cable support brackets and strut channel system, white background, studio lighting"),
    ("prod-conduit-pvc.webp",   "Professional product photo of grey PVC conduit pipes and trunking cable management system, white background, studio lighting"),
    ("prod-cable-ties.webp",    "Professional product photo of nylon cable ties bundle assortment, black and white, white background, studio lighting"),
    ("prod-floor-dist.webp",    "Professional product photo of underfloor cable distribution box and floor socket system, white background, studio lighting"),
    ("prod-cable-joint.webp",   "Professional product photo of cable jointing kit and straight through splice connectors, white background, studio lighting"),
    ("prod-steel-conduit.webp", "Professional product photo of steel conduit pipes and metal wiring junction boxes, grey, white background, studio lighting"),
    # CABLES
    ("prod-solar-cable.webp",   "Professional product photo of solar DC cables red and black, UV resistant, coiled on white background, studio lighting"),
    ("prod-coaxial.webp",       "Professional product photo of coaxial cable cross section and coil, RF cable, white background, studio lighting"),
    ("prod-single-wire.webp",   "Professional product photo of single core copper electrical wires in multiple colours, white background, studio lighting"),
    ("prod-xlpe-cable.webp",    "Professional product photo of XLPE insulated armoured electrical cable cross section showing layers, white background, studio lighting"),
    ("prod-fire-cable.webp",    "Professional product photo of fire performance resistant cable, red sheath, coiled, white background, studio lighting"),
    ("prod-multicore.webp",     "Professional product photo of multicore industrial cable cross section and coil, white background, studio lighting"),
    ("prod-welding-cable.webp", "Professional product photo of rubber welding cable heavy duty flexible, yellow and black, white background, studio lighting"),
    ("prod-battery-cable.webp", "Professional product photo of battery and switchboard cables with lugs, heavy copper, white background, studio lighting"),
    ("prod-fiber-optic.webp",   "Professional product photo of fiber optic cable cross section showing glass fibers and data cable bundle, white background, studio lighting"),
    # PLUMBING
    ("prod-ppr-pipe.webp",      "Professional product photo of green PPR pipes and fittings elbows tees, polypropylene plumbing, white background, studio lighting"),
    ("prod-upvc-pipe.webp",     "Professional product photo of white UPVC pipes and fittings for plumbing, white background, studio lighting"),
    ("prod-hdpe-pipe.webp",     "Professional product photo of black HDPE high density polyethylene pipes and fittings, white background, studio lighting"),
    ("prod-pex-pipe.webp",      "Professional product photo of flexible PEX pipes red and blue coils with brass fittings, white background, studio lighting"),
    ("prod-pvc-pipe.webp",      "Professional product photo of white PVC water supply pipes and fittings, white background, studio lighting"),
    ("prod-hp-pipe.webp",       "Professional product photo of high pressure industrial steel pipes and fittings, white background, studio lighting"),
    ("prod-drainage.webp",      "Professional product photo of drainage pipes and channel system, grey PVC, white background, studio lighting"),
    # SWITCHES
    ("prod-switch-wp.webp",     "Professional product photo of waterproof IP rated electrical switch socket, white or grey, white background, studio lighting"),
    ("prod-popup-switch.webp",  "Professional product photo of pop-up floor electrical socket switch module, chrome finish, white background, studio lighting"),
    ("prod-socket.webp",        "Professional product photo of standard wall electrical switch socket plate, white plastic, white background, studio lighting"),
    ("prod-smart-switch.webp",  "Professional product photo of smart WiFi electrical switch panel with touch screen, modern, white background, studio lighting"),
    ("prod-grid-switch.webp",   "Professional product photo of modular grid switch and socket modules, white background, studio lighting"),
    ("prod-metal-switch.webp",  "Professional product photo of metal clad industrial electrical switch socket, grey steel, white background, studio lighting"),
    ("prod-sw-isolator.webp",   "Professional product photo of electrical isolator switch rotary disconnector, industrial, white background, studio lighting"),
    # PAINTING
    ("prod-antifungal-paint.webp","Professional product photo of anti-fungal anti-bacterial wall paint tin can, white background, studio lighting"),
    ("prod-exterior-paint.webp","Professional product photo of exterior wall emulsion paint bucket and brush, white background, studio lighting"),
    ("prod-interior-paint.webp","Professional product photo of interior emulsion wall paint tin and roller, white background, studio lighting"),
    ("prod-fenomastic.webp",    "Professional product photo of premium Jotun Fenomastic paint tin can, white background, studio lighting"),
    ("prod-emulsion.webp",      "Professional product photo of emulsion paint bucket with paint roller and tray, white background, studio lighting"),
    ("prod-texture-paint.webp", "Professional product photo of texture paint bucket with textured wall sample, white background, studio lighting"),
    ("prod-enamel-paint.webp",  "Professional product photo of enamel paint tin cans for metal and wood, white background, studio lighting"),
    ("prod-primer.webp",        "Professional product photo of wall primer and undercoat paint cans, white background, studio lighting"),
    ("prod-wall-putty.webp",    "Professional product photo of wall putty powder bag and mixing tools, white background, studio lighting"),
    # TOOLS
    ("prod-impact-wrench.webp", "Professional product photo of cordless impact wrench power tool, yellow and black, white background, studio lighting"),
    ("prod-angle-grinder.webp", "Professional product photo of angle grinder power tool with grinding disc, white background, studio lighting"),
    ("prod-power-tools.webp",   "Professional product photo of power tools set: drill, grinder, saw on white background, studio lighting"),
    ("prod-hand-tools.webp",    "Professional product photo of hand tools set: hammer, screwdrivers, pliers, spanner on white background, studio lighting"),
    ("prod-tool-acc.webp",      "Professional product photo of power tool accessories: drill bits, saw blades, sanding discs on white background, studio lighting"),
    ("prod-drill.webp",         "Professional product photo of rotary hammer drill SDS power tool, professional, white background, studio lighting"),
    ("prod-router.webp",        "Professional product photo of wood router power tool with guide, white background, studio lighting"),
    ("prod-miter-saw.webp",     "Professional product photo of compound miter chop saw power tool, white background, studio lighting"),
    ("prod-jigsaw.webp",        "Professional product photo of jigsaw power tool with blade, white background, studio lighting"),
    ("prod-hilti.webp",         "Professional product photo of professional Hilti drilling and anchoring system power tool, red, white background, studio lighting"),
    # EARTHING
    ("prod-lightning.webp",     "Professional product photo of lightning protection air terminal rod on white background, studio lighting"),
    ("prod-earthing.webp",      "Professional product photo of copper earthing rod and earth clamp grounding system, white background, studio lighting"),
    ("prod-copper-tape.webp",   "Professional product photo of copper earthing tape roll for lightning protection, white background, studio lighting"),
    ("prod-air-terminal.webp",  "Professional product photo of Furse lightning protection air terminal spike, white background, studio lighting"),
    ("prod-prot-acc.webp",      "Professional product photo of earthing and lightning protection accessories: clamps, bonds, fittings, white background, studio lighting"),
    # SANITARY
    ("prod-sanitary.webp",      "Professional product photo of premium sanitary ware: toilet, basin, chrome fittings on white background, studio lighting"),
    ("prod-water-heater.webp",  "Professional product photo of electric water heater storage tank unit, white, white background, studio lighting"),
    ("prod-sensor-tap.webp",    "Professional product photo of touchless sensor tap faucet chrome finish, white background, studio lighting"),
    ("prod-shower.webp",        "Professional product photo of shower mixer tap set with overhead shower head, chrome, white background, studio lighting"),
    ("prod-tiles.webp",         "Professional product photo of ceramic floor and wall tiles stack, various designs, white background, studio lighting"),
    ("prod-valve.webp",         "Professional product photo of plumbing valves and fittings: ball valve, gate valve, chrome and brass, white background, studio lighting"),
    # SAFETY
    ("prod-safety-shoes.webp",  "Professional product photo of steel toe safety boots and shoes, black, white background, studio lighting"),
    ("prod-harness.webp",       "Professional product photo of full body safety harness fall protection equipment, orange and black, white background, studio lighting"),
    ("prod-helmet.webp",        "Professional product photo of construction safety hard hat helmet, yellow and white, white background, studio lighting"),
    ("prod-ear-plug.webp",      "Professional product photo of ear plugs and ear muff protectors safety equipment, white background, studio lighting"),
    ("prod-gloves.webp",        "Professional product photo of safety work gloves cut resistant and chemical resistant, white background, studio lighting"),
    ("prod-hi-vis.webp",        "Professional product photo of high visibility vest and coverall workwear, orange and yellow, white background, studio lighting"),
    # HVAC
    ("prod-copper-coil.webp",   "Professional product photo of copper refrigeration coil tubes for HVAC, shiny, white background, studio lighting"),
    ("prod-insulation.webp",    "Professional product photo of pipe insulation foam Aerofoam tube sections, black, white background, studio lighting"),
    ("prod-sheet-ins.webp",     "Professional product photo of thermal sheet insulation foam panels for HVAC, white background, studio lighting"),
    ("prod-refrigerant.webp",   "Professional product photo of refrigerant gas cylinder canister for air conditioning, white background, studio lighting"),
    ("prod-hvac-control.webp",  "Professional product photo of HVAC control panel thermostat and controller unit, white background, studio lighting"),
    ("prod-hvac-acc.webp",      "Professional product photo of HVAC accessories: duct fittings, diffusers, grilles, white background, studio lighting"),
    # LIGHTING
    ("prod-track-light.webp",   "Professional product photo of ceiling track light system with adjustable spotlights, white background, studio lighting"),
    ("prod-panel-light.webp",   "Professional product photo of LED ceiling panel light flat square, white, white background, studio lighting"),
    ("prod-downlight.webp",     "Professional product photo of recessed LED downlight ceiling fixture, white background, studio lighting"),
    ("prod-spotlight.webp",     "Professional product photo of LED spotlight adjustable ceiling mounted, white background, studio lighting"),
    ("prod-led-strip.webp",     "Professional product photo of LED strip light reel and aluminium profile channel, white background, studio lighting"),
    ("prod-linear-light.webp",  "Professional product photo of linear LED batten light fixture suspended ceiling, white background, studio lighting"),
    # PUMPS
    ("prod-centrifugal-pump.webp","Professional product photo of centrifugal water pump industrial motor unit, white background, studio lighting"),
    ("prod-pressure-pump.webp", "Professional product photo of pressure booster pump set with pressure tank, white background, studio lighting"),
    ("prod-transfer-pump.webp", "Professional product photo of water transfer pump portable industrial, white background, studio lighting"),
    ("prod-booster-pump.webp",  "Professional product photo of water booster pump system with pressure vessel, white background, studio lighting"),
    ("prod-pump-panel.webp",    "Professional product photo of pump motor control panel electrical cabinet, white background, studio lighting"),
    ("prod-submersible.webp",   "Professional product photo of submersible water pump stainless steel, white background, studio lighting"),
    # HARDWARE
    ("prod-nails.webp",         "Professional product photo of steel construction nails assortment scattered, white background, studio lighting"),
    ("prod-screws.webp",        "Professional product photo of wood and metal screws assortment in compartment box, white background, studio lighting"),
    ("prod-nuts-bolts.webp",    "Professional product photo of hex nuts and bolts hardware assortment, stainless steel, white background, studio lighting"),
    ("prod-anchor-bolt.webp",   "Professional product photo of concrete anchor bolts expansion anchors assortment, white background, studio lighting"),
    ("prod-wire-rope.webp",     "Professional product photo of wire rope clips bulldog grips and D-shackles rigging hardware, white background, studio lighting"),
    ("prod-ladder.webp",        "Professional product photo of aluminium extension ladder, white background, studio lighting"),
    ("prod-wheelbarrow.webp",   "Professional product photo of construction wheelbarrow and platform trolley, white background, studio lighting"),
    ("prod-steel-tube.webp",    "Professional product photo of mild steel hollow tube sections and steel profiles, white background, studio lighting"),
    ("prod-tarpaulin.webp",     "Professional product photo of blue polythene tarpaulin sheet and protective sheeting roll, white background, studio lighting"),
    ("prod-thermocol.webp",     "Professional product photo of white thermocol expanded polystyrene foam sheets, white background, studio lighting"),
    ("prod-masking-tape.webp",  "Professional product photo of masking tape rolls yellow, white background, studio lighting"),
    ("prod-duct-tape.webp",     "Professional product photo of duct tape rolls silver grey, white background, studio lighting"),
    ("prod-ins-tape.webp",      "Professional product photo of electrical insulation tape rolls in multiple colours, white background, studio lighting"),
    ("prod-spanner.webp",       "Professional product photo of spanners and hand tools set on white background, studio lighting"),
    ("prod-spirit-level.webp",  "Professional product photo of spirit level tool and manhole cover utility, white background, studio lighting"),
]

total = len(PRODUCTS)
success = 0
skipped = 0
failed = []

print(f"Generating {total} product images with Gemini AI...\n")

for i, (filename, prompt) in enumerate(PRODUCTS, 1):
    out_path = OUT_DIR / filename
    if out_path.exists() and out_path.stat().st_size > 10000:
        print(f"[{i}/{total}] SKIP (exists): {filename}")
        skipped += 1
        continue

    print(f"[{i}/{total}] Generating: {filename}")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"]
            )
        )
        saved = False
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                img = Image.open(BytesIO(part.inline_data.data)).convert("RGB")
                img.save(out_path, "WEBP", quality=82, method=6)
                size = out_path.stat().st_size
                print(f"         ✅ Saved {size//1024}KB")
                success += 1
                saved = True
                break
        if not saved:
            print(f"         ❌ No image in response")
            failed.append(filename)
    except Exception as e:
        print(f"         ❌ Error: {e}")
        failed.append(filename)

    # Respect rate limits
    if i % 10 == 0:
        print("  (pausing 5s for rate limit...)")
        time.sleep(5)
    else:
        time.sleep(1)

print(f"\n{'='*50}")
print(f"Done: {success} generated, {skipped} skipped, {len(failed)} failed")
if failed:
    print(f"Failed: {', '.join(failed)}")
print(f"\nNext step: Add images to products.html by running:")
print(f"  python3 wire-product-images.py")
