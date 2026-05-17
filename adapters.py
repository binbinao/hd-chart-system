"""
Adapters to convert between hd_calc dataclasses and hd_render dict format.
"""

def chart_to_render_dict(chart_result):
    """Convert ChartResult dataclass to the dict format expected by hd_render."""
    # Personality/Design: planet -> (longitude, gate, line)
    personality = {}
    for planet, act in chart_result.personality.items():
        personality[planet] = (act.longitude, act.gate, act.line)
    
    design = {}
    for planet, act in chart_result.design.items():
        design[planet] = (act.longitude, act.gate, act.line)
    
    # Channels: list of (gate1, gate2) tuples
    channels = [(c.gate1, c.gate2) for c in chart_result.channels]
    
    # Defined centers
    defined_centers = [name for name, c in chart_result.centers.items() if c.is_defined]
    
    # Build the dict
    render_dict = {
        'personality': personality,
        'design': design,
        'channels': channels,
        'defined_centers': defined_centers,
        'type': chart_result.type_en or chart_result.type_zh,
        'profile': chart_result.profile,
        'authority': chart_result.authority_zh,
        'birth_info': {
            'date': f"{chart_result.request.year}-{chart_result.request.month:02d}-{chart_result.request.day:02d}",
            'time': f"{chart_result.request.hour:02d}:{chart_result.request.minute:02d}",
            'tz': f"UTC{'+' if chart_result.request.timezone_offset >= 0 else ''}{chart_result.request.timezone_offset}",
            'lat': chart_result.request.lat,
            'lng': chart_result.request.lng,
        }
    }
    
    return render_dict
