#!/usr/bin/env python3
"""
Tibetan Astrological System - Reference Tables
Based on the Nine Palaces Outer Calculation (九宫外算) system
"""

# =============================================================================
# CORE ANIMAL AND ELEMENT MAPPINGS
# =============================================================================

# Animal Signs based on n mod 12
# From document: 1984 mod 12 = 4 → 鼠 (Rat), 1990 mod 12 = 10 → 马 (Horse)
ANIMAL_SIGNS_MOD_12_MAP = {
    4: "鼠 (Rat)",
    5: "牛 (Ox)", 
    6: "虎 (Tiger)",
    7: "兔 (Rabbit)",
    8: "龙 (Dragon)",
    9: "蛇 (Snake)",
    10: "马 (Horse)",
    11: "羊 (Sheep)",
    0: "猴 (Monkey)",
    1: "鸡 (Rooster)",
    2: "狗 (Dog)",
    3: "猪 (Pig)"
}

# Tiangan (Heavenly Stems) mapping for n mod 10
# From document: 1984 mod 10 = 4 → 木阳, 1990 mod 10 = 0 → 金阳
TIANGAN_MAP_MOD_10 = {
    4: {"element": "木 (Wood)", "yin_yang": "阳 (Yang)"},    # 甲 (Jia)
    5: {"element": "木 (Wood)", "yin_yang": "阴 (Yin)"},     # 乙 (Yi)
    6: {"element": "火 (Fire)", "yin_yang": "阳 (Yang)"},    # 丙 (Bing)
    7: {"element": "火 (Fire)", "yin_yang": "阴 (Yin)"},     # 丁 (Ding)
    8: {"element": "土 (Earth)", "yin_yang": "阳 (Yang)"},   # 戊 (Wu)
    9: {"element": "土 (Earth)", "yin_yang": "阴 (Yin)"},    # 己 (Ji)
    0: {"element": "金 (Metal)", "yin_yang": "阳 (Yang)"},   # 庚 (Geng)
    1: {"element": "金 (Metal)", "yin_yang": "阴 (Yin)"},    # 辛 (Xin)
    2: {"element": "水 (Water)", "yin_yang": "阳 (Yang)"},   # 壬 (Ren)
    3: {"element": "水 (Water)", "yin_yang": "阴 (Yin)"}     # 癸 (Gui)
}

# Generate the complete 60-cycle combinations systematically
# The 60-cycle follows the pattern where tiangan (10) and dizhi (12) advance together
# Starting from 甲子 (Wood-Yang-Rat) which is position 0 in traditional systems

def generate_sixty_cycle_names():
    """Generate the complete 60-cycle combinations in correct order"""
    cycle_names = []
    
    # Start from the traditional beginning - 甲子 corresponds to 木阳鼠
    for i in range(60):
        # Calculate tiangan and dizhi indices
        tiangan_index = i % 10
        dizhi_index = i % 12
        
        # Map to our mod system (where 4 = 鼠, 0 = 金阳, etc.)
        actual_tiangan_mod = (tiangan_index + 4) % 10  # Start from 4 (木阳)
        actual_animal_mod = (dizhi_index + 4) % 12     # Start from 4 (鼠)
        
        element = TIANGAN_MAP_MOD_10[actual_tiangan_mod]["element"]
        yin_yang = TIANGAN_MAP_MOD_10[actual_tiangan_mod]["yin_yang"]
        animal = ANIMAL_SIGNS_MOD_12_MAP[actual_animal_mod]
        
        # Create clean format for lookup (remove English translations)
        element_clean = element.split(' ')[0]  # "木 (Wood)" -> "木"
        yin_yang_clean = yin_yang.split(' ')[0]  # "阳 (Yang)" -> "阳"
        animal_clean = animal.split(' ')[0]  # "鼠 (Rat)" -> "鼠"
        
        sixty_cycle_name = f"{element_clean}{yin_yang_clean}{animal_clean}"
        cycle_names.append(sixty_cycle_name)
    
    return cycle_names

SIXTY_CYCLE_NAMES = generate_sixty_cycle_names()

# =============================================================================
# MEWA (NINE PALACES) MAPPINGS
# =============================================================================

# Mewa number to color mapping
MEWA_COLORS = {
    1: "白 (White)",
    2: "黑 (Black)", 
    3: "蓝 (Blue)",
    4: "绿 (Green)",
    5: "黄 (Yellow)",
    6: "白 (White)",
    7: "红 (Red)",
    8: "白 (White)",
    9: "红 (Red)"
}

