"""
Human Design Chart System - Shared Constants

The single source of truth for gate order, center definitions, 
channel mappings, and interpretation texts.
"""

# ============================================================
# I Ching Wheel Configuration
# ============================================================

# Gate 41 starts at 2° Aquarius = 302° absolute
WHEEL_OFFSET_DEGREES = 302.0
GATE_SIZE_DEGREES = 360.0 / 64  # 5.625°

# Gate order around the mandala (counterclockwise)
# Index 0 = segment starting at WHEEL_OFFSET
GATE_ORDER = [
    41, 19, 13, 49, 30, 55, 37, 63, 22, 36, 25, 17, 21, 51, 42, 3,
    27, 24, 2, 23, 8, 20, 16, 35, 45, 12, 15, 52, 39, 53, 62, 56,
    31, 33, 7, 4, 29, 59, 40, 64, 47, 6, 46, 18, 48, 57, 32, 50,
    28, 44, 1, 43, 14, 34, 9, 5, 26, 11, 10, 58, 38, 54, 61, 60
]

# ============================================================
# Planets
# ============================================================

# Swiss Ephemeris planet IDs
PLANET_IDS = {
    'Sun': 0, 'Moon': 1, 'Mercury': 2, 'Venus': 3, 'Mars': 4,
    'Jupiter': 5, 'Saturn': 6, 'Uranus': 7, 'Neptune': 8, 'Pluto': 9,
    'NorthNode': 11,  # Mean Node
}

# Planets that are derived (not directly calculated)
DERIVED_PLANETS = {
    'Earth': 'Sun',      # Earth = Sun + 180°
    'SouthNode': 'NorthNode',  # S.Node = N.Node + 180°
}

PLANET_NAMES_ORDERED = [
    'Sun', 'Earth', 'Moon', 'NorthNode', 'SouthNode',
    'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn',
    'Uranus', 'Neptune', 'Pluto'
]

# ============================================================
# Centers
# ============================================================

CENTERS = {
    'Head':      {'gates': [64, 61, 63],                       'zh': '头脑中心',    'en': 'Head Center'},
    'Ajna':      {'gates': [47, 24, 4, 17, 43, 11],            'zh': '意识中心',    'en': 'Ajna Center'},
    'Throat':    {'gates': [62, 23, 56, 16, 35, 45, 33, 8, 20, 31, 12],
                                                              'zh': '喉咙中心',    'en': 'Throat Center'},
    'G':         {'gates': [1, 2, 7, 13, 15, 25, 10, 46],     'zh': '自我中心',    'en': 'G Center'},
    'Heart':     {'gates': [21, 40, 26, 51],                   'zh': '意志力中心',  'en': 'Heart Center'},
    'SolarPlexus':{'gates': [36, 22, 37, 6, 49, 55, 30],       'zh': '情绪中心',    'en': 'Solar Plexus'},
    'Spleen':    {'gates': [57, 44, 50, 28, 18, 48, 32],        'zh': '直觉中心',    'en': 'Spleen Center'},
    'Sacral':    {'gates': [5, 14, 29, 59, 9, 3, 42, 27, 34],  'zh': '荐骨中心',    'en': 'Sacral Center'},
    'Root':      {'gates': [38, 54, 58, 60, 52, 39, 53, 19, 41],'zh': '根部中心',   'en': 'Root Center'},
}

# Center connectivity for bodygraph layout
CENTER_CONNECTIONS = {
    'Head':      ['Ajna'],
    'Ajna':      ['Head', 'Throat'],
    'Throat':    ['Ajna', 'G', 'Heart', 'SolarPlexus'],
    'G':         ['Throat', 'Heart', 'Sacral', 'Spleen'],
    'Heart':     ['Throat', 'G'],
    'SolarPlexus':['Throat', 'Root', 'Sacral'],
    'Spleen':    ['G', 'Sacral', 'Root'],
    'Sacral':    ['G', 'Spleen', 'Root', 'SolarPlexus'],
    'Root':      ['SolarPlexus', 'Sacral', 'Spleen'],
}

