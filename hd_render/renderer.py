"""
Human Design Bodygraph SVG Renderer

Generates a complete bodygraph SVG from a ChartResult dict.
"""

import math
from hd_render import styles as S
from hd_constants import CENTERS, CHANNELS, GATE_TO_CHANNELS, TYPES, AUTHORITY_PRIORITY

# ============================================================
# Gate position offsets per center (angle around center perimeter)
# These map gate numbers to angular positions on each center's boundary
# ============================================================

def _build_gate_positions():
    """Calculate gate marker positions on each center's perimeter."""
    positions = {}
    for center_name, center_data in CENTERS.items():
        pos = S.CENTER_POSITIONS[center_name]
        cx, cy = pos['x'], pos['y']
        rx, ry = pos['rx'], pos['ry']
        gates = center_data['gates']
        n = len(gates)
        positions[center_name] = {}
        for i, gate in enumerate(gates):
            # Distribute gates evenly around the center perimeter
            # Start from top, go clockwise
            angle = -math.pi / 2 + (2 * math.pi * i / n)
            # Place gate markers further outside the center shape to avoid overlap
            offset = 1.35
            gx = cx + rx * offset * math.cos(angle)
            gy = cy + ry * offset * math.sin(angle)
            positions[center_name][gate] = (gx, gy, angle)
    return positions

GATE_POSITIONS = _build_gate_positions()

# Reverse: gate -> (center, x, y, angle)
GATE_TO_POSITION = {}
for center, gates in GATE_POSITIONS.items():
    for gate, (gx, gy, angle) in gates.items():
        GATE_TO_POSITION[gate] = (center, gx, gy, angle)


def _determine_channel_type(personality_gates, design_gates, g1, g2):
    """Determine if a channel is personality (black), design (red), or both (striped)."""
    p1 = g1 in personality_gates
    p2 = g2 in personality_gates
    d1 = g1 in design_gates
    d2 = g2 in design_gates

    has_p = p1 or p2
    has_d = d1 or d2

    if has_p and has_d:
        return 'both'
    elif has_p:
        return 'personality'
    else:
        return 'design'


def _determine_gate_type(personality_gates, design_gates, gate):
    """Determine if a gate is personality, design, or both."""
    in_p = gate in personality_gates
    in_d = gate in design_gates

    if in_p and in_d:
        return 'both'
    elif in_p:
        return 'personality'
    else:
        return 'design'


def _get_authority(chart):
    """Determine authority from defined centers."""
    defined = set(chart.get('defined_centers', []))
    for center, info in AUTHORITY_PRIORITY:
        if center is None:
            return info['en']
        if center in defined:
            return info['en']
    return 'No Authority'


def _get_strategy(chart):
    """Get strategy from type."""
    hd_type = chart.get('type', 'Generator')
    type_info = TYPES.get(hd_type, TYPES['Generator'])
    return type_info['strategy_en']