# Mewa number to element mapping (derived from colors)
MEWA_ELEMENTS = {
    1: "金 (Metal)",   # White
    2: "水 (Water)",   # Black
    3: "水 (Water)",   # Blue
    4: "木 (Wood)",    # Green
    5: "土 (Earth)",   # Yellow
    6: "金 (Metal)",   # White
    7: "火 (Fire)",    # Red
    8: "金 (Metal)",   # White
    9: "火 (Fire)"     # Red
}

# Generate Mewa rotation mappings following the reverse sequence (9,8,7,6,5,4,3,2,1)
# Starting points from document: 木阳鼠 → Life=1, Body=4, Power=7

def generate_mewa_rotation_sequence(start_mewa, length=60):
    """Generate a sequence of Mewa numbers starting from start_mewa, going in reverse (9→1)"""
    sequence = []
    current = start_mewa
    for i in range(length):
        sequence.append(current)
        current -= 1
        if current < 1:
            current = 9
    return sequence

# Generate Life Mewa rotation (starts at 1 for 木阳鼠)
life_sequence = generate_mewa_rotation_sequence(1, 60)
LIFE_MEWA_ROTATION = {SIXTY_CYCLE_NAMES[i]: life_sequence[i] for i in range(60)}

# Generate Body Mewa rotation (starts at 4 for 木阳鼠)  
body_sequence = generate_mewa_rotation_sequence(4, 60)
BODY_MEWA_ROTATION = {SIXTY_CYCLE_NAMES[i]: body_sequence[i] for i in range(60)}

# Generate Power Mewa rotation (starts at 7 for 木阳鼠)
power_sequence = generate_mewa_rotation_sequence(7, 60)
POWER_MEWA_ROTATION = {SIXTY_CYCLE_NAMES[i]: power_sequence[i] for i in range(60)}

# =============================================================================
# OBSTACLE SYSTEM MAPPINGS
# =============================================================================

# Darkness Body Mewa for Regional Obstacle (RO)
DARKNESS_BODY_MEWA = {
    "9_under": 1,                    # 9岁以下 → 1白
    "9_18": 3,                       # 9-18岁 → 3蓝
    "male_19_over": 2,               # 19岁以上，男 → 2黑
    "sex_worker_19_over": 4,         # 19岁以上，性工作者 → 4绿
    "monastic_19_over": 5,           # 19岁以上，出家人 → 5黄
    "lay_practitioner_19_over": 6,   # 19岁以上，居家士 → 6白
    "female_19_over": 7,             # 19岁以上，女 → 7红
    "official_19_over": 8,           # 19岁以上，官员 → 8红
    "elderly_60_over": 9             # 60岁以上，老年人 → 9红
}

# Five Elements Destructive Cycle
ELEMENT_CLASH_MAP = {
    "木 (Wood)": "土 (Earth)",
    "火 (Fire)": "金 (Metal)", 
    "土 (Earth)": "水 (Water)",
    "金 (Metal)": "木 (Wood)",
    "水 (Water)": "火 (Fire)"
}

# Obstacle interpretations and solutions
OBSTACLE_INTERPRETATIONS = {
    "RO": {
        "condition_met": "疾病、盗窃、遇一类遇事不顺的非人 (Disease, theft, encountering obstacles and undesired non-human entities)"
    },
    "HO": {
        "condition_met": "Powerful ghost of hunting (Tsen) come to home"
    },
    "BO": {
        "黑 (Black)": "Meeting with demon (dud) —— 心神不安 (Unease of mind)",
        "蓝 (Blue)": "Meeting with ghost (Dre) —— 疾病 (内) (Illness - internal)",
        "绿 (Green)": "Meeting with dragon (lu) —— 疾病 (皮肤病) (Illness - skin disease)",
        "黄 (Yellow)": "Meeting with hunting ghost (ngur tsen) and land-owner (房屋不稳 生意不顺) (Unstable house, business not smooth)",
        "红 (Red)": "Contention of mouth and tongue",
        "白 (White)": "Meeting with spirits of white category"
    },
    "DO": {
        "element_clash": "人畜均衰、不兴旺 (Decline for people and livestock, not prosperous)",
        "three_colors_same": {
            "白 (White)": "护法神逃逸，（需强化守护、安魂）(Guardian spirits flee, need to strengthen protection, pacify soul)",
            "蓝 (Blue)": "口舌之争与水灾 (Disputes and water disasters)", 
            "绿 (Green)": "Meeting with dragon (lu) —— 皮肤病 不宜动土 (Skin disease, not suitable to break ground)",
            "黄 (Yellow)": "Powerful ghost of hunting (Tsen)",
            "红 (Red)": "伤患 能量过低 (Injury/illness, low energy)"
        }
    }
}

