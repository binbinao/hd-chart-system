"""Chart analysis: determine channels, centers, type, authority, profile, definition."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from hd_constants import (
    CENTERS, CHANNELS, GATE_TO_CHANNELS, GATE_INFO,
    TYPES, AUTHORITY_PRIORITY, LINE_INFO,
    INCARNATION_CROSSES, CROSS_NAMES, CROSS_NAME_OVERRIDES,
    PROFILE_TO_ANGLE, ANGLE_NAMES,
    MOTOR_CENTERS,
)
from hd_calc.models import ChartResult, ChannelActivation, CenterInfo


def _get_all_gates(personality, design):
    """Get sets of gates activated in personality and design."""
    p_gates = {a.gate for a in personality.values()}
    d_gates = {a.gate for a in design.values()}
    return p_gates, d_gates


def _find_channels(p_gates, d_gates):
    """Find activated channels. A channel is active when BOTH gates are present
    (either from personality or design)."""
    all_gates = p_gates | d_gates
    channels = []
    for (g1, g2), info in sorted(CHANNELS.items()):
        if g1 in all_gates and g2 in all_gates:
            p_side = [g for g in (g1, g2) if g in p_gates]
            d_side = [g for g in (g1, g2) if g in d_gates]
            channels.append(ChannelActivation(
                gate1=g1, gate2=g2,
                name_zh=info['zh'], name_en=info['en'],
                personality_gates=p_side,
                design_gates=d_side,
            ))
    return channels


def _determine_centers(all_gates, channels):
    """Determine which centers are defined.
    A center is defined if it has an activated gate AND is connected
    through a complete channel, OR if it has a complete channel through it."""
    # Centers with any activated gate
    centers_with_gates = {}
    for center_name, center_data in CENTERS.items():
        activated = [g for g in center_data['gates'] if g in all_gates]
        centers_with_gates[center_name] = activated

    # A center is defined if it participates in at least one complete channel
    # OR if it's the Sacral (always considered for type determination)
    defined_via_channel = set()
    for ch in channels:
        c1, c2 = CHANNELS[(ch.gate1, ch.gate2)]['centers']
        defined_via_channel.add(c1)
        defined_via_channel.add(c2)

    # Build center info
    centers = {}
    for center_name, center_data in CENTERS.items():
        is_defined = center_name in defined_via_channel
        centers[center_name] = CenterInfo(
            name=center_name,
            name_zh=center_data['zh'],
            name_en=center_data['en'],
            is_defined=is_defined,
            activated_gates=centers_with_gates[center_name],
        )
    return centers


def _build_channel_graph(channels):
    """Build an adjacency graph of centers connected by activated channels.

    Returns a dict: center_name -> set of directly connected center_names
    (only through activated channels, not all possible bodygraph connections).
    """
    graph = {}
    for ch in channels:
        c1, c2 = CHANNELS[(ch.gate1, ch.gate2)]['centers']
        graph.setdefault(c1, set()).add(c2)
        graph.setdefault(c2, set()).add(c1)
    return graph


def _motor_reaches_throat(channels):
    """Check if any motor center can reach the Throat via activated channels.

    Uses BFS on the graph of centers connected by activated channels.
    This correctly handles indirect connections like Sacral → Spleen → Throat.
    """
    channel_graph = _build_channel_graph(channels)

    # If Throat is not in the graph at all, no motor can reach it
    if 'Throat' not in channel_graph:
        return False

    for motor in MOTOR_CENTERS:
        if motor not in channel_graph:
            continue
        # BFS from this motor center to see if it can reach Throat
        visited = set()
        queue = [motor]
        while queue:
            current = queue.pop(0)
            if current == 'Throat':
                return True
            if current in visited:
                continue
            visited.add(current)
            for neighbor in channel_graph.get(current, set()):
                if neighbor not in visited:
                    queue.append(neighbor)
    return False


def _determine_type(centers, channels):
    """Determine the Type based on defined centers and channel connectivity.

    Uses BFS to check if any motor center can reach the Throat
    through a chain of activated channels (not just direct connection).
    """
    defined = {name for name, c in centers.items() if c.is_defined}
    sacral_defined = centers.get('Sacral', CenterInfo('Sacral','','',False)).is_defined

    motor_to_throat = _motor_reaches_throat(channels)

    if not defined:
        return 'Reflector'
    elif sacral_defined and motor_to_throat:
        return 'ManifestingGenerator'
    elif sacral_defined:
        return 'Generator'
    elif motor_to_throat:
        return 'Manifestor'
    else:
        return 'Projector'


def _determine_authority(centers):
    """Determine authority based on defined centers."""
    defined = {name for name, c in centers.items() if c.is_defined}
    for center_key, auth_info in AUTHORITY_PRIORITY:
        if center_key is None:
            return auth_info
        if center_key in defined:
            return auth_info
    return AUTHORITY_PRIORITY[-1][1]


def _determine_profile(personality, design):
    """Determine profile from Sun's lines."""
    p_sun_line = personality.get('Sun', PlanetActivation(0,0,1)).line
    d_sun_line = design.get('Sun', PlanetActivation(0,0,1)).line
    return f"{p_sun_line}/{d_sun_line}", p_sun_line, d_sun_line


