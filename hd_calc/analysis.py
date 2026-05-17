"""Chart analysis: determine channels, centers, type, authority, profile, definition."""
import sys
sys.path.insert(0, '/root/.openclaw/workspace/hd-chart-system')

from hd_constants import (
    CENTERS, CHANNELS, GATE_TO_CHANNELS, GATE_INFO,
    TYPES, AUTHORITY_PRIORITY, LINE_INFO, INCARNATION_CROSSES,
    MOTOR_CENTERS, CENTER_CONNECTIONS,
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


def _determine_type(centers, channels):
    """Determine the Type based on defined centers."""
    defined = {name for name, c in centers.items() if c.is_defined}
    sacral_defined = centers.get('Sacral', CenterInfo('Sacral','','',False)).is_defined
    throat_defined = centers.get('Throat', CenterInfo('Throat','','',False)).is_defined

    # Check if any motor center connects to throat via a channel
    motor_to_throat = False
    for ch in channels:
        c1, c2 = CHANNELS[(ch.gate1, ch.gate2)]['centers']
        if (c1 == 'Throat' and c2 in MOTOR_CENTERS) or \
           (c2 == 'Throat' and c1 in MOTOR_CENTERS):
            motor_to_throat = True
            break

    if not defined:
        return 'Reflector'
    elif sacral_defined and motor_to_throat:
        # Manifesting Generator check: if sacral defined + motor to throat
        # AND there's also a direct connection from a motor to throat that isn't
        # just the sacral (or if there's a manifesting channel pattern)
        # Simplified: MG if sacral + motor-to-throat
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


def _determine_definition_type(centers):
    """Determine definition type (single, split, triple, quadruple, none)."""
    defined = {name for name, c in centers.items() if c.is_defined}
    if not defined:
        return 'none'

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
                for neighbor in CENTER_CONNECTIONS.get(current, []):
                    if neighbor in defined and neighbor not in visited:
                        queue.append(neighbor)

    mapping = {1: 'single', 2: 'split', 3: 'triple_split', 4: 'quadruple_split'}
    return mapping.get(components, 'quadruple_split')


def _determine_incarnation_cross(personality, design):
    """Determine incarnation cross from Sun/Earth gates."""
    p_sun = personality.get('Sun', PlanetActivation(0,1,1)).gate
    p_earth = personality.get('Earth', PlanetActivation(0,2,1)).gate
    d_sun = design.get('Sun', PlanetActivation(0,3,1)).gate
    d_earth = design.get('Earth', PlanetActivation(0,4,1)).gate
    cross_gates = [p_sun, p_earth, d_sun, d_earth]

    cross_key = tuple(sorted(cross_gates))
    cross_info = INCARNATION_CROSSES.get(cross_key)

    if cross_info:
        return cross_info['zh'], cross_info['en'], cross_gates

    # Generate a generic cross name
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
    definition_type = _determine_definition_type(centers)
    cross_zh, cross_en, cross_gates = _determine_incarnation_cross(personality, design)

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
