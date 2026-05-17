"""Format readings as Markdown, JSON, or plain text."""
import json


def format_reading_markdown(reading: dict) -> str:
    """Format a reading dict as a Markdown string."""
    parts = []

    # Header
    type_info = reading.get('type', {})
    parts.append(f"# {type_info.get('name_zh', '')} ({type_info.get('name_en', '')})")
    parts.append('')
    parts.append(f"**策略 (Strategy):** {type_info.get('strategy_zh', '')} ({type_info.get('strategy_en', '')})")
    parts.append(f"**签名 (Signature):** {type_info.get('signature_zh', '')} ({type_info.get('signature_en', '')})")
    parts.append(f"**非自我 (Not-Self):** {type_info.get('notself_zh', '')} ({type_info.get('notself_en', '')})")
    parts.append('')

    # Authority
    auth = reading.get('authority', {})
    parts.append(f"## 内在权威 (Authority)")
    parts.append(f"{auth.get('name_zh', '')} ({auth.get('name_en', '')})")
    parts.append('')

    # Profile
    profile = reading.get('profile', {})
    if profile.get('title'):
        parts.append(f"## 人生档案: {profile.get('title', '')}")
        parts.append(profile.get('body', ''))
        parts.append('')

    # Type body
    if type_info.get('body'):
        parts.append(f"## 类型详解")
        parts.append(type_info['body'])
        parts.append('')

    # Channels
    channels = reading.get('channels', [])
    if channels:
        parts.append(f"## 活化通道 ({len(channels)})")
        for ch in channels:
            parts.append(f"### {ch.get('name', '')}")
            if ch.get('centers'):
                parts.append(f"**连接中心:** {ch['centers']}")
            parts.append(ch.get('body', ''))
            parts.append('')

    # Centers
    centers = reading.get('centers', {})
    if centers:
        parts.append("## 能量中心")
        for name, c in centers.items():
            parts.append(f"### {c.get('title', c.get('name_zh', ''))}")
            if c.get('body'):
                parts.append(c['body'])
            if c.get('activated_gates'):
                parts.append(f"**活化闸门:** {', '.join(str(g) for g in c['activated_gates'])}")
            parts.append('')

    # Key gates
    parts.append("## 关键闸门")
    for side_label, side_key in [("意识 (Personality)", "personality"), ("潜意识 (Design)", "design")]:
        parts.append(f"### {side_label}")
        gates = reading.get('gates', {}).get(side_key, {})
        for planet, g in gates.items():
            parts.append(f"- **{planet}** → {g.get('gate', '')}号闸门 {g.get('gate_name', '')} ({g.get('i_ching', '')}) 第{g.get('line', '')}线")
        parts.append('')

    # Incarnation cross
    cross = reading.get('incarnation_cross', {})
    if cross.get('name_zh'):
        parts.append(f"## 人生交叉 (Incarnation Cross)")
        parts.append(f"{cross['name_zh']} ({cross.get('name_en', '')})")
        parts.append('')

    # Definition
    def_type = reading.get('definition_type', '')
    if def_type:
        parts.append(f"**定义类型:** {def_type}")
        parts.append('')

    return '\n'.join(parts)


def format_reading_json(reading: dict) -> dict:
    """Return the reading dict as-is (already structured for JSON)."""
    return reading


def format_reading_plain(reading: dict) -> str:
    """Format a reading as plain text (for WeChat/card output)."""
    lines = []
    type_info = reading.get('type', {})
    lines.append(f"【{type_info.get('name_zh', '')} {type_info.get('name_en', '')}】")
    lines.append(f"策略: {type_info.get('strategy_zh', '')}")
    lines.append(f"签名: {type_info.get('signature_zh', '')}")
    lines.append('')

    auth = reading.get('authority', {})
    lines.append(f"内在权威: {auth.get('name_zh', '')}")
    lines.append('')

    profile = reading.get('profile', {})
    if profile.get('title'):
        lines.append(f"【人生档案: {profile['title']}】")
        # Truncate body for plain text
        body = profile.get('body', '')
        if len(body) > 300:
            body = body[:300] + '...'
        lines.append(body)
        lines.append('')

    # Type summary
    if type_info.get('body'):
        body = type_info['body']
        if len(body) > 300:
            body = body[:300] + '...'
        lines.append('【类型简述】')
        lines.append(body)
        lines.append('')

    # Channels
    channels = reading.get('channels', [])
    if channels:
        lines.append(f'【活化通道 x{len(channels)}】')
        for ch in channels:
            lines.append(f"  · {ch.get('name', '')}")
        lines.append('')

    # Centers summary
    centers = reading.get('centers', {})
    defined = [c.get('name_zh', '') for c in centers.values() if c.get('is_defined')]
    undefined = [c.get('name_zh', '') for c in centers.values() if not c.get('is_defined')]
    if defined:
        lines.append(f"定义中心: {', '.join(defined)}")
    if undefined:
        lines.append(f"开放中心: {', '.join(undefined)}")
    lines.append('')

    # Sun gates
    p_gates = reading.get('gates', {}).get('personality', {})
    d_gates = reading.get('gates', {}).get('design', {})
    sun_p = p_gates.get('Sun', {})
    sun_d = d_gates.get('Sun', {})
    if sun_p:
        lines.append(f"意识太阳: {sun_p.get('gate', '')}号 {sun_p.get('gate_name', '')}")
    if sun_d:
        lines.append(f"设计太阳: {sun_d.get('gate', '')}号 {sun_d.get('gate_name', '')}")

    cross = reading.get('incarnation_cross', {})
    if cross.get('name_zh'):
        lines.append(f"人生交叉: {cross['name_zh']}")

    return '\n'.join(lines)