# Motor centers (can manifest energy)
MOTOR_CENTERS = ['Heart', 'SolarPlexus', 'Root', 'Sacral']

# ============================================================
# Channels
# ============================================================

CHANNELS = {
    (1, 8):   {'zh': '启发通道',   'en': 'Inspiration',      'centers': ('G', 'Throat')},
    (2, 14):  {'zh': '脉动通道',   'en': 'Beating',          'centers': ('G', 'Sacral')},
    (3, 60):  {'zh': '突变通道',   'en': 'Mutation',         'centers': ('Sacral', 'Root')},
    (4, 63):  {'zh': '逻辑通道',   'en': 'Logic',            'centers': ('Ajna', 'Head')},
    (5, 15):  {'zh': '节律通道',   'en': 'Rhythm',           'centers': ('Sacral', 'G')},
    (6, 59):  {'zh': '亲密通道',   'en': 'Intimacy',         'centers': ('SolarPlexus', 'Sacral')},
    (7, 31):  {'zh': '领袖通道',   'en': 'Alpha',            'centers': ('G', 'Throat')},
    (9, 52):  {'zh': '专注通道',   'en': 'Concentration',    'centers': ('Sacral', 'Root')},
    (10, 57): {'zh': '完美通道',   'en': 'Perfection',       'centers': ('G', 'Spleen')},
    (10, 20): {'zh': '觉醒通道',   'en': 'Awakening',        'centers': ('G', 'Throat')},
    (10, 34): {'zh': '探索通道',   'en': 'Exploration',      'centers': ('G', 'Sacral')},
    (11, 56): {'zh': '好奇通道',   'en': 'Curiosity',        'centers': ('Ajna', 'Throat')},
    (12, 22): {'zh': '开放通道',   'en': 'Openness',         'centers': ('Throat', 'SolarPlexus')},
    (13, 33): {'zh': '浪子通道',   'en': 'Prodigal',         'centers': ('G', 'Throat')},
    (16, 48): {'zh': '天赋通道',   'en': 'Talent',           'centers': ('Throat', 'Spleen')},
    (17, 62): {'zh': '接纳通道',   'en': 'Acceptance',       'centers': ('Ajna', 'Throat')},
    (18, 58): {'zh': '判断通道',   'en': 'Judgment',         'centers': ('Spleen', 'Root')},
    (19, 49): {'zh': '综合通道',   'en': 'Synthesis',        'centers': ('Root', 'SolarPlexus')},
    (20, 34): {'zh': '魅力通道',   'en': 'Charisma',         'centers': ('Throat', 'Sacral')},
    (20, 57): {'zh': '脑波通道',   'en': 'Brainwave',        'centers': ('Throat', 'Spleen')},
    (21, 45): {'zh': '金钱通道',   'en': 'Money',            'centers': ('Heart', 'Throat')},
    (23, 43): {'zh': '天才通道',   'en': 'Genius',           'centers': ('Throat', 'Ajna')},
    (24, 61): {'zh': '觉知通道',   'en': 'Awareness',        'centers': ('Ajna', 'Head')},
    (25, 51): {'zh': '启动通道',   'en': 'Initiation',       'centers': ('G', 'Heart')},
    (26, 44): {'zh': '投降通道',   'en': 'Surrender',        'centers': ('Heart', 'Spleen')},
    (27, 50): {'zh': '守护通道',   'en': 'Preservation',     'centers': ('Sacral', 'Spleen')},
    (28, 38): {'zh': '奋战通道',   'en': 'Struggle',         'centers': ('Spleen', 'Root')},
    (29, 46): {'zh': '发现通道',   'en': 'Discovery',        'centers': ('Sacral', 'G')},
    (30, 41): {'zh': '识别通道',   'en': 'Recognition',      'centers': ('SolarPlexus', 'Root')},
    (32, 54): {'zh': '转化通道',   'en': 'Transformation',   'centers': ('Spleen', 'Root')},
    (34, 57): {'zh': '力量通道',   'en': 'Power',            'centers': ('Sacral', 'Spleen')},
    (35, 36): {'zh': '无常通道',   'en': 'Transitoriness',   'centers': ('Throat', 'SolarPlexus')},
    (37, 40): {'zh': '社群通道',   'en': 'Community',        'centers': ('SolarPlexus', 'Heart')},
    (39, 55): {'zh': '情感通道',   'en': 'Emoting',          'centers': ('Root', 'SolarPlexus')},
    (42, 53): {'zh': '成熟通道',   'en': 'Maturation',       'centers': ('Sacral', 'Root')},
    (47, 64): {'zh': '抽象通道',   'en': 'Abstraction',      'centers': ('Ajna', 'Head')},
}

# Build reverse lookup: gate -> which channels it belongs to
GATE_TO_CHANNELS = {}
for (g1, g2), info in CHANNELS.items():
    GATE_TO_CHANNELS.setdefault(g1, []).append((g1, g2))
    GATE_TO_CHANNELS.setdefault(g2, []).append((g1, g2))

# ============================================================
# Gate Descriptions
# ============================================================

GATE_INFO = {
    1:   {'zh': '创意',   'en': 'The Creative',       'i_ching': '乾'},
    2:   {'zh': '接纳',   'en': 'The Receptive',      'i_ching': '坤'},
    3:   {'zh': '开端',   'en': 'Ordering',            'i_ching': '屯'},
    4:   {'zh': '公式',   'en': 'Formulization',       'i_ching': '蒙'},
    5:   {'zh': '等待',   'en': 'Waiting',             'i_ching': '需'},
    6:   {'zh': '摩擦',   'en': 'Conflict',            'i_ching': '讼'},
    7:   {'zh': '军队',   'en': 'The Army',            'i_ching': '师'},
    8:   {'zh': '凝聚',   'en': 'Holding Together',    'i_ching': '比'},
    9:   {'zh': '聚焦',   'en': 'Small Harvest',       'i_ching': '小畜'},
    10:  {'zh': '前行',   'en': 'Treading',            'i_ching': '履'},
    11:  {'zh': '和平',   'en': 'Peace',               'i_ching': '泰'},
    12:  {'zh': '静止',   'en': 'Standstill',          'i_ching': '否'},
    13:  {'zh': '聆听',   'en': 'Fellowship',          'i_ching': '同人'},
    14:  {'zh': '丰饶',   'en': 'Possession in Great',  'i_ching': '大有'},
    15:  {'zh': '谦逊',   'en': 'Modesty',             'i_ching': '谦'},
    16:  {'zh': '热忱',   'en': 'Enthusiasm',          'i_ching': '豫'},
    17:  {'zh': '意见',   'en': 'Following',           'i_ching': '随'},
    18:  {'zh': '修正',   'en': 'Work on Decay',       'i_ching': '蛊'},
    19:  {'zh': '趋近',   'en': 'Approach',            'i_ching': '临'},
    20:  {'zh': '当下',   'en': 'Contemplation',       'i_ching': '观'},
    21:  {'zh': '控制',   'en': 'Biting Through',      'i_ching': '噬嗑'},
    22:  {'zh': '优雅',   'en': 'Grace',               'i_ching': '贲'},
    23:  {'zh': '裂变',   'en': 'Splitting Apart',     'i_ching': '剥'},
    24:  {'zh': '回归',   'en': 'Return',              'i_ching': '复'},
    25:  {'zh': '纯真',   'en': 'Innocence',           'i_ching': '无妄'},
    26:  {'zh': '驯服',   'en': 'Taming Power',        'i_ching': '大畜'},
    27:  {'zh': '滋养',   'en': 'Nourishment',         'i_ching': '颐'},
    28:  {'zh': '冒险',   'en': 'Preponderance',       'i_ching': '大过'},
    29:  {'zh': '承诺',   'en': 'The Abysmal',         'i_ching': '坎'},
    30:  {'zh': '欲望',   'en': 'The Clinging',        'i_ching': '离'},
    31:  {'zh': '影响',   'en': 'Influence',           'i_ching': '咸'},
    32:  {'zh': '延续',   'en': 'Duration',            'i_ching': '恒'},
    33:  {'zh': '退隐',   'en': 'Retreat',             'i_ching': '遁'},
    34:  {'zh': '力量',   'en': 'Great Power',         'i_ching': '大壮'},
    35:  {'zh': '变化',   'en': 'Progress',            'i_ching': '晋'},
    36:  {'zh': '幽暗',   'en': 'Darkening',           'i_ching': '明夷'},
    37:  {'zh': '家庭',   'en': 'The Family',          'i_ching': '家人'},
    38:  {'zh': '对抗',   'en': 'Opposition',          'i_ching': '睽'},
    39:  {'zh': '阻碍',   'en': 'Obstruction',         'i_ching': '蹇'},
    40:  {'zh': '释放',   'en': 'Deliverance',         'i_ching': '解'},
    41:  {'zh': '缩减',   'en': 'Decrease',            'i_ching': '损'},
    42:  {'zh': '增益',   'en': 'Increase',            'i_ching': '益'},
    43:  {'zh': '突破',   'en': 'Breakthrough',        'i_ching': '夬'},
    44:  {'zh': '聚合',   'en': 'Coming to Meet',      'i_ching': '姤'},
    45:  {'zh': '聚集',   'en': 'Gathering',           'i_ching': '萃'},
    46:  {'zh': '推进',   'en': 'Pushing Upward',      'i_ching': '升'},
    47:  {'zh': '压抑',   'en': 'Oppression',          'i_ching': '困'},
    48:  {'zh': '深井',   'en': 'The Well',            'i_ching': '井'},
    49:  {'zh': '革命',   'en': 'Revolution',          'i_ching': '革'},
    50:  {'zh': '熔炉',   'en': 'The Cauldron',        'i_ching': '鼎'},
    51:  {'zh': '震惊',   'en': 'Arousal',             'i_ching': '震'},
    52:  {'zh': '静山',   'en': 'Keeping Still',       'i_ching': '艮'},
    53:  {'zh': '开始',   'en': 'Development',         'i_ching': '渐'},
    54:  {'zh': '野心',   'en': 'The Marrying Maiden', 'i_ching': '归妹'},
    55:  {'zh': '丰盛',   'en': 'Abundance',           'i_ching': '丰'},
    56:  {'zh': '游走',   'en': 'The Wanderer',        'i_ching': '旅'},
    57:  {'zh': '直觉',   'en': 'The Gentle',          'i_ching': '巽'},
    58:  {'zh': '喜悦',   'en': 'Joyous',              'i_ching': '兑'},
    59:  {'zh': '涣散',   'en': 'Dispersion',          'i_ching': '涣'},
    60:  {'zh': '限制',   'en': 'Limitation',          'i_ching': '节'},
    61:  {'zh': '真理',   'en': 'Inner Truth',         'i_ching': '中孚'},
    62:  {'zh': '细节',   'en': 'Preponderance Small',  'i_ching': '小过'},
    63:  {'zh': '完成',   'en': 'After Completion',    'i_ching': '既济'},
    64:  {'zh': '混沌',   'en': 'Before Completion',   'i_ching': '未济'},
}