# =============================================================================
# PROSPERITY ASSESSMENT SYSTEM (SUBSYSTEM 4)
# =============================================================================

# Event types for prosperity assessment
PROSPERITY_EVENT_TYPES = [
    "屠杀 (Massacre)",
    "怀孕 (Pregnancy)", 
    "成年 (Adulthood)",
    "生辰 (Birthday)",
    "洗礼 (Baptism)",
    "着衣 (Wearing new clothes)",
    "行事 (Undertaking activities)",
    "盛 (Prosperity)",
    "衰 (Decline)",
    "病 (Sickness)",
    "死 (Death)",
    "殡葬 (Funeral)"
]

# Hour animal signs mapping (2-hour periods)
HOUR_ANIMAL_MAP = {
    23: "鼠 (Rat)", 0: "鼠 (Rat)", 1: "鼠 (Rat)",
    2: "牛 (Ox)", 3: "牛 (Ox)",
    4: "虎 (Tiger)", 5: "虎 (Tiger)",
    6: "兔 (Rabbit)", 7: "兔 (Rabbit)",
    8: "龙 (Dragon)", 9: "龙 (Dragon)",
    10: "蛇 (Snake)", 11: "蛇 (Snake)",
    12: "马 (Horse)", 13: "马 (Horse)",
    14: "羊 (Sheep)", 15: "羊 (Sheep)",
    16: "猴 (Monkey)", 17: "猴 (Monkey)",
    18: "鸡 (Rooster)", 19: "鸡 (Rooster)",
    20: "狗 (Dog)", 21: "狗 (Dog)",
    22: "猪 (Pig)"
}

# Animal to element mapping for prosperity calculations
ANIMAL_ELEMENT_MAP = {
    "鼠 (Rat)": "水 (Water)",
    "牛 (Ox)": "土 (Earth)",
    "虎 (Tiger)": "木 (Wood)",
    "兔 (Rabbit)": "木 (Wood)",
    "龙 (Dragon)": "土 (Earth)",
    "蛇 (Snake)": "火 (Fire)",
    "马 (Horse)": "火 (Fire)",
    "羊 (Sheep)": "土 (Earth)",
    "猴 (Monkey)": "金 (Metal)",
    "鸡 (Rooster)": "金 (Metal)",
    "狗 (Dog)": "土 (Earth)",
    "猪 (Pig)": "水 (Water)"
}

# Five Elements Generative Cycle
ELEMENT_GENERATE_MAP = {
    "木 (Wood)": "火 (Fire)",
    "火 (Fire)": "土 (Earth)",
    "土 (Earth)": "金 (Metal)",
    "金 (Metal)": "水 (Water)",
    "水 (Water)": "木 (Wood)"
}

if __name__ == "__main__":
    # Print some samples for verification
    print("=== SAMPLE VERIFICATION ===")
    print(f"First 10 sixty-cycle names: {SIXTY_CYCLE_NAMES[:10]}")
    print(f"木阳鼠 → Life: {LIFE_MEWA_ROTATION.get('木阳鼠', 'NOT FOUND')}")
    print(f"木阳鼠 → Body: {BODY_MEWA_ROTATION.get('木阳鼠', 'NOT FOUND')}")
    print(f"木阳鼠 → Power: {POWER_MEWA_ROTATION.get('木阳鼠', 'NOT FOUND')}")
    print(f"Total sixty-cycle combinations: {len(SIXTY_CYCLE_NAMES)}")
    
    # Verify key examples from document
    print(f"\n=== DOCUMENT EXAMPLES VERIFICATION ===")
    print(f"1984 calculation test:")
    print(f"  1984 mod 12 = {1984 % 12} → {ANIMAL_SIGNS_MOD_12_MAP.get(1984 % 12, 'NOT FOUND')}")
    print(f"  1984 mod 10 = {1984 % 10} → {TIANGAN_MAP_MOD_10.get(1984 % 10, 'NOT FOUND')}")
    
    print(f"1990 calculation test:")
    print(f"  1990 mod 12 = {1990 % 12} → {ANIMAL_SIGNS_MOD_12_MAP.get(1990 % 12, 'NOT FOUND')}")
    print(f"  1990 mod 10 = {1990 % 10} → {TIANGAN_MAP_MOD_10.get(1990 % 10, 'NOT FOUND')}")
    
    # Test if we can find 金阳马 in our cycle
    target_1990 = "金阳马"
    if target_1990 in SIXTY_CYCLE_NAMES:
        print(f"  Found {target_1990} at position {SIXTY_CYCLE_NAMES.index(target_1990)}")
    else:
        print(f"  {target_1990} NOT FOUND in cycle") 