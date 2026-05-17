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
    'Ajna':      {'gates': [24, 4, 17, 43, 11],                'zh': '逻辑中心',    'en': 'Ajna Center'},
    'Throat':    {'gates': [62, 23, 16, 35, 45, 33, 8, 20, 31, 7, 12, 22],
                                                              'zh': '喉咙中心',    'en': 'Throat Center'},
    'G':         {'gates': [1, 2, 7, 13, 15, 25, 10, 46],     'zh': '自我中心',    'en': 'G Center'},
    'Heart':     {'gates': [21, 40, 26, 51],                   'zh': '意志力中心',  'en': 'Heart Center'},
    'SolarPlexus':{'gates': [36, 22, 37, 6, 49, 55, 30],       'zh': '情绪中心',    'en': 'Solar Plexus'},
    'Spleen':    {'gates': [57, 44, 50, 28, 18, 48, 32, 54],   'zh': '直觉中心',    'en': 'Spleen Center'},
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
# Incarnation Cross names
# ============================================================

INCARNATION_CROSSES = {
    # Right Angle Crosses
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
    # Juxtaposition Crosses
    (20, 34, 37, 40): {'zh': '并列交叉之行动', 'en': 'Juxtaposition Cross of Action'},
    # Left Angle Crosses
    (24, 44, 7, 13):  {'zh': '左角度交叉之面具', 'en': 'Left Angle Cross of Masks'},
    (36, 6, 10, 15):  {'zh': '左角度交叉之需求', 'en': 'Left Angle Cross of Needs'},
}