# ============================================================
# Type Definitions
# ============================================================

TYPES = {
    'Generator': {
        'zh': '纯生产者', 'en': 'Generator',
        'strategy_zh': '等待回应', 'strategy_en': 'Wait to Respond',
        'signature_zh': '满足', 'signature_en': 'Satisfaction',
        'notself_zh': '挫败', 'notself_en': 'Frustration',
        'pct': 37,
    },
    'ManifestingGenerator': {
        'zh': '显示生产者', 'en': 'Manifesting Generator',
        'strategy_zh': '等待回应后告知', 'strategy_en': 'Wait to Respond, then Inform',
        'signature_zh': '满足', 'signature_en': 'Satisfaction',
        'notself_zh': '愤怒/挫败', 'notself_en': 'Anger/Frustration',
        'pct': 33,
    },
    'Manifestor': {
        'zh': '显示者', 'en': 'Manifestor',
        'strategy_zh': '告知', 'strategy_en': 'Inform',
        'signature_zh': '和平', 'signature_en': 'Peace',
        'notself_zh': '愤怒', 'notself_en': 'Anger',
        'pct': 8,
    },
    'Projector': {
        'zh': '投射者', 'en': 'Projector',
        'strategy_zh': '等待邀请', 'strategy_en': 'Wait for Invitation',
        'signature_zh': '成功', 'signature_en': 'Success',
        'notself_zh': '苦涩', 'notself_en': 'Bitterness',
        'pct': 20,
    },
    'Reflector': {
        'zh': '反映者', 'en': 'Reflector',
        'strategy_zh': '等待28天', 'strategy_en': 'Wait a Lunar Cycle',
        'signature_zh': '惊喜', 'signature_en': 'Surprise',
        'notself_zh': '失望', 'notself_en': 'Disappointment',
        'pct': 1,
    },
}

# ============================================================
# Authority Priority
# ============================================================

AUTHORITY_PRIORITY = [
    ('SolarPlexus', {'zh': '情绪型权威', 'en': 'Emotional Authority'}),
    ('Sacral',      {'zh': '荐骨型权威', 'en': 'Sacral Authority'}),
    ('Spleen',      {'zh': '直觉型权威', 'en': 'Splenic Authority'}),
    ('Heart',       {'zh': '意志力权威', 'en': 'Ego Authority'}),
    ('G',           {'zh': '自我型权威', 'en': 'Self Authority'}),
    ('Throat',      {'zh': '喉咙型权威', 'en': 'Throat Authority'}),
    (None,          {'zh': '月循环/无内在权威', 'en': 'Lunar/No Authority'}),
]

# ============================================================
# Profile (Line) descriptions
# ============================================================

LINE_INFO = {
    1: {'zh': '研究者', 'en': 'Investigator', 'desc_zh': '需要深入探究本质，建立稳固基础'},
    2: {'zh': '隐士', 'en': 'Hermit', 'desc_zh': '天然天赋，需要独处空间来发展'},
    3: {'zh': '烈士', 'en': 'Martyr', 'desc_zh': '通过试错学习，拥抱失败'},
    4: {'zh': '机会主义者', 'en': 'Opportunist', 'desc_zh': '通过社交网络扩展机会'},
    5: {'zh': '异端者', 'en': 'Heretic', 'desc_zh': '天生投射力，解决问题'},
    6: {'zh': '典范', 'en': 'Role Model', 'desc_zh': '三段人生，最终成为典范'},
}

# ============================================================
# Incarnation Cross System (192 = 64 base themes × 3 angles)
# ============================================================

# Profile determines the angle (Right/Juxtaposition/Left)
PROFILE_TO_ANGLE = {
    '1/3': 'right', '1/4': 'right', '2/4': 'right', '2/5': 'right',
    '3/5': 'right', '3/6': 'right', '4/6': 'right',
    '4/1': 'juxtaposition',
    '5/1': 'left', '5/2': 'left', '6/2': 'left', '6/3': 'left',
}

# Angle name prefixes
ANGLE_NAMES = {
    'right':         {'zh': '右角度交叉之', 'en': 'Right Angle Cross of '},
    'juxtaposition': {'zh': '并列交叉之',   'en': 'Juxtaposition Cross of '},
    'left':          {'zh': '左角度交叉之', 'en': 'Left Angle Cross of '},
}

