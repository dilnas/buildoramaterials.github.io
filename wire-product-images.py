"""
Run this after generate-product-images.py to add the images into products.html.
"""
import re
from pathlib import Path

PRODUCTS_HTML = Path("products.html")
IMG_DIR = Path("assets/images/products")

PRODUCT_MAP = {
    "Modular Distribution Board Components": "prod-dist-board.webp",
    "Main Distribution Panel Board Circuit Breakers": "prod-circuit-breaker.webp",
    "Load Break Isolators": "prod-isolator.webp",
    "Control Components": "prod-control-panel.webp",
    "Power Factor Capacitor Bank Components": "prod-capacitor.webp",
    "Distribution Boards &amp; Enclosures": "prod-enclosure.webp",
    "Panel Board Accessories": "prod-panel-acc.webp",
    "Cable Glands Lugs &amp; Connectors": "prod-cable-gland.webp",
    "Cable Trays &amp; Ladders": "prod-cable-tray.webp",
    "Steel Support Systems": "prod-steel-support.webp",
    "PVC Conduit &amp; Trunking Systems": "prod-conduit-pvc.webp",
    "Cable Ties &amp; Pulling Springs": "prod-cable-ties.webp",
    "Floor Distribution Systems": "prod-floor-dist.webp",
    "Cable Jointing Systems": "prod-cable-joint.webp",
    "Steel Conduit &amp; Wiring Boxes": "prod-steel-conduit.webp",
    "Solar Cables": "prod-solar-cable.webp",
    "Co-axial Cables": "prod-coaxial.webp",
    "Single Core Wires": "prod-single-wire.webp",
    "XLPE Insulated Cables": "prod-xlpe-cable.webp",
    "Fire Performance Cables": "prod-fire-cable.webp",
    "Multicore Industrial Cables": "prod-multicore.webp",
    "Rubber &amp; Welding Cables": "prod-welding-cable.webp",
    "Panel Switchboard &amp; Battery Cables": "prod-battery-cable.webp",
    "Data Fibre-optic &amp; Instrumentation Cables": "prod-fiber-optic.webp",
    "PPR Pipes &amp; Fittings": "prod-ppr-pipe.webp",
    "UPVC Pipes &amp; Fittings": "prod-upvc-pipe.webp",
    "HDPE Pipes &amp; Fittings": "prod-hdpe-pipe.webp",
    "Pex Pipes": "prod-pex-pipe.webp",
    "PVC White Pipes": "prod-pvc-pipe.webp",
    "High Pressure Pipes": "prod-hp-pipe.webp",
    "Drainage Pipes &amp; Systems": "prod-drainage.webp",
    "Waterproof Switch Sockets": "prod-switch-wp.webp",
    "Pop-up Switches": "prod-popup-switch.webp",
    "Switch Sockets Standard": "prod-socket.webp",
    "Smart Switches": "prod-smart-switch.webp",
    "Grid Switches &amp; Modules": "prod-grid-switch.webp",
    "Metal Clad Switches": "prod-metal-switch.webp",
    "Isolators": "prod-sw-isolator.webp",
    "Anti-Fungal Anti-Bacterial Paint": "prod-antifungal-paint.webp",
    "Exterior Emulsion": "prod-exterior-paint.webp",
    "Interior Emulsion": "prod-interior-paint.webp",
    "Fenomastic Paint": "prod-fenomastic.webp",
    "Emulsion Paint": "prod-emulsion.webp",
    "Texture Paint": "prod-texture-paint.webp",
    "Enamel Paint": "prod-enamel-paint.webp",
    "Primers &amp; Undercoats": "prod-primer.webp",
    "Wall Putty": "prod-wall-putty.webp",
    "Impact Wrench": "prod-impact-wrench.webp",
    "Angle Grinders": "prod-angle-grinder.webp",
    "Power Tools General": "prod-power-tools.webp",
    "Hand Tools": "prod-hand-tools.webp",
    "Tool Accessories": "prod-tool-acc.webp",
    "Drills &amp; Hammer Drills": "prod-drill.webp",
    "Routers": "prod-router.webp",
    "Chop Saws Miter Saws": "prod-miter-saw.webp",
    "Jig Saws": "prod-jigsaw.webp",
    "Hilti Systems": "prod-hilti.webp",
    "Lightning Protection Systems": "prod-lightning.webp",
    "Earthing Systems": "prod-earthing.webp",
    "Furse Copper Tape": "prod-copper-tape.webp",
    "Furse Air Terminals": "prod-air-terminal.webp",
    "Protection Accessories": "prod-prot-acc.webp",
    "Sanitary Fittings &amp; Ware": "prod-sanitary.webp",
    "Water Heaters": "prod-water-heater.webp",
    "Sensor Taps": "prod-sensor-tap.webp",
    "Mixer Taps &amp; Shower Sets": "prod-shower.webp",
    "Ceramics &amp; Tiles": "prod-tiles.webp",
    "Valves &amp; Fittings": "prod-valve.webp",
    "Safety Shoes": "prod-safety-shoes.webp",
    "Safety Harness": "prod-harness.webp",
    "Safety Helmets": "prod-helmet.webp",
    "Ear Plugs &amp; Protectors": "prod-ear-plug.webp",
    "Safety Gloves": "prod-gloves.webp",
    "Coveralls &amp; Hi-Vis Vests": "prod-hi-vis.webp",
    "Copper Coils &amp; Tubes": "prod-copper-coil.webp",
    "Pipe Insulation Aerofoam": "prod-insulation.webp",
    "Sheet Insulation": "prod-sheet-ins.webp",
    "Refrigerant Gas": "prod-refrigerant.webp",
    "HVAC Controls": "prod-hvac-control.webp",
    "HVAC Accessories": "prod-hvac-acc.webp",
    "Track Lights": "prod-track-light.webp",
    "Panel Lights": "prod-panel-light.webp",
    "Down Lights": "prod-downlight.webp",
    "Spot Lights": "prod-spotlight.webp",
    "LED Strips &amp; Profiles": "prod-led-strip.webp",
    "Linear Lights": "prod-linear-light.webp",
    "Water Pumps Centrifugal": "prod-centrifugal-pump.webp",
    "Pressure Kit Pressure Sets": "prod-pressure-pump.webp",
    "Transfer Pumps": "prod-transfer-pump.webp",
    "Booster Pumps": "prod-booster-pump.webp",
    "Control Panels for Pumps": "prod-pump-panel.webp",
    "Submersible Pumps": "prod-submersible.webp",
    "Steel Nails": "prod-nails.webp",
    "Screws": "prod-screws.webp",
    "Nuts &amp; Bolts": "prod-nuts-bolts.webp",
    "Anchor Bolts": "prod-anchor-bolt.webp",
    "Wire Rope Clips &amp; D-Shackles": "prod-wire-rope.webp",
    "Ladders": "prod-ladder.webp",
    "Wheelbarrow &amp; Platform Trolley": "prod-wheelbarrow.webp",
    "MS Tube &amp; Steel Sections": "prod-steel-tube.webp",
    "Polythene Sheets &amp; Tarpauline": "prod-tarpaulin.webp",
    "Thermocol Sheets": "prod-thermocol.webp",
    "Masking Tape": "prod-masking-tape.webp",
    "Duct Tape": "prod-duct-tape.webp",
    "Insulation Tape": "prod-ins-tape.webp",
    "Spanners &amp; Hand Tools": "prod-spanner.webp",
    "Spirit Level &amp; Manhole Cover": "prod-spirit-level.webp",
}

