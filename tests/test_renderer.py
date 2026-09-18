"""Tests for hd_render.renderer + styles.

Covers Scope A of the renderer rewrite: contrast/legibility, per-endpoint
channel-color logic, the Manifesting Generator type-key fix, and SVG a11y.
Scope B (canonical gate geometry) is blocked on a reference layout and lands
separately.
"""
import re
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def _hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _luminance(hex_color):
    r, g, b = (c / 255 for c in _hex_to_rgb(hex_color))

    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def _contrast(c1, c2):
    """WCAG 2.x contrast ratio between two hex colors."""
    l1, l2 = _luminance(c1), _luminance(c2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def _minimal_chart(**over):
    base = {
        'personality': {}, 'design': {}, 'channels': [],
        'defined_centers': [], 'type': 'Manifesting Generator',
        'type_key': 'ManifestingGenerator', 'profile': '1/3',
        'birth_info': {},
    }
    base.update(over)
    return base


class TestBodygraphContrast:
    """The bodygraph background must be light enough that black personality
    channels (>=3:1 for graphical objects) and header/gate-number text
    (>=4.5:1) are legible. The previous dark theme gave ~1.02:1.
    """

    def _svg(self):
        from hd_render.renderer import render_bodygraph
        return render_bodygraph(_minimal_chart())

    def _bg_fill(self, svg):
        m = re.search(r'<rect[^>]*fill="(#[0-9a-fA-F]{3,6})"', svg)
        assert m, "no solid background rect found"
        return m.group(1)

    def test_personality_channels_readable_on_bg(self):
        from hd_render.styles import CHANNEL_PERSONALITY_COLOR
        bg = self._bg_fill(self._svg())
        assert _contrast(bg, CHANNEL_PERSONALITY_COLOR) >= 3.0

    def test_header_text_readable_on_bg(self):
        from hd_render.styles import HEADER_COLOR
        bg = self._bg_fill(self._svg())
        assert _contrast(bg, HEADER_COLOR) >= 4.5

    def test_gate_numbers_readable_on_bg(self):
        from hd_render.styles import GATE_NUMBER_COLOR
        bg = self._bg_fill(self._svg())
        assert _contrast(bg, GATE_NUMBER_COLOR) >= 4.5


class TestChannelEndpointColors:
    """_channel_endpoint_colors returns a per-gate color so each half of a
    channel can be drawn by its own activation (black/red), instead of OR-ing
    both gates into a single 'both' bucket.
    """

    def test_personality_at_g1_design_at_g2(self):
        from hd_render.renderer import _channel_endpoint_colors
        c1, c2 = _channel_endpoint_colors({34}, {57}, 34, 57)
        assert c1 == 'personality'
        assert c2 == 'design'

    def test_both_sides_at_one_gate(self):
        from hd_render.renderer import _channel_endpoint_colors
        c1, c2 = _channel_endpoint_colors({34, 57}, {34, 57}, 34, 57)
        assert c1 == 'both'
        assert c2 == 'both'

    def test_neither_activated_is_none(self):
        from hd_render.renderer import _channel_endpoint_colors
        c1, c2 = _channel_endpoint_colors(set(), set(), 34, 57)
        assert c1 is None
        assert c2 is None


class TestManifestingGeneratorHeader:
    """MG must render its own type color + strategy, not fall back to Generator.
    Adapter passes type_key='ManifestingGenerator' (no space); the renderer
    previously keyed lookups on the display name 'Manifesting Generator' (space)
    and missed every TYPE_COLORS / TYPES entry.
    """

    def test_uses_mg_type_color(self):
        from hd_render.renderer import render_bodygraph
        from hd_render.styles import TYPE_COLORS
        svg = render_bodygraph(_minimal_chart())
        assert TYPE_COLORS['ManifestingGenerator'].lower() in svg.lower()

    def test_uses_mg_strategy_text(self):
        from hd_render.renderer import render_bodygraph
        svg = render_bodygraph(_minimal_chart())
        assert 'INFORM' in svg.upper()  # MG strategy: "Wait to Respond, then Inform"


class TestBodygraphA11y:
    """The inline SVG must expose itself to AT as a labeled image."""

    def test_has_role_img(self):
        from hd_render.renderer import render_bodygraph
        assert 'role="img"' in render_bodygraph(_minimal_chart())

    def test_has_title(self):
        from hd_render.renderer import render_bodygraph
        assert '<title' in render_bodygraph(_minimal_chart())

    def test_has_desc(self):
        from hd_render.renderer import render_bodygraph
        assert '<desc' in render_bodygraph(_minimal_chart())
