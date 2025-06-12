#!/usr/bin/env python3
"""
Verification script to display key reference table samples
"""

from tibetan_astro_tables import *

def main():
    print('=== CORE SIXTY-CYCLE COMBINATIONS (First 20) ===')
    for i, name in enumerate(SIXTY_CYCLE_NAMES[:20]):
        print(f'{i:2d}: {name}')

    print('\n=== MEWA ROTATION SAMPLES ===')
    samples = ['木阳鼠', '木阴牛', '火阳虎', '金阳马', '水阴猪']
    for name in samples:
        if name in LIFE_MEWA_ROTATION:
            life = LIFE_MEWA_ROTATION[name]
            body = BODY_MEWA_ROTATION[name] 
            power = POWER_MEWA_ROTATION[name]
            print(f'{name} → Life: {life}, Body: {body}, Power: {power}')

    print('\n=== DOCUMENT EXAMPLES VERIFICATION ===')
    print('1984 mod 12 =', 1984 % 12, '→', ANIMAL_SIGNS_MOD_12_MAP[1984 % 12])
    print('1984 mod 10 =', 1984 % 10, '→', TIANGAN_MAP_MOD_10[1984 % 10])
    print('Expected: 木阳鼠, Generated:', '木阳鼠' in SIXTY_CYCLE_NAMES)

    print('1990 mod 12 =', 1990 % 12, '→', ANIMAL_SIGNS_MOD_12_MAP[1990 % 12]) 
    print('1990 mod 10 =', 1990 % 10, '→', TIANGAN_MAP_MOD_10[1990 % 10])
    print('Expected: 金阳马, Position:', SIXTY_CYCLE_NAMES.index('金阳马') if '金阳马' in SIXTY_CYCLE_NAMES else 'NOT FOUND')

    print('\n=== OBSTACLE SYSTEM SAMPLES ===')
    print('Darkness Body Mewa for males 19+:', DARKNESS_BODY_MEWA['male_19_over'])
    print('Element clashes - Wood destroys:', ELEMENT_CLASH_MAP['木 (Wood)'])
    print('Mewa 4 color:', MEWA_COLORS[4], '| element:', MEWA_ELEMENTS[4])
    
    print('\n=== FULL SIXTY CYCLE (showing every 10th) ===')
    for i in range(0, 60, 10):
        name = SIXTY_CYCLE_NAMES[i]
        life = LIFE_MEWA_ROTATION[name]
        body = BODY_MEWA_ROTATION[name]
        power = POWER_MEWA_ROTATION[name]
        print(f'{i:2d}: {name} → L:{life} B:{body} P:{power}')

if __name__ == "__main__":
    main() 