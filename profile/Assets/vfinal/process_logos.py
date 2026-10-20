import xml.etree.ElementTree as ET
import re
import os
import fitz

SVG_SRC = r'C:\Users\USER\Desktop\Extras\ZenOska\.github\Assets\vfinal\zenOska_logo_com.svg'
ASSETS_DIR = r'C:\Users\USER\Desktop\Extras\ZenOska\.github\Assets'
VFINAL_DIR = r'C:\Users\USER\Desktop\Extras\ZenOska\.github\Assets\vfinal'

tree = ET.parse(SVG_SRC)
root = tree.getroot()

dark_paths = []
light_paths = []
dark_zo_paths = []
light_zo_paths = []

for elem in root.iter():
    if elem.tag.endswith('path'):
        tr = elem.attrib.get('transform', '')
        fill = elem.attrib.get('fill', '')
        d = elem.attrib.get('d', '')
        m = re.match(r'translate\(([^,]+),([^)]+)\)', tr)
        if m:
            tx, ty = float(m.group(1)), float(m.group(2))
            if tx == 0 and ty == 0 and fill in ['#FDFDFD', '#020202']:
                continue
            # Logo is at y <= 540; text is at y > 540
            if ty <= 540:
                if tx < 800:
                    dark_paths.append((tx, ty, fill, d))
                    if tx < 360:
                        dark_zo_paths.append((tx, ty, fill, d))
                else:
                    # light mode paths (normalized to x - 800)
                    tx_rel = tx - 800.0
                    light_paths.append((tx_rel, ty, fill, d))
                    if tx_rel < 360:
                        light_zo_paths.append((tx_rel, ty, fill, d))

print(f"Extracted {len(dark_paths)} dark logo paths, {len(light_paths)} light logo paths.")
print(f"Extracted {len(dark_zo_paths)} dark Z+O monogram paths, {len(light_zo_paths)} light Z+O monogram paths.")

# Center offsets for 800x800 square
# Dark logo bounds: cx = 421.4, cy = 349.45
dx_d = 400.0 - 421.4
dy_d = 400.0 - 349.45

# Light logo bounds: cx_rel = 419.4, cy = 352.75
dx_l = 400.0 - 419.4
dy_l = 400.0 - 352.75

# 1. GENERATE REFINED zenOska_logo_com.svg (Side by Side, no bottom text)
com_svg = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="1600" height="800" viewBox="0 0 1600 800">',
    '  <!-- Dark Mode Background (Left Half) -->',
    '  <rect x="0" y="0" width="800" height="800" fill="#020202"/>',
    '  <!-- Light Mode Background (Right Half) -->',
    '  <rect x="800" y="0" width="800" height="800" fill="#FFFFFF"/>',
    f'  <!-- Dark Mode Logo (Centered) -->',
    f'  <g id="dark-mode-logo" transform="translate({dx_d:.2f}, {dy_d:.2f})">'
]
for tx, ty, fill, d in dark_paths:
    com_svg.append(f'    <path d="{d}" fill="{fill}" transform="translate({tx:.4f},{ty:.4f})"/>')
com_svg.append('  </g>')

com_svg.append(f'  <!-- Light Mode Logo (Centered in Right Half) -->')
com_svg.append(f'  <g id="light-mode-logo" transform="translate({dx_l + 800.0:.2f}, {dy_l:.2f})">')
for tx, ty, fill, d in light_paths:
    com_svg.append(f'    <path d="{d}" fill="{fill}" transform="translate({tx:.4f},{ty:.4f})"/>')
com_svg.append('  </g>')
com_svg.append('</svg>')

with open(SVG_SRC, 'w', encoding='utf-8') as f:
    f.write('\n'.join(com_svg))
print("Saved refined zenOska_logo_com.svg")

# 2. GENERATE SQUARE LOGOS (800x800)
def generate_square_logo(paths, dx, dy, bg_color, output_path, logo_id):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">',
        f'  <rect width="800" height="800" fill="{bg_color}"/>',
        f'  <g id="{logo_id}" transform="translate({dx:.2f}, {dy:.2f})">'
    ]
    for tx, ty, fill, d in paths:
        lines.append(f'    <path d="{d}" fill="{fill}" transform="translate({tx:.4f},{ty:.4f})"/>')
    lines.append('  </g>')
    lines.append('</svg>')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

generate_square_logo(dark_paths, dx_d, dy_d, '#020202', os.path.join(VFINAL_DIR, 'zenOska_logo_dark.svg'), 'zenoska-logo-dark')
generate_square_logo(light_paths, dx_l, dy_l, '#FFFFFF', os.path.join(VFINAL_DIR, 'zenOska_logo_light.svg'), 'zenoska-logo-light')
generate_square_logo(dark_paths, dx_d, dy_d, '#020202', os.path.join(ASSETS_DIR, 'zenoska-logo-dark.svg'), 'zenoska-logo-dark')
generate_square_logo(light_paths, dx_l, dy_l, '#FFFFFF', os.path.join(ASSETS_DIR, 'zenoska-logo-light.svg'), 'zenoska-logo-light')
generate_square_logo(dark_paths, dx_d, dy_d, '#020202', os.path.join(ASSETS_DIR, 'zenoska-logo.svg'), 'zenoska-logo')

# 3. GENERATE BANNERS (1200x320)
# In 1200x320, we scale logo by scale = 0.58.
# Logo original center cx = 421.4, cy = 349.45.
# Target center in banner: X = 600, Y = 138.
# transform: translate(600, 138) scale(0.58) translate(-cx, -cy)
def generate_banner(paths, orig_cx, orig_cy, bg_color, border_stroke, text_fill, output_path, banner_id):
    scale = 0.58
    target_cx = 600.0
    target_cy = 138.0
    border_tag = f' stroke="{border_stroke}" stroke-width="1.5"' if border_stroke else ''
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320">',
        f'  <rect width="1200" height="320" rx="12" fill="{bg_color}"{border_tag}/>',
        f'  <g id="{banner_id}" transform="translate({target_cx:.1f}, {target_cy:.1f}) scale({scale:.3f}) translate({-orig_cx:.2f}, {-orig_cy:.2f})">'
    ]
    for tx, ty, fill, d in paths:
        lines.append(f'    <path d="{d}" fill="{fill}" transform="translate({tx:.4f},{ty:.4f})"/>')
    lines.append('  </g>')
    lines.append(f'  <text x="600" y="272" text-anchor="middle" font-family="system-ui, -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="13" font-weight="600" letter-spacing="0.32em" fill="{text_fill}">SOVEREIGN MACHINE COGNITION</text>')
    lines.append('</svg>')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

generate_banner(dark_paths, 421.4, 349.45, '#020202', None, '#8B8E99', os.path.join(VFINAL_DIR, 'zenOska_banner_dark.svg'), 'zenoska-banner-dark')
generate_banner(light_paths, 419.4, 352.75, '#FFFFFF', '#E2E4E9', '#6B7280', os.path.join(VFINAL_DIR, 'zenOska_banner_light.svg'), 'zenoska-banner-light')
generate_banner(dark_paths, 421.4, 349.45, '#020202', None, '#8B8E99', os.path.join(ASSETS_DIR, 'zenoska-banner-dark.svg'), 'zenoska-banner-dark')
generate_banner(light_paths, 419.4, 352.75, '#FFFFFF', '#E2E4E9', '#6B7280', os.path.join(ASSETS_DIR, 'zenoska-banner-light.svg'), 'zenoska-banner-light')
generate_banner(dark_paths, 421.4, 349.45, '#020202', None, '#8B8E99', os.path.join(ASSETS_DIR, 'zenoska-banner.svg'), 'zenoska-banner')

# 4. GENERATE MONOGRAMS (512x512)
# Z+O bounds:
# Dark: X in 102..338 (width 236), Y in 178..520 (height 342)
# Center: cx = 220, cy = 349.
# Target center in 512x512: (256, 256), scale = 1.15
def generate_monogram(paths, orig_cx, orig_cy, bg_color, output_path, mono_id):
    scale = 1.15
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">',
        f'  <rect width="512" height="512" rx="112" fill="{bg_color}"/>',
        f'  <g id="{mono_id}" transform="translate(256, 256) scale({scale:.2f}) translate({-orig_cx:.2f}, {-orig_cy:.2f})">'
    ]
    for tx, ty, fill, d in paths:
        lines.append(f'    <path d="{d}" fill="{fill}" transform="translate({tx:.4f},{ty:.4f})"/>')
    lines.append('  </g>')
    lines.append('</svg>')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

generate_monogram(dark_zo_paths, 220.0, 349.45, '#020202', os.path.join(VFINAL_DIR, 'zenOska_monogram_dark.svg'), 'zenoska-monogram-dark')
generate_monogram(light_zo_paths, 220.0, 352.75, '#FFFFFF', os.path.join(VFINAL_DIR, 'zenOska_monogram_light.svg'), 'zenoska-monogram-light')
generate_monogram(dark_zo_paths, 220.0, 349.45, '#020202', os.path.join(ASSETS_DIR, 'zenoska-monogram-dark.svg'), 'zenoska-monogram-dark')
generate_monogram(light_zo_paths, 220.0, 352.75, '#FFFFFF', os.path.join(ASSETS_DIR, 'zenoska-monogram-light.svg'), 'zenoska-monogram-light')
generate_monogram(dark_zo_paths, 220.0, 349.45, '#020202', os.path.join(ASSETS_DIR, 'zenoska-monogram.svg'), 'zenoska-monogram')

# Render preview PNGs for visual inspection
fitz.open(SVG_SRC)[0].get_pixmap(dpi=150).save(os.path.join(VFINAL_DIR, 'preview_com.png'))
fitz.open(os.path.join(ASSETS_DIR, 'zenoska-logo-dark.svg'))[0].get_pixmap(dpi=150).save(os.path.join(VFINAL_DIR, 'preview_logo_dark.png'))
fitz.open(os.path.join(ASSETS_DIR, 'zenoska-logo-light.svg'))[0].get_pixmap(dpi=150).save(os.path.join(VFINAL_DIR, 'preview_logo_light.png'))
fitz.open(os.path.join(ASSETS_DIR, 'zenoska-banner-dark.svg'))[0].get_pixmap(dpi=150).save(os.path.join(VFINAL_DIR, 'preview_banner_dark.png'))
fitz.open(os.path.join(ASSETS_DIR, 'zenoska-banner-light.svg'))[0].get_pixmap(dpi=150).save(os.path.join(VFINAL_DIR, 'preview_banner_light.png'))
fitz.open(os.path.join(ASSETS_DIR, 'zenoska-monogram-dark.svg'))[0].get_pixmap(dpi=150).save(os.path.join(VFINAL_DIR, 'preview_mono_dark.png'))
fitz.open(os.path.join(ASSETS_DIR, 'zenoska-monogram-light.svg'))[0].get_pixmap(dpi=150).save(os.path.join(VFINAL_DIR, 'preview_mono_light.png'))

print("All assets generated and previews rendered successfully!")