def _determine_definition_type(centers, channels):
    """Determine definition type (single, split, triple, quadruple, none).

    Uses the graph of centers connected by activated channels (not all
    possible bodygraph connections) to find connected components.
    """
    defined = {name for name, c in centers.items() if c.is_defined}
    if not defined:
        return 'none'

    # Build adjacency only from activated channels
    channel_graph = _build_channel_graph(channels)

    # Find connected components among defined centers
    visited = set()
    components = 0
    for center in defined:
        if center not in visited:
            components += 1
            queue = [center]
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                # Only traverse through activated channel connections
                for neighbor in channel_graph.get(current, set()):
                    if neighbor in defined and neighbor not in visited:
                        queue.append(neighbor)

    mapping = {1: 'single', 2: 'split', 3: 'triple_split', 4: 'quadruple_split'}
    return mapping.get(components, 'quadruple_split')


def _determine_incarnation_cross(personality, design, profile_str):
    """Determine incarnation cross from Sun/Earth gates and profile.

    Uses the new gate+profile lookup (192 crosses = 64 gates × 3 angles).
    Falls back to legacy INCARNATION_CROSSES dict, then to a generic name.
    """
    p_sun = personality.get('Sun', PlanetActivation(0, 1, 1)).gate
    p_earth = personality.get('Earth', PlanetActivation(0, 2, 1)).gate
    d_sun = design.get('Sun', PlanetActivation(0, 3, 1)).gate
    d_earth = design.get('Earth', PlanetActivation(0, 4, 1)).gate
    cross_gates = [p_sun, p_earth, d_sun, d_earth]

    # --- New lookup: gate + profile → angle → cross name ---
    angle = PROFILE_TO_ANGLE.get(profile_str, 'right')
    base_name = CROSS_NAMES.get(p_sun)

    if base_name:
        # Check if this gate has an angle-specific override
        overrides = CROSS_NAME_OVERRIDES.get(p_sun, {})
        name_info = overrides.get(angle, base_name)

        # Build full name with angle prefix
        prefix = ANGLE_NAMES[angle]
        cross_zh = prefix['zh'] + name_info['zh']
        cross_en = prefix['en'] + name_info['en']
        return cross_zh, cross_en, cross_gates

    # --- Legacy fallback: exact 4-gate tuple lookup ---
    cross_key = tuple(cross_gates)
    cross_info = INCARNATION_CROSSES.get(cross_key)
    if not cross_info:
        cross_info = INCARNATION_CROSSES.get(tuple(sorted(cross_gates)))

    if cross_info:
        return cross_info['zh'], cross_info['en'], cross_gates

    # --- Final fallback: generate generic name ---
    return f"交叉之{GATE_INFO[p_sun]['zh']}/{GATE_INFO[d_sun]['zh']}", \
           f"Cross of {GATE_INFO[p_sun]['en']}/{GATE_INFO[d_sun]['en']}", \
           cross_gates


from hd_calc.models import PlanetActivation  # noqa: E402


def analyze_chart(personality, design, personality_positions, design_positions):
    """Analyze a chart and return a ChartResult (minus request/personality/design/date)."""
    p_gates, d_gates = _get_all_gates(personality, design)
    all_gates = p_gates | d_gates

    channels = _find_channels(p_gates, d_gates)
    centers = _determine_centers(all_gates, channels)
    type_key = _determine_type(centers, channels)
    type_info = TYPES[type_key]
    authority = _determine_authority(centers)
    profile_str, p_line, d_line = _determine_profile(personality, design)
    definition_type = _determine_definition_type(centers, channels)
    cross_zh, cross_en, cross_gates = _determine_incarnation_cross(personality, design, profile_str)

    return ChartResult(
        request=None,
        personality=None,
        design=None,
        design_date_approx='',
        channels=channels,
        centers=centers,
        type_key=type_key,
        type_zh=type_info['zh'],
        type_en=type_info['en'],
        authority_zh=authority['zh'],
        authority_en=authority['en'],
        profile=profile_str,
        profile_conscious_line=p_line,
        profile_design_line=d_line,
        definition_type=definition_type,
        incarnation_cross_zh=cross_zh,
        incarnation_cross_en=cross_en,
        incarnation_cross_gates=cross_gates,
    )