def _center_shape_svg(center_name, cx, cy, rx, ry, defined, activated_gates):
    """Generate SVG for a single center shape."""
    color = S.CENTER_COLORS[center_name]
    border_color = S.CENTER_BORDER_COLORS[center_name]
    shape = S.CENTER_SHAPES[center_name]
    
    if defined:
        fill = color
        stroke = _darken(color, 0.3)
        stroke_w = 2
        fill_opacity = 0.85
    else:
        fill = S.UNDEFINED_FILL
        stroke = border_color
        stroke_w = S.UNDEFINED_BORDER_WIDTH
        fill_opacity = 0.4
    
    # Adjust rx/ry for shapes
    path = ''
    if shape == 'triangle_up':
        pts = [
            (cx, cy - ry),
            (cx + rx, cy + ry * 0.7),
            (cx - rx, cy + ry * 0.7),
        ]
        path = f'M {pts[0][0]},{pts[0][1]} L {pts[1][0]},{pts[1][1]} L {pts[2][0]},{pts[2][1]} Z'
    elif shape == 'triangle_down':
        pts = [
            (cx, cy + ry),
            (cx + rx, cy - ry * 0.7),
            (cx - rx, cy - ry * 0.7),
        ]
        path = f'M {pts[0][0]},{pts[0][1]} L {pts[1][0]},{pts[1][1]} L {pts[2][0]},{pts[2][1]} Z'
    elif shape == 'diamond':
        pts = [
            (cx, cy - ry),
            (cx + rx, cy),
            (cx, cy + ry),
            (cx - rx, cy),
        ]
        path = f'M {pts[0][0]},{pts[0][1]} L {pts[1][0]},{pts[1][1]} L {pts[2][0]},{pts[2][1]} L {pts[3][0]},{pts[3][1]} Z'
    elif shape in ('square', 'square_small'):
        r = rx * 0.9
        path = f'M {cx-r},{cy-ry*0.8} L {cx+r},{cy-ry*0.8} L {cx+r},{cy+ry*0.8} L {cx-r},{cy+ry*0.8} Z'
    else:  # circle fallback
        path = ''
    
    svg = ''
    if path:
        svg += f'  <path d="{path}" fill="{fill}" fill-opacity="{fill_opacity}" stroke="{stroke}" stroke-width="{stroke_w}" stroke-linejoin="round"/>\n'
    else:
        svg += f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" fill-opacity="{fill_opacity}" stroke="{stroke}" stroke-width="{stroke_w}"/>\n'
    
    # Gate numbers inside the center
    if activated_gates:
        gate_strs = [str(g) for g in sorted(activated_gates)]
        font_color = '#1a1a1a' if defined else '#8888aa'
        # For many gates, split into two lines
        if len(gate_strs) > 4:
            mid = len(gate_strs) // 2
            line1 = ' '.join(gate_strs[:mid])
            line2 = ' '.join(gate_strs[mid:])
            font_size = min(11, max(8, 120 // max(len(gate_strs), 1)))
            svg += f'  <text x="{cx}" y="{cy - 5}" text-anchor="middle" dominant-baseline="middle" font-family="{S.HEADER_FONT}" font-size="{font_size}" fill="{font_color}" font-weight="600">{line1}</text>\n'
            svg += f'  <text x="{cx}" y="{cy + 9}" text-anchor="middle" dominant-baseline="middle" font-family="{S.HEADER_FONT}" font-size="{font_size}" fill="{font_color}" font-weight="600">{line2}</text>\n'
        elif len(gate_strs) > 2:
            text = ' '.join(gate_strs)
            font_size = min(12, max(9, 140 // max(len(gate_strs), 1)))
            svg += f'  <text x="{cx}" y="{cy + 4}" text-anchor="middle" dominant-baseline="middle" font-family="{S.HEADER_FONT}" font-size="{font_size}" fill="{font_color}" font-weight="600">{text}</text>\n'
        else:
            text = ' '.join(gate_strs)
            font_size = 14
            svg += f'  <text x="{cx}" y="{cy + 4}" text-anchor="middle" dominant-baseline="middle" font-family="{S.HEADER_FONT}" font-size="{font_size}" fill="{font_color}" font-weight="600">{text}</text>\n'
    
    return svg


def _darken(hex_color, amount=0.3):
    """Darken a hex color by amount (0-1)."""
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = int(r * (1 - amount))
    g = int(g * (1 - amount))
    b = int(b * (1 - amount))
    return f'#{r:02x}{g:02x}{b:02x}'


def _gate_marker_svg(gate, gate_type, gx, gy, angle):
    """Generate SVG for a gate marker circle + number."""
    r = S.GATE_CIRCLE_RADIUS

    if gate_type == 'both':
        fill = S.GATE_BOTH_COLOR
    elif gate_type == 'personality':
        fill = S.GATE_PERSONALITY_COLOR
    else:
        fill = S.GATE_DESIGN_COLOR

    # Text offset - push label outward from center
    text_offset = r + 8
    tx = gx + text_offset * math.cos(angle)
    ty = gy + text_offset * math.sin(angle)

    # Anchor based on angle
    if abs(math.cos(angle)) < 0.3:
        anchor = 'middle'
    elif math.cos(angle) > 0:
        anchor = 'start'
    else:
        anchor = 'end'

    svg = f'  <circle cx="{gx:.1f}" cy="{gy:.1f}" r="{r}" fill="{fill}" stroke="#ffffff" stroke-width="1" stroke-opacity="0.3"/>\n'
    svg += f'  <text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}" dominant-baseline="middle" font-family="{S.HEADER_FONT}" font-size="{S.GATE_FONT_SIZE}" fill="{S.GATE_NUMBER_COLOR}" font-weight="700">{gate}</text>\n'
    return svg


def _channel_svg(g1, g2, channel_type):
    """Generate SVG for a channel line between two gates."""
    if g1 not in GATE_TO_POSITION or g2 not in GATE_TO_POSITION:
        return ''

    _, x1, y1, _ = GATE_TO_POSITION[g1]
    _, x2, y2, _ = GATE_TO_POSITION[g2]

    if channel_type == 'personality':
        color = S.CHANNEL_PERSONALITY_COLOR
    elif channel_type == 'design':
        color = S.CHANNEL_DESIGN_COLOR
    else:
        color = S.CHANNEL_BOTH_COLOR

    svg = f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{S.CHANNEL_WIDTH}" stroke-linecap="round"'

    if channel_type == 'both':
        svg += f' stroke-dasharray="8,4"'

    svg += '/>\n'

    return svg


def _header_svg(chart):
    """Generate SVG for the header section."""
    hd_type = chart.get('type', 'Generator')
    profile = chart.get('profile', '')
    authority = _get_authority(chart)
    strategy = _get_strategy(chart)
    type_color = S.TYPE_COLORS.get(hd_type, '#ffffff')
    
    svg = ''
    y = 30
    
    # Type
    svg += f'  <text x="{S.CANVAS_WIDTH // 2}" y="{y}" text-anchor="middle" font-family="{S.HEADER_FONT}" font-size="28" fill="{type_color}" font-weight="700" letter-spacing="2">{hd_type.upper()}</text>\n'
    
    # Divider line
    y += 15
    svg += f'  <line x1="250" y1="{y}" x2="550" y2="{y}" stroke="{type_color}" stroke-width="1" opacity="0.4"/>\n'
    
    # Profile | Authority | Strategy
    y += 25
    svg += f'  <text x="{S.CANVAS_WIDTH // 2}" y="{y}" text-anchor="middle" font-family="{S.HEADER_FONT}" font-size="14" fill="{S.HEADER_COLOR}" font-weight="400">Profile {profile}  ·  {authority}  ·  {strategy}</text>\n'
    
    return svg


def _footer_svg(chart):
    """Generate SVG for the footer section."""
    svg = ''
    y = S.CANVAS_HEIGHT - 40
    
    # Decorative line
    svg += f'  <line x1="100" y1="{y - 15}" x2="700" y2="{y - 15}" stroke="#ffffff" stroke-width="0.5" opacity="0.15"/>\n'
    
    birth_info = chart.get('birth_info', {})
    if birth_info:
        date_str = birth_info.get('date', '')
        time_str = birth_info.get('time', '')
        place_str = birth_info.get('place', '')
        info_text = f"{date_str}  {time_str}  ·  {place_str}".strip(' ·')
        if info_text:
            svg += f'  <text x="{S.CANVAS_WIDTH // 2}" y="{y}" text-anchor="middle" font-family="{S.HEADER_FONT}" font-size="11" fill="{S.SUBHEADER_COLOR}" font-weight="300">{info_text}</text>\n'
    
    # Branding
    svg += f'  <text x="{S.CANVAS_WIDTH // 2}" y="{y + 18}" text-anchor="middle" font-family="{S.HEADER_FONT}" font-size="9" fill="#555566" font-weight="300">Human Design Bodygraph</text>\n'
    
    return svg


def _defs_svg():
    """SVG defs: gradients, filters, etc."""
    svg = '  <defs>\n'
    # Half-black, half-red gradient for "both" gate markers
    svg += '    <linearGradient id="gateBothGrad" x1="0" y1="0" x2="1" y2="0">\n'
    svg += f'      <stop offset="50%" stop-color="{S.GATE_PERSONALITY_COLOR}"/>\n'
    svg += f'      <stop offset="50%" stop-color="{S.GATE_DESIGN_COLOR}"/>\n'
    svg += '    </linearGradient>\n'
    svg += '    <radialGradient id="bgGrad" cx="50%" cy="40%" r="60%">\n'
    svg += '      <stop offset="0%" stop-color="#252545"/>\n'
    svg += '      <stop offset="100%" stop-color="#1a1a2e"/>\n'
    svg += '    </radialGradient>\n'
    # Subtle glow for defined centers
    svg += '    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">\n'
    svg += '      <feGaussianBlur stdDeviation="3" result="blur"/>\n'
    svg += '      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
    svg += '    </filter>\n'
    svg += '  </defs>\n'
    return svg


def _structural_lines_svg():
    """Draw the faint structural lines connecting centers (bodygraph skeleton)."""
    svg = ''
    connections = [
        ('Head', 'Ajna'),
        ('Ajna', 'Throat'),
        ('Throat', 'G'),
        ('Throat', 'Heart'),
        ('G', 'Heart'),
        ('G', 'SolarPlexus'),
        ('G', 'Spleen'),
        ('Heart', 'SolarPlexus'),
        ('SolarPlexus', 'Spleen'),
        ('SolarPlexus', 'Sacral'),
        ('SolarPlexus', 'Root'),
        ('Spleen', 'Sacral'),
        ('Spleen', 'Root'),
        ('Sacral', 'Root'),
    ]
    
    drawn = set()
    for c1, c2 in connections:
        key = tuple(sorted([c1, c2]))
        if key in drawn:
            continue
        drawn.add(key)
        p1 = S.CENTER_POSITIONS[c1]
        p2 = S.CENTER_POSITIONS[c2]
        svg += f'  <line x1="{p1["x"]}" y1="{p1["y"]}" x2="{p2["x"]}" y2="{p2["y"]}" stroke="#ffffff" stroke-width="1" opacity="0.08"/>\n'
    
    return svg


def render_bodygraph(chart, output_path=None):
    """
    Render a Human Design bodygraph SVG.
    
    Args:
        chart: ChartResult dict with keys:
            - personality: dict of {planet: (longitude, gate, line)}
            - design: dict of {planet: (longitude, gate, line)}
            - channels: list of (gate1, gate2) tuples
            - defined_centers: list of center name strings
            - type: string (e.g. 'Generator')
            - profile: string (e.g. '1/5')
            - birth_info: optional dict with date, time, place
        output_path: optional file path to save SVG
    
    Returns:
        SVG string
    """
    defined_centers = set(chart.get('defined_centers', []))
    channels = chart.get('channels', [])
    
    # Collect activated gates
    personality_gates = {v[1] for v in chart.get('personality', {}).values() if v}
    design_gates = {v[1] for v in chart.get('design', {}).values() if v}
    all_activated = personality_gates | design_gates
    
    # Map gates to their centers
    gate_to_center = {}
    for center_name, center_data in CENTERS.items():
        for g in center_data['gates']:
            gate_to_center[g] = center_name
    
    # Group activated gates by center
    center_activated_gates = {cn: set() for cn in CENTERS}
    for g in all_activated:
        if g in gate_to_center:
            center_activated_gates[gate_to_center[g]].add(g)
    
    # Start building SVG
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{S.VIEWBOX}" width="{S.CANVAS_WIDTH}" height="{S.CANVAS_HEIGHT}" style="max-width:100%;height:auto;">')
    parts.append(_defs_svg())
    
    # Background
    parts.append(f'  <rect width="{S.CANVAS_WIDTH}" height="{S.CANVAS_HEIGHT}" fill="{S.BG_COLOR}" rx="12"/>')
    
    # Subtle radial gradient overlay
    parts.append(f'  <rect width="{S.CANVAS_WIDTH}" height="{S.CANVAS_HEIGHT}" fill="url(#bgGrad)" rx="12" opacity="0.5"/>')
    # Add bg gradient to defs... let me just inline a circle
    parts.append(f'  <circle cx="{S.CANVAS_WIDTH//2}" cy="450" r="400" fill="none" stroke="#ffffff" stroke-width="0.5" opacity="0.04"/>')
    parts.append(f'  <circle cx="{S.CANVAS_WIDTH//2}" cy="450" r="300" fill="none" stroke="#ffffff" stroke-width="0.5" opacity="0.03"/>')
    
    # Header
    parts.append(_header_svg(chart))
    
    # Structural skeleton lines
    parts.append(_structural_lines_svg())
    
    # Active channels (draw before centers so they go behind)
    for g1, g2 in channels:
        ch_type = _determine_channel_type(personality_gates, design_gates, g1, g2)
        parts.append(_channel_svg(g1, g2, ch_type))
    
    # Centers
    for center_name in ['Root', 'Sacral', 'Spleen', 'SolarPlexus', 'Heart', 'G', 'Throat', 'Ajna', 'Head']:
        pos = S.CENTER_POSITIONS[center_name]
        defined = center_name in defined_centers
        act_gates = center_activated_gates.get(center_name, set())
        parts.append(_center_shape_svg(center_name, pos['x'], pos['y'], pos['rx'], pos['ry'], defined, act_gates))
    
    # Gate markers (draw on top)
    for gate in sorted(all_activated):
        if gate not in GATE_TO_POSITION:
            continue
        center, gx, gy, angle = GATE_TO_POSITION[gate]
        gate_type = _determine_gate_type(personality_gates, design_gates, gate)
        parts.append(_gate_marker_svg(gate, gate_type, gx, gy, angle))
    
    # Footer
    parts.append(_footer_svg(chart))
    
    parts.append('</svg>')
    
    svg_str = '\n'.join(parts)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_str)
    
    return svg_str