# Each Personality Sun gate uniquely determines the cross base name.
# The 64 gates are grouped into 16 themes of 4 gates each (quarters of the wheel).
# Key = P_Sun gate number, Value = {'zh': Chinese name, 'en': English name}
CROSS_NAMES = {
    # === Quarter of Initiation (Gates 13, 49, 30, 55, 37, 63, 22, 36, 25, 17, 21, 51, 42, 3, 27, 24) ===
    13: {'zh': '伊甸园', 'en': 'Eden'},
    49: {'zh': '原则', 'en': 'Principles'},
    30: {'zh': '命运', 'en': 'Fates'},
    55: {'zh': '灵性', 'en': 'Spirit'},
    37: {'zh': '计划', 'en': 'Planning'},
    63: {'zh': '疑问', 'en': 'Doubts'},
    22: {'zh': '优雅', 'en': 'Grace'},
    36: {'zh': '伊甸园2', 'en': 'Eden 2'},
    25: {'zh': '爱的容器', 'en': 'the Vessel of Love'},
    17: {'zh': '服务', 'en': 'Service'},
    21: {'zh': '主宰', 'en': 'Rulership'},
    51: {'zh': '穿透', 'en': 'Penetration'},
    42: {'zh': '玛雅', 'en': 'Maya'},
    3:  {'zh': '法则', 'en': 'Laws'},
    27: {'zh': '看守人', 'en': 'the Custodian'},
    24: {'zh': '四方之路', 'en': 'the Four Ways'},

    # === Quarter of Civilization (Gates 2, 23, 8, 20, 16, 35, 45, 12, 15, 52, 39, 53, 62, 56, 31, 33) ===
    2:  {'zh': '狮身人面像', 'en': 'the Sphinx'},
    23: {'zh': '同化', 'en': 'Assimilation'},
    8:  {'zh': '贡献', 'en': 'Contribution'},
    20: {'zh': '沉睡的凤凰', 'en': 'the Sleeping Phoenix'},
    16: {'zh': '鉴定', 'en': 'Identification'},
    35: {'zh': '意识', 'en': 'Consciousness'},
    45: {'zh': '统治者', 'en': 'Rulership 2'},
    12: {'zh': '教育', 'en': 'Education'},
    15: {'zh': '极端', 'en': 'Extremes'},
    52: {'zh': '服务2', 'en': 'Service 2'},
    39: {'zh': '紧张', 'en': 'Tension'},
    53: {'zh': '循环', 'en': 'Cycles'},
    62: {'zh': '玛雅2', 'en': 'Maya 2'},
    56: {'zh': '刺激', 'en': 'Stimulation'},
    31: {'zh': '出乎意料', 'en': 'the Unexpected'},
    33: {'zh': '四方之路2', 'en': 'the Four Ways 2'},

    # === Quarter of Duality (Gates 7, 4, 29, 59, 40, 64, 47, 6, 46, 18, 48, 57, 32, 50, 28, 44) ===
    7:  {'zh': '狮身人面像2', 'en': 'the Sphinx 2'},
    4:  {'zh': '解释', 'en': 'Explanation'},
    29: {'zh': '传染', 'en': 'Contagion'},
    59: {'zh': '沉睡的凤凰2', 'en': 'the Sleeping Phoenix 2'},
    40: {'zh': '鉴定2', 'en': 'Identification 2'},
    64: {'zh': '意识2', 'en': 'Consciousness 2'},
    47: {'zh': '统治者2', 'en': 'Rulership 3'},
    6:  {'zh': '飞机', 'en': 'the Plane'},
    46: {'zh': '爱的容器2', 'en': 'the Vessel of Love 2'},
    18: {'zh': '动荡', 'en': 'Upheaval'},
    48: {'zh': '深度', 'en': 'Depth'},
    57: {'zh': '直觉', 'en': 'Intuition'},
    32: {'zh': '玛雅3', 'en': 'Maya 3'},
    50: {'zh': '法则2', 'en': 'Laws 2'},
    28: {'zh': '风险', 'en': 'Risks'},
    44: {'zh': '四方之路3', 'en': 'the Four Ways 3'},

    # === Quarter of Mutation (Gates 1, 43, 14, 34, 9, 5, 26, 11, 10, 58, 38, 54, 61, 60, 41, 19) ===
    1:  {'zh': '狮身人面像3', 'en': 'the Sphinx 3'},
    43: {'zh': '洞察', 'en': 'Insight'},
    14: {'zh': '传染2', 'en': 'Contagion 2'},
    34: {'zh': '沉睡的凤凰3', 'en': 'the Sleeping Phoenix 3'},
    9:  {'zh': '计划2', 'en': 'Planning 2'},
    5:  {'zh': '意识3', 'en': 'Consciousness 3'},
    26: {'zh': '迷惑', 'en': 'Trickster'},
    11: {'zh': '教育2', 'en': 'Education 2'},
    10: {'zh': '爱', 'en': 'Love'},
    58: {'zh': '服务3', 'en': 'Service 3'},
    38: {'zh': '紧张2', 'en': 'Tension 2'},
    54: {'zh': '循环2', 'en': 'Cycles 2'},
    61: {'zh': '朦胧', 'en': 'Obscuration'},
    60: {'zh': '限制', 'en': 'Limitation'},
    41: {'zh': '出乎意料2', 'en': 'the Unexpected 2'},
    19: {'zh': '四方之路4', 'en': 'the Four Ways 4'},
}

