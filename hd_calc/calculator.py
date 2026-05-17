"""Core calculation logic for Human Design charts."""
import sys
import math
import os
from collections import deque

import swisseph as swe

# Add project root to path for hd_constants import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from hd_constants import (
    WHEEL_OFFSET_DEGREES, GATE_SIZE_DEGREES, GATE_ORDER,
    PLANET_IDS, DERIVED_PLANETS, PLANET_NAMES_ORDERED,
    CENTERS, CENTER_CONNECTIONS, MOTOR_CENTERS,
    CHANNELS, GATE_TO_CHANNELS, GATE_INFO,
    TYPES, AUTHORITY_PRIORITY, LINE_INFO, INCARNATION_CROSSES,
)

from hd_calc.models import (
    CalculateRequest, ChartResult, PlanetActivation,
    ChannelActivation, CenterInfo,
)
from hd_calc.analysis import analyze_chart


def degree_to_gate_line(longitude: float) -> tuple:
    """Convert ecliptic longitude to (gate, line).

    The HD wheel starts at WHEEL_OFFSET_DEGREES (302° = 2° Aquarius).
    Each of the 64 segments is GATE_SIZE_DEGREES wide.
    Line is determined by subdividing each gate into 6 equal parts.
    """
    lon = longitude % 360.0
    # Adjust so that 0 corresponds to the wheel offset
    adjusted = (lon - WHEEL_OFFSET_DEGREES) % 360.0
    segment_float = adjusted / GATE_SIZE_DEGREES
    segment_index = int(segment_float) % 64
    gate = GATE_ORDER[segment_index]
    # Line: 6 lines per gate, each line = GATE_SIZE_DEGREES / 6
    line_fraction = segment_float - int(segment_float)
    line = min(int(line_fraction * 6) + 1, 6)
    return gate, line


def compute_planet_positions(jd_ut: float) -> dict:
    """Compute all planet longitudes for a given Julian Day (UT).

    Returns dict of planet_name -> longitude (degrees).
    """
    positions = {}
    FLG_MOSEPH_SPEED = swe.FLG_MOSEPH | swe.FLG_SPEED
    for name, pid in PLANET_IDS.items():
        result = swe.calc_ut(jd_ut, pid, FLG_MOSEPH_SPEED)
        lon = result[0][0]  # ecliptic longitude
        speed = result[0][3]  # speed in longitude
        positions[name] = {'longitude': lon % 360.0, 'speed': speed}

    # Derived planets
    for derived, source in DERIVED_PLANETS.items():
        lon = (positions[source]['longitude'] + 180.0) % 360.0
        positions[derived] = {'longitude': lon, 'speed': positions[source]['speed']}

    return positions


def find_design_date(birth_jd: float, timezone_offset: float) -> float:
    """Find the Design date via Newton-Raphson iteration.

    The Design date is when the Sun was 88° behind its birth position
    (measured along the ecliptic, going backward).

    We solve: sun_lon(design_jd) = sun_lon(birth_jd) - 88° (mod 360)
    Using Newton-Raphson on the Sun's position.

    Returns the Julian Day of the design date.
    """
    FLG_MOSEPH_SPEED = swe.FLG_MOSEPH | swe.FLG_SPEED
    birth_sun = swe.calc_ut(birth_jd, swe.SUN, FLG_MOSEPH_SPEED)
    target_lon = (birth_sun[0][0] - 88.0) % 360.0

    # Initial guess: ~89.3 days before birth (Sun moves ~0.9856°/day)
    jd = birth_jd - 88.0 / 0.9856

    for _ in range(50):
        result = swe.calc_ut(jd, swe.SUN, FLG_MOSEPH_SPEED)
        lon = result[0][0] % 360.0
        speed = result[0][3]

        # Angular distance to target
        diff = (lon - target_lon + 180.0) % 360.0 - 180.0

        if abs(diff) < 1e-8:
            break

        if abs(speed) < 1e-12:
            # Speed is zero — can't continue Newton-Raphson
            break

        jd -= diff / speed

    return jd


def build_activations(positions: dict) -> dict:
    """Convert planet positions dict to PlanetActivation dict."""
    activations = {}
    for name in PLANET_NAMES_ORDERED:
        if name not in positions:
            continue
        lon = positions[name]['longitude']
        gate, line = degree_to_gate_line(lon)
        activations[name] = PlanetActivation(longitude=lon, gate=gate, line=line)
    return activations


def calculate_chart(req: CalculateRequest) -> ChartResult:
    """Main entry point: compute a full Human Design chart."""
    # Convert birth date/time to Julian Day (UT)
    hour_decimal = req.hour + req.minute / 60.0 - req.timezone_offset
    birth_jd = swe.julday(req.year, req.month, req.day, hour_decimal)

    # Personality positions (birth moment)
    personality_positions = compute_planet_positions(birth_jd)
    personality = build_activations(personality_positions)

    # Design date and positions
    design_jd = find_design_date(birth_jd, req.timezone_offset)
    design_positions = compute_planet_positions(design_jd)
    design = build_activations(design_positions)

    # Approximate design date string
    design_date_tuple = swe.revjul(design_jd)
    design_date_str = f"{int(design_date_tuple[0]):04d}-{int(design_date_tuple[1]):02d}-{int(design_date_tuple[2]):02d}"

    # Run analysis
    result = analyze_chart(personality, design, personality_positions, design_positions)
    result.request = req
    result.personality = personality
    result.design = design
    result.design_date_approx = design_date_str

    return result