# Add CSS + inject images into HTML
html = PRODUCTS_HTML.read_text()

# Add .item-img CSS if not present
if "item-img" not in html:
    css_inject = """    .item-card {
      background: var(--white);
      padding: 1.2rem;"""
    css_new = """    .item-card {
      background: var(--white);
      padding: 0;
      overflow: hidden;"""
    img_css = """
    .item-img {
      width: 100%;
      height: 140px;
      object-fit: cover;
      display: block;
      transition: transform 0.3s;
    }
    .item-card:hover .item-img { transform: scale(1.04); }
    .item-body { padding: 1.2rem; }
"""
    html = html.replace(css_inject, css_new)
    # Insert img CSS before .item-name
    html = html.replace("    .item-name {", img_css + "    .item-name {", 1)

# Fix padding to use .item-body
if ".item-body" in html:
    # Wrap card content in .item-body
    pass  # handled below via split approach

# Inject <img> after each item-card opening tag
count = 0
parts = re.split(r'(<div class="item-card"[^>]*>)', html)
result = []
current_name = None

for j, part in enumerate(parts):
    result.append(part)
    if re.match(r'<div class="item-card"', part):
        # Look ahead for the product name in the next part
        next_part = parts[j + 1] if j + 1 < len(parts) else ""
        m = re.search(r"openWA\('([^']+)'\)", part)
        if not m:
            m = re.search(r"openWA\('([^']+)'\)", next_part)
        if m:
            raw_name = m.group(1)
            # Try exact match first, then HTML entity version
            filename = PRODUCT_MAP.get(raw_name) or PRODUCT_MAP.get(
                raw_name.replace("&", "&amp;")
            )
            if filename and (IMG_DIR / filename).exists():
                result.append(
                    f'\n          <img class="item-img" src="assets/images/products/{filename}" alt="{raw_name}" loading="lazy">\n          <div class="item-body">'
                )
                count += 1

output = "".join(result)

# Close item-body divs (add </div> before each </div> that closes item-card)
# Simple approach: add closing body div before item-quote closing
output = output.replace(
    '<span class="item-quote">',
    '</div><span class="item-quote">'  # close item-body
)
# Remove duplicate closes
output = re.sub(r'(</div>\s*){3,}(\s*</div>)', r'</div>\2', output)

PRODUCTS_HTML.write_text(output)
print(f"Done — injected images into {count} product cards.")
print("Run: git add -A && git push origin HEAD:refs/heads/\\(root\\)")
