"""
Run this after generate-product-images.py to add the images into products.html.
"""
import re
from pathlib import Path

PRODUCTS_HTML = Path("products.html")
IMG_DIR = Path("assets/images/products")

PRODUCT_MAP = {
    "Modular Distribution Board Components": "prod-dist-board.jpg",
    "Main Distribution Panel Board Circuit Breakers": "prod-circuit-breaker.jpg",
    "Load Break Isolators": "prod-isolator.jpg",
    "Control Components": "prod-control-panel.jpg",
    "Power Factor Capacitor Bank Components": "prod-capacitor.jpg",
    "Distribution Boards &amp; Enclosures": "prod-enclosure.jpg",
    "Panel Board Accessories": "prod-panel-acc.jpg",
    "Cable Glands Lugs &amp; Connectors": "prod-cable-gland.jpg",
    "Cable Trays &amp; Ladders": "prod-cable-tray.jpg",
    "Steel Support Systems": "prod-steel-support.jpg",
    "PVC Conduit &amp; Trunking Systems": "prod-conduit-pvc.jpg",
    "Cable Ties &amp; Pulling Springs": "prod-cable-ties.jpg",
    "Floor Distribution Systems": "prod-floor-dist.jpg",
    "Cable Jointing Systems": "prod-cable-joint.jpg",
    "Steel Conduit &amp; Wiring Boxes": "prod-steel-conduit.jpg",
    "Solar Cables": "prod-solar-cable.jpg",
    "Co-axial Cables": "prod-coaxial.jpg",
    "Single Core Wires": "prod-single-wire.jpg",
    "XLPE Insulated Cables": "prod-xlpe-cable.jpg",
    "Fire Performance Cables": "prod-fire-cable.jpg",
    "Multicore Industrial Cables": "prod-multicore.jpg",
    "Rubber &amp; Welding Cables": "prod-welding-cable.jpg",
    "Panel Switchboard &amp; Battery Cables": "prod-battery-cable.jpg",
    "Data Fibre-optic &amp; Instrumentation Cables": "prod-fiber-optic.jpg",
    "PPR Pipes &amp; Fittings": "prod-ppr-pipe.jpg",
    "UPVC Pipes &amp; Fittings": "prod-upvc-pipe.jpg",
    "HDPE Pipes &amp; Fittings": "prod-hdpe-pipe.jpg",
    "Pex Pipes": "prod-pex-pipe.jpg",
    "PVC White Pipes": "prod-pvc-pipe.jpg",
    "High Pressure Pipes": "prod-hp-pipe.jpg",
    "Drainage Pipes &amp; Systems": "prod-drainage.jpg",
    "Waterproof Switch Sockets": "prod-switch-wp.jpg",
    "Pop-up Switches": "prod-popup-switch.jpg",
    "Switch Sockets Standard": "prod-socket.jpg",
    "Smart Switches": "prod-smart-switch.jpg",
    "Grid Switches &amp; Modules": "prod-grid-switch.jpg",
    "Metal Clad Switches": "prod-metal-switch.jpg",
    "Isolators": "prod-sw-isolator.jpg",
    "Anti-Fungal Anti-Bacterial Paint": "prod-antifungal-paint.jpg",
    "Exterior Emulsion": "prod-exterior-paint.jpg",
    "Interior Emulsion": "prod-interior-paint.jpg",
    "Fenomastic Paint": "prod-fenomastic.jpg",
    "Emulsion Paint": "prod-emulsion.jpg",
    "Texture Paint": "prod-texture-paint.jpg",
    "Enamel Paint": "prod-enamel-paint.jpg",
    "Primers &amp; Undercoats": "prod-primer.jpg",
    "Wall Putty": "prod-wall-putty.jpg",
    "Impact Wrench": "prod-impact-wrench.jpg",
    "Angle Grinders": "prod-angle-grinder.jpg",
    "Power Tools General": "prod-power-tools.jpg",
    "Hand Tools": "prod-hand-tools.jpg",
    "Tool Accessories": "prod-tool-acc.jpg",
    "Drills &amp; Hammer Drills": "prod-drill.jpg",
    "Routers": "prod-router.jpg",
    "Chop Saws Miter Saws": "prod-miter-saw.jpg",
    "Jig Saws": "prod-jigsaw.jpg",
    "Hilti Systems": "prod-hilti.jpg",
    "Lightning Protection Systems": "prod-lightning.jpg",
    "Earthing Systems": "prod-earthing.jpg",
    "Furse Copper Tape": "prod-copper-tape.jpg",
    "Furse Air Terminals": "prod-air-terminal.jpg",
    "Protection Accessories": "prod-prot-acc.jpg",
    "Sanitary Fittings &amp; Ware": "prod-sanitary.jpg",
    "Water Heaters": "prod-water-heater.jpg",
    "Sensor Taps": "prod-sensor-tap.jpg",
    "Mixer Taps &amp; Shower Sets": "prod-shower.jpg",
    "Ceramics &amp; Tiles": "prod-tiles.jpg",
    "Valves &amp; Fittings": "prod-valve.jpg",
    "Safety Shoes": "prod-safety-shoes.jpg",
    "Safety Harness": "prod-harness.jpg",
    "Safety Helmets": "prod-helmet.jpg",
    "Ear Plugs &amp; Protectors": "prod-ear-plug.jpg",
    "Safety Gloves": "prod-gloves.jpg",
    "Coveralls &amp; Hi-Vis Vests": "prod-hi-vis.jpg",
    "Copper Coils &amp; Tubes": "prod-copper-coil.jpg",
    "Pipe Insulation Aerofoam": "prod-insulation.jpg",
    "Sheet Insulation": "prod-sheet-ins.jpg",
    "Refrigerant Gas": "prod-refrigerant.jpg",
    "HVAC Controls": "prod-hvac-control.jpg",
    "HVAC Accessories": "prod-hvac-acc.jpg",
    "Track Lights": "prod-track-light.jpg",
    "Panel Lights": "prod-panel-light.jpg",
    "Down Lights": "prod-downlight.jpg",
    "Spot Lights": "prod-spotlight.jpg",
    "LED Strips &amp; Profiles": "prod-led-strip.jpg",
    "Linear Lights": "prod-linear-light.jpg",
    "Water Pumps Centrifugal": "prod-centrifugal-pump.jpg",
    "Pressure Kit Pressure Sets": "prod-pressure-pump.jpg",
    "Transfer Pumps": "prod-transfer-pump.jpg",
    "Booster Pumps": "prod-booster-pump.jpg",
    "Control Panels for Pumps": "prod-pump-panel.jpg",
    "Submersible Pumps": "prod-submersible.jpg",
    "Steel Nails": "prod-nails.jpg",
    "Screws": "prod-screws.jpg",
    "Nuts &amp; Bolts": "prod-nuts-bolts.jpg",
    "Anchor Bolts": "prod-anchor-bolt.jpg",
    "Wire Rope Clips &amp; D-Shackles": "prod-wire-rope.jpg",
    "Ladders": "prod-ladder.jpg",
    "Wheelbarrow &amp; Platform Trolley": "prod-wheelbarrow.jpg",
    "MS Tube &amp; Steel Sections": "prod-steel-tube.jpg",
    "Polythene Sheets &amp; Tarpauline": "prod-tarpaulin.jpg",
    "Thermocol Sheets": "prod-thermocol.jpg",
    "Masking Tape": "prod-masking-tape.jpg",
    "Duct Tape": "prod-duct-tape.jpg",
    "Insulation Tape": "prod-ins-tape.jpg",
    "Spanners &amp; Hand Tools": "prod-spanner.jpg",
    "Spirit Level &amp; Manhole Cover": "prod-spirit-level.jpg",
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