# Some gates have different cross names depending on the angle.
# If a gate is NOT listed here, the same base name is used for all 3 angles.
# Key = P_Sun gate, Value = {angle: {'zh': ..., 'en': ...}}
CROSS_NAME_OVERRIDES = {
    # Gate 20: Right=沉睡的凤凰, Juxtaposition=当下, Left=二元性
    20: {
        'juxtaposition': {'zh': '当下', 'en': 'the Now'},
        'left':          {'zh': '二元性', 'en': 'Duality'},
    },
    # Gate 34: Right=沉睡的凤凰3, Juxtaposition=力量, Left=二元性2
    34: {
        'juxtaposition': {'zh': '力量', 'en': 'Power'},
        'left':          {'zh': '二元性2', 'en': 'Duality 2'},
    },
    # Gate 59: Right=沉睡的凤凰2, Juxtaposition=策略, Left=突破
    59: {
        'juxtaposition': {'zh': '策略', 'en': 'Strategy'},
        'left':          {'zh': '突破', 'en': 'Breakthrough'},
    },
    # Gate 10: Right=爱, Juxtaposition=行为, Left=预防
    10: {
        'juxtaposition': {'zh': '行为', 'en': 'Behavior'},
        'left':          {'zh': '预防', 'en': 'Prevention'},
    },
    # Gate 15: Right=极端, Juxtaposition=极端, Left=预防2
    15: {
        'left':          {'zh': '预防2', 'en': 'Prevention 2'},
    },
    # Gate 46: Right=爱的容器2, Juxtaposition=行为2, Left=预防3
    46: {
        'juxtaposition': {'zh': '行为2', 'en': 'Behavior 2'},
        'left':          {'zh': '预防3', 'en': 'Prevention 3'},
    },
    # Gate 25: Right=爱的容器, Juxtaposition=纯真, Left=治愈
    25: {
        'juxtaposition': {'zh': '纯真', 'en': 'Innocence'},
        'left':          {'zh': '治愈', 'en': 'Healing'},
    },
    # Gate 36: Right=伊甸园2, Juxtaposition=危机, Left=飞机2
    36: {
        'juxtaposition': {'zh': '危机', 'en': 'Crisis'},
        'left':          {'zh': '飞机2', 'en': 'the Plane 2'},
    },
    # Gate 6: Right=飞机, Juxtaposition=冲突, Left=飞机3
    6: {
        'juxtaposition': {'zh': '冲突', 'en': 'Conflict'},
        'left':          {'zh': '飞机3', 'en': 'the Plane 3'},
    },
    # Gate 45: Right=统治者, Juxtaposition=拥有, Left=对抗
    45: {
        'juxtaposition': {'zh': '拥有', 'en': 'Possession'},
        'left':          {'zh': '对抗', 'en': 'Confrontation'},
    },
    # Gate 47: Right=统治者2, Juxtaposition=压迫, Left=对抗2
    47: {
        'juxtaposition': {'zh': '压迫', 'en': 'Oppression'},
        'left':          {'zh': '对抗2', 'en': 'Confrontation 2'},
    },
    # Gate 21: Right=主宰, Juxtaposition=控制, Left=努力
    21: {
        'juxtaposition': {'zh': '控制', 'en': 'Control'},
        'left':          {'zh': '努力', 'en': 'Endeavor'},
    },
    # Gate 51: Right=穿透, Juxtaposition=震惊, Left=竞赛
    51: {
        'juxtaposition': {'zh': '震惊', 'en': 'Shock'},
        'left':          {'zh': '竞赛', 'en': 'Competition'},
    },
    # Gate 26: Right=迷惑, Juxtaposition=迷惑, Left=告知
    26: {
        'left':          {'zh': '告知', 'en': 'Informing'},
    },
    # Gate 44: Right=四方之路3, Juxtaposition=警觉, Left=面具
    44: {
        'juxtaposition': {'zh': '警觉', 'en': 'Alertness'},
        'left':          {'zh': '面具', 'en': 'Masks'},
    },
    # Gate 24: Right=四方之路, Juxtaposition=合理化, Left=轮回
    24: {
        'juxtaposition': {'zh': '合理化', 'en': 'Rationalization'},
        'left':          {'zh': '轮回', 'en': 'Incarnation'},
    },
    # Gate 33: Right=四方之路2, Juxtaposition=退隐, Left=精炼
    33: {
        'juxtaposition': {'zh': '退隐', 'en': 'Retreat'},
        'left':          {'zh': '精炼', 'en': 'Refinement'},
    },
    # Gate 19: Right=四方之路4, Juxtaposition=需要, Left=精炼2
    19: {
        'juxtaposition': {'zh': '需要', 'en': 'Need'},
        'left':          {'zh': '精炼2', 'en': 'Refinement 2'},
    },
}

