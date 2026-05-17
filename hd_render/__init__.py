"""
Human Design Bodygraph SVG Renderer

Generates beautiful, professional Human Design bodygraph SVGs.
"""

import sys
import os

# Add parent directory to path for hd_constants import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from hd_render.renderer import render_bodygraph

__all__ = ['render_bodygraph']
