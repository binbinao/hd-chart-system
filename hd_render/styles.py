"""
Human Design Bodygraph - Style Constants & Color Definitions
"""

# ============================================================
# Canvas
# ============================================================
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 1100
VIEWBOX = f"0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}"
BG_COLOR = "#1a1a2e"

# ============================================================
# Center Colors (Traditional HD colors)
# ============================================================
CENTER_COLORS = {
    'Head':        '#F5D442',   # Yellow
    'Ajna':        '#6EC5A8',   # Green
    'Throat':      '#B8926A',   # Brown/tan
    'G':           '#F5D442',   # Yellow
    'Heart':       '#D94F4F',   # Red
    'SolarPlexus': '#E8943A',   # Orange
    'Spleen':      '#B8926A',   # Brown/tan
    'Sacral':      '#D94F4F',   # Red
    'Root':        '#B8926A',   # Brown/tan
}

# Undefined center border color (same as fill but darker)
CENTER_BORDER_COLORS = {
    'Head':        '#C4A820',
    'Ajna':        '#4A9A7E',
    'Throat':      '#8A6840',
    'G':           '#C4A820',
    'Heart':       '#A03030',
    'SolarPlexus': '#B86E20',
    'Spleen':      '#8A6840',
    'Sacral':      '#A03030',
    'Root':        '#8A6840',
}

UNDEFINED_FILL = '#2a2a4a'
UNDEFINED_BORDER_WIDTH = 2.5

# ============================================================
# Center Positions & Sizes
# ============================================================
CENTER_POSITIONS = {
    'Head':        {'x': 400, 'y': 95,  'rx': 55, 'ry': 48},
    'Ajna':        {'x': 400, 'y': 195, 'rx': 55, 'ry': 48},
    'Throat':      {'x': 400, 'y': 305, 'rx': 50, 'ry': 42},
    'G':           {'x': 295, 'y': 415, 'rx': 52, 'ry': 52},
    'Heart':       {'x': 530, 'y': 415, 'rx': 42, 'ry': 42},
    'SolarPlexus': {'x': 400, 'y': 540, 'rx': 55, 'ry': 48},
    'Spleen':      {'x': 275, 'y': 660, 'rx': 45, 'ry': 45},
    'Sacral':      {'x': 530, 'y': 660, 'rx': 48, 'ry': 48},
    'Root':        {'x': 400, 'y': 800, 'rx': 52, 'ry': 42},
}

# Center shapes
CENTER_SHAPES = {
    'Head':        'triangle_up',     # △
    'Ajna':        'triangle_down',   # ▽
    'G':           'diamond',         # ◇
    'Heart':       'square',          # □
    'Throat':      'square_small',    # smaller square
    'SolarPlexus': 'triangle_down',   # ▽
    'Spleen':      'triangle_up',     # △
    'Sacral':      'square',          # □
    'Root':        'triangle_down',   # ▽
}

# ============================================================
# Gate Colors
# ============================================================
GATE_PERSONALITY_COLOR = '#1a1a1a'   # Black
GATE_DESIGN_COLOR = '#E84040'        # Red
GATE_BOTH_COLOR = 'url(#gateBothGrad)'  # Half-black, half-red

GATE_CIRCLE_RADIUS = 7
GATE_FONT_SIZE = 9

# ============================================================
# Channel Colors
# ============================================================
CHANNEL_PERSONALITY_COLOR = '#1a1a1a'  # Black
CHANNEL_DESIGN_COLOR = '#E84040'       # Red
CHANNEL_BOTH_COLOR = '#884422'         # Brown (mixed)
CHANNEL_WIDTH = 3.5

# ============================================================
# Text Styles
# ============================================================
HEADER_FONT = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
HEADER_COLOR = '#e0e0e0'
SUBHEADER_COLOR = '#a0a0b0'
GATE_NUMBER_COLOR = '#ffffff'
CENTER_GATE_COLOR = '#1a1a1a'

# ============================================================
# Type Colors (for header accent)
# ============================================================
TYPE_COLORS = {
    'Generator':            '#D94F4F',
    'ManifestingGenerator': '#E8943A',
    'Manifestor':           '#B8926A',
    'Projector':            '#6EC5A8',
    'Reflector':            '#F5D442',
}