# Legacy dict kept for backward compatibility (original 13 entries).
# New code should use CROSS_NAMES + PROFILE_TO_ANGLE instead.
INCARNATION_CROSSES = {
    (57, 51, 53, 54): {'zh': '右角度交叉之直觉', 'en': 'Right Angle Cross of Intuition'},
    (1, 2, 7, 13):    {'zh': '右角度交叉之计划', 'en': 'Right Angle Cross of Planning'},
    (4, 49, 23, 43):  {'zh': '右角度交叉之解释', 'en': 'Right Angle Cross of Explanation'},
    (3, 50, 59, 55):  {'zh': '右角度交叉之交配', 'en': 'Right Angle Cross of Mating'},
    (5, 35, 47, 64):  {'zh': '右角度交叉之沉睡', 'en': 'Right Angle Cross of Sleeping'},
    (7, 13, 23, 43):  {'zh': '右角度交叉之意识', 'en': 'Right Angle Cross of Consciousness'},
    (9, 16, 40, 37):  {'zh': '右角度交叉之计划2', 'en': 'Right Angle Cross of Planning 2'},
    (10, 34, 15, 5):  {'zh': '右角度交叉之爱', 'en': 'Right Angle Cross of Love'},
    (14, 8, 59, 55):  {'zh': '右角度交叉之服务', 'en': 'Right Angle Cross of Service'},
    (17, 18, 38, 39): {'zh': '右角度交叉之解释2', 'en': 'Right Angle Cross of Explanation 2'},
    (20, 34, 37, 40): {'zh': '并列交叉之行动', 'en': 'Juxtaposition Cross of Action'},
    (24, 44, 7, 13):  {'zh': '左角度交叉之面具', 'en': 'Left Angle Cross of Masks'},
    (36, 6, 10, 15):  {'zh': '左角度交叉之需求', 'en': 'Left Angle Cross of Needs'},
}
