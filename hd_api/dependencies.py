"""Dependency injection for the HD API."""
import sys
sys.path.insert(0, '/root/.openclaw/workspace/hd-chart-system')

from hd_calc import calculate_chart
from hd_calc.models import CalculateRequest
from hd_interp import generate_reading
from hd_interp.formatter import format_reading_markdown, format_reading_json, format_reading_plain
from hd_constants import GATE_INFO, CHANNELS, TYPES


def do_calculate(year, month, day, hour, minute, tz_offset, lat, lng):
    """Calculate a chart from birth data."""
    req = CalculateRequest(
        year=year, month=month, day=day,
        hour=hour, minute=minute,
        timezone_offset=tz_offset,
        lat=lat, lng=lng,
    )
    return calculate_chart(req)


def do_reading(chart_result):
    """Generate a reading from a chart result."""
    return generate_reading(chart_result)


def get_gate_info(gate_number: int) -> dict:
    """Get info for a specific gate."""
    info = GATE_INFO.get(gate_number)
    if not info:
        return None
    return {
        'gate': gate_number,
        'name_zh': info['zh'],
        'name_en': info['en'],
        'i_ching': info['i_ching'],
    }


def get_channel_info(g1: int, g2: int) -> dict:
    """Get info for a specific channel."""
    info = CHANNELS.get((g1, g2)) or CHANNELS.get((g2, g1))
    if not info:
        return None
    return {
        'gates': [g1, g2],
        'name_zh': info['zh'],
        'name_en': info['en'],
        'centers': list(info['centers']),
    }


def get_type_info(type_key: str) -> dict:
    """Get info for a specific type."""
    info = TYPES.get(type_key)
    if not info:
        return None
    return info
