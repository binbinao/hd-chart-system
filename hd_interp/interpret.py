"""Main interpretation logic - generates structured readings from ChartResult."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from hd_interp.readings.type_readings import TYPE_READINGS
from hd_interp.readings.channel_readings import CHANNEL_READINGS
from hd_interp.readings.center_readings import CENTER_READINGS
from hd_interp.readings.gate_readings import GATE_READINGS
from hd_interp.readings.profile_readings import PROFILE_READINGS
from hd_constants import GATE_INFO, CHANNELS, TYPES


def generate_reading(chart_result) -> dict:
    """Generate a complete Chinese interpretation from a ChartResult.

    Returns a structured dict with all reading sections.
    """
    reading = {}

    # 1. Type reading
    type_key = chart_result.type_key
    type_reading = TYPE_READINGS.get(type_key, {})
    reading['type'] = {
        'key': type_key,
        'name_zh': chart_result.type_zh,
        'name_en': chart_result.type_en,
        'strategy_zh': TYPES.get(type_key, {}).get('strategy_zh', ''),
        'strategy_en': TYPES.get(type_key, {}).get('strategy_en', ''),
        'signature_zh': TYPES.get(type_key, {}).get('signature_zh', ''),
        'signature_en': TYPES.get(type_key, {}).get('signature_en', ''),
        'notself_zh': TYPES.get(type_key, {}).get('notself_zh', ''),
        'notself_en': TYPES.get(type_key, {}).get('notself_en', ''),
        'title': type_reading.get('title', ''),
        'body': type_reading.get('body', ''),
    }

    # 2. Authority reading
    reading['authority'] = {
        'name_zh': chart_result.authority_zh,
        'name_en': chart_result.authority_en,
    }

    # 3. Profile reading
    profile_key = chart_result.profile
    profile_reading = PROFILE_READINGS.get(profile_key, {})
    reading['profile'] = {
        'key': profile_key,
        'title': profile_reading.get('title', ''),
        'body': profile_reading.get('body', ''),
    }

    # 4. Channels reading
    reading['channels'] = []
    for ch in chart_result.channels:
        ch_key = (ch.gate1, ch.gate2)
        # Try both orderings
        ch_reading = CHANNEL_READINGS.get(ch_key) or CHANNEL_READINGS.get((ch.gate2, ch.gate1), {})
        reading['channels'].append({
            'gates': [ch.gate1, ch.gate2],
            'name': ch_reading.get('name', f'{ch.name_zh} ({ch.name_en})'),
            'centers': ch_reading.get('centers', ''),
            'body': ch_reading.get('body', ''),
        })

    # 5. Centers reading
    reading['centers'] = {}
    for center_name, center_info in chart_result.centers.items():
        center_reading = CENTER_READINGS.get(center_name, {})
        state = 'defined' if center_info.is_defined else 'undefined'
        state_reading = center_reading.get(state, {})
        reading['centers'][center_name] = {
            'name_zh': center_info.name_zh,
            'name_en': center_info.name_en,
            'is_defined': center_info.is_defined,
            'state': state,
            'activated_gates': center_info.activated_gates,
            'title': state_reading.get('title', ''),
            'body': state_reading.get('body', ''),
        }

    # 6. Gates reading - from personality and design
    reading['gates'] = {'personality': {}, 'design': {}}
    for planet_name, activation in chart_result.personality.items():
        gate_reading = GATE_READINGS.get(activation.gate, {})
        reading['gates']['personality'][planet_name] = {
            'gate': activation.gate,
            'line': activation.line,
            'gate_name': gate_reading.get('name', GATE_INFO.get(activation.gate, {}).get('zh', '')),
            'i_ching': gate_reading.get('i_ching', GATE_INFO.get(activation.gate, {}).get('i_ching', '')),
            'theme': gate_reading.get('theme', ''),
            'conscious': gate_reading.get('conscious', ''),
            'unconscious': gate_reading.get('unconscious', ''),
        }
    for planet_name, activation in chart_result.design.items():
        gate_reading = GATE_READINGS.get(activation.gate, {})
        reading['gates']['design'][planet_name] = {
            'gate': activation.gate,
            'line': activation.line,
            'gate_name': gate_reading.get('name', GATE_INFO.get(activation.gate, {}).get('zh', '')),
            'i_ching': gate_reading.get('i_ching', GATE_INFO.get(activation.gate, {}).get('i_ching', '')),
            'theme': gate_reading.get('theme', ''),
            'conscious': gate_reading.get('conscious', ''),
            'unconscious': gate_reading.get('unconscious', ''),
        }

    # 7. Definition type
    reading['definition_type'] = chart_result.definition_type

    # 8. Incarnation cross
    reading['incarnation_cross'] = {
        'name_zh': chart_result.incarnation_cross_zh or '',
        'name_en': chart_result.incarnation_cross_en or '',
        'gates': chart_result.incarnation_cross_gates,
    }

    # 9. Design date
    reading['design_date'] = chart_result.design_date_approx

    return reading
