Okay, this is a fascinating system! To help an AI agent code this Tibetan astrological calculation system robustly and systematically, I've prepared a full documentation guide. This guide breaks down each subsystem, detailing inputs, processing logic, outputs, and considerations for robustness and various output formats.

## AI Agent Coding Documentation: Tibetan Astrological Calculation System

**Based on "算命系统设计.docx" [1]**

### I. System Overview

**Purpose:** To calculate an individual's astrological profile based on their birth year and current year information, identify potential obstacles, provide interpretations, and offer solutions, according to a specific Tibetan "Nine Palaces Outer Calculation" (九宫外算) system. A "Prosperity Assessment" feature is also envisioned.

**High-Level Architecture:** The system is composed of the following main subsystems:
1.  **Subsystem 1: Animal Sign and Element Calculation (天干地支系统)**: Determines the user's 60-cycle astrological sign from their birth year.
2.  **Subsystem 2: Animal Sign to Mewa (Nine Palaces) Conversion (九宫转换系统)**: Converts the 60-cycle sign into three Mewa numbers (Life, Body, Power).
3.  **Subsystem 3: Mewa Interpretation - Obstacle System (障碍解读系统)**: Identifies and interprets four types of obstacles based on the user's Mewas and current year data.
4.  **(Future/Optional) Subsystem 4: Prosperity Assessment (兴盛鉴)**: Assesses various life events.

### II. Core Data Structures and Constants

The AI agent should pre-define or have access to the following data structures:

1.  **Animals (生肖 - Shēngxiào):**
    *   Array/List: ``
    *   Indices for `n mod 12` calculation (e.g., Rat might be 4 if 1984 mod 12 = 4, adjust as per document's base year or provide a mapping). The document implies a direct `n mod 12` mapping where the resulting index corresponds to the list above. Ensure the starting point of the cycle (e.g., which animal is 0 or 1) is consistently handled. The document states "鼠 - 牛 - 虎 - 兔 - 龙 - 蛇 - 马 - 羊 - 猴 - 鸡 - 狗 - 猪" and for `n mod 12` gives "木阳鼠" for 1984 (1984 mod 12 = 4). This suggests Rat is index 4.
        *   `ANIMAL_SIGNS = {0: "猴 (Monkey)", 1: "鸡 (Rooster)", 2: "狗 (Dog)", 3: "猪 (Pig)", 4: "鼠 (Rat)", 5: "牛 (Ox)", 6: "虎 (Tiger)", 7: "兔 (Rabbit)", 8: "龙 (Dragon)", 9: "蛇 (Snake)", 10: "马 (Horse)", 11: "羊 (Sheep)"}` (Example mapping if 1980 is Monkey, index 0)
        *   *Correction based on document [1]:* "年份 n 转属相： 12 种 = n mod 12". Example: 1990 (马 Horse). 1990 mod 12 = 10. So, Horse is index 10.
            `ANIMAL_SIGNS_BY_MOD_12 = {0: "猴 (Monkey)", 1: "鸡 (Rooster)",..., 4: "鼠 (Rat)",..., 10: "马 (Horse)",...}`.
            The document lists animals sequentially. Let's assume a standard sequence starting with Rat as 0 for modulo purposes if a base year isn't explicitly used for `n mod 12`'s 0-index. However, the document uses `n mod 12` directly. For 1984 (Rat), 1984 mod 12 = 4. For 1985 (Ox), 1985 mod 12 = 5. This implies:
            `ANIMAL_SIGNS_MOD_12_MAP = {4:"鼠 (Rat)", 5:"牛 (Ox)", 6:"虎 (Tiger)", 7:"兔 (Rabbit)", 8:"龙 (Dragon)", 9:"蛇 (Snake)", 10:"马 (Horse)", 11:"羊 (Sheep)", 0:"猴 (Monkey)", 1:"鸡 (Rooster)", 2:"狗 (Dog)", 3:"猪 (Pig)"}`

2.  **Elements (五行 - Wǔxíng):**
    *   Array/List: `["木 (Wood)", "火 (Fire)", "土 (Earth)", "金 (Metal)", "水 (Water)"]`

3.  **Yin/Yang (阴阳):**
    *   Array/List: `["阳 (Yang)", "阴 (Yin)"]`
    *   Mapping to Animals: `YANG_ANIMALS =`, `YIN_ANIMALS =`

4.  **Ten Heavenly Stems Combinations (天干 - Tiāngān derived):**
    *   A mapping for `n mod 10` to Element and Yin/Yang. The document states "10 组合对应 = n mod 10" and "每 2 个属相用同一个元素".
    *   The 60-cycle output "木阳鼠 - 木阴牛 - 火阳虎 - 火阴兔..." implies a sequence.
        *   `TIANGAN_MAP_MOD_10 = {`
            `4: {"element": "木 (Wood)", "yin_yang": "阳 (Yang)"}, // Corresponds to 甲 (Jia) - e.g., 1984 mod 10 = 4`
            `5: {"element": "木 (Wood)", "yin_yang": "阴 (Yin)"},   // Corresponds to 乙 (Yi)  - e.g., 1985 mod 10 = 5`
            `6: {"element": "火 (Fire)", "yin_yang": "阳 (Yang)"}, // Corresponds to 丙 (Bing) - e.g., 1986 mod 10 = 6`
            `7: {"element": "火 (Fire)", "yin_yang": "阴 (Yin)"},   // Corresponds to 丁 (Ding)`
            `8: {"element": "土 (Earth)", "yin_yang": "阳 (Yang)"}, // Corresponds to 戊 (Wu)`
            `9: {"element": "土 (Earth)", "yin_yang": "阴 (Yin)"},   // Corresponds to 己 (Ji)`
            `0: {"element": "金 (Metal)", "yin_yang": "阳 (Yang)"}, // Corresponds to 庚 (Geng) - e.g., 1990 mod 10 = 0`
            `1: {"element": "金 (Metal)", "yin_yang": "阴 (Yin)"},   // Corresponds to 辛 (Xin)`
            `2: {"element": "水 (Water)", "yin_yang": "阳 (Yang)"}, // Corresponds to 壬 (Ren)`
            `3: {"element": "水 (Water)", "yin_yang": "阴 (Yin)"}    // Corresponds to 癸 (Gui)`
            `}`

5.  **Mewa Numbers (九宫数字 - Jiǔgōng Shùzì):**
    *   Integers 1 through 9.

6.  **Mewa-Color Mapping (数字-颜色对应系统):**
    *   Dictionary:
        `MEWA_COLORS = {`
        `1: "白 (White)", 2: "黑 (Black)", 3: "蓝 (Blue)", 4: "绿 (Green)", 5: "黄 (Yellow)",`
        `6: "白 (White)", 7: "红 (Red)", 8: "白 (White)", 9: "红 (Red)"`
        `}`

7.  **Mewa-Color-Element Mapping (Implied):**
    *   This can be derived from Mewa-Color and standard Element-Color associations if needed, though the document primarily uses color for BO and element (derived from color) for DO.
        `MEWA_ELEMENTS = {`
        `1: "金 (Metal)",  // White`
        `2: "水 (Water)",  // Black`
        `3: "水 (Water)",  // Blue (document implies, traditional sources confirm)`
        `4: "木 (Wood)",   // Green`
        `5: "土 (Earth)",  // Yellow`
        `6: "金 (Metal)",  // White`
        `7: "火 (Fire)",   // Red`
        `8: "金 (Metal)",  // White (document has 8 Red for official in RO, but Mewa color is 8 White)`
        `9: "火 (Fire)"    // Red`
        `}`
    *   *Clarification:* For DO, element is derived from the Mewa number's color. For RO, the "Darkness Body Mewa" itself has a color (e.g., "1白").

8.  **Sixty-Cycle Combinations (六十甲子 - Liùshí Jiǎzǐ):**
    *   An ordered list of the 60 combinations (e.g., "木阳鼠", "木阴牛",..., "水阴猪"). This is crucial for the "轮流制" (Rotation System) in Subsystem 2.
    *   `SIXTY_CYCLE_NAMES = ["木阳鼠", "木阴牛", "火阳虎", "火阴兔",... , "水阳狗", "水阴猪"]` (This list needs to be fully generated or accessible).

9.  **Mewa Rotation Mapping for Subsystem 2 (轮流对应系统):**
    *   This requires three lists/dictionaries, each mapping the 60 cycle names to a Mewa number (1-9) following a reversed sequence (9, 8,..., 1).
    *   `LIFE_MEWA_ROTATION = {"木阳鼠": 1, "木阴牛": 9, "火阳虎": 8,..., "水阳狗": 6, "水阴猪": 5}`
    *   `BODY_MEWA_ROTATION = {"木阳鼠": 4, "水阴牛": 3, "火阳虎": 2,..., "水阳狗": 9, "水阴猪": 8}` (Note: "水阴牛" in doc is likely a typo for "木阴牛" to maintain sequence)
    *   `POWER_MEWA_ROTATION = {"木阳鼠": 7, "水阴牛": 6, "火阳虎": 5,..., "水阳狗": 3, "水阴猪": 2}` (Same typo note)
    *   **Action for AI Agent:** These three mappings need to be fully populated based on the "轮流制" (rotation) and the reversed 9-1 sequence for all 60 combinations. If the full list isn't in the doc, the pattern must be extrapolated. The pattern is: for each of Life, Body, Power, take the 60 cycle names in order. Assign Mewa numbers starting from a specific Mewa for the first animal (e.g. 木阳鼠) and then decrement (9,8,7,6,5,4,3,2,1,9,8...) for subsequent animals in the 60-cycle. The starting Mewa for Life, Body, Power for "木阳鼠" are 1, 4, 7 respectively.

10. **Darkness Body Mewa (黑暗性体格) for Regional Obstacle (RO):**
    *   Dictionary mapping age/profession to a Mewa number:
        `DARKNESS_BODY_MEWA = {`
        `"9_under": 1,       // 9岁以下 ---1 白`
        `"9_18": 3,          // 9-18岁 --- 3 靛 (Indigo/Blue)`
        `"male_19_over": 2,  // 19岁以上, 男 --- 2 黑`
        `"sex_worker_19_over": 4, // 19岁以上, 性工作者 --- 4 绿`
        `"monastic_19_over": 5, // 19岁以上, 出家人 --- 5 黄`
        `"lay_practitioner_19_over": 6, // 19岁以上, 居家士བེན་པོ། ---6 白`
        `"female_19_over": 7, // 19岁以上, 女 --- 7 红`
        `"official_19_over": 8, // 19岁以上, 官员 ---8 红`
        `"elderly_60_over": 9 // 19岁以上, 老年人（60岁以上） --- 9 红`
        `}`
    *   Note: The "19岁以上" is a general category, with sub-categories. Logic will need to handle precedence (e.g., an elderly official). Assume the most specific category applies. "老年人（60岁以上）" likely overrides other 19+ categories if age is 60+.

11. **Obstacle Interpretations and Solutions (障碍阐释和-解决方案):**
    *   Structured data (e.g., nested dictionaries) for each obstacle type and its specific conditions/colors.
    *   `OBSTACLE_INTERPRETATIONS = {`
        `"RO": {"condition_met": "疾病、盗窃、遇一类遇事不顺的非人 (disease, being stolen, meeting with obstacles creating and undesired)"},`
        `"HO": {"condition_met": "powerful ghost of hunting (Tsen) come to home"},`
        `"BO": {`
        `"黑 (Black)": "meeting with demon (dud) —— 心神不安 (unease of mind)",`
        `"蓝 (Blue)": "meeting with ghost (Dre) —— 疾病 (内) (illness - internal)",`
        `"绿 (Green)": "meeting with dragon (lu) — — 疾病 (皮肤病) (illness - skin disease)",`
        `"黄 (Yellow)": "meeting with hunting ghost (ngur tsen) and land-owner (房屋不稳 生意不顺) (unstable house, business not smooth)",`
        `"红 (Red)": "contention of mouth and tongue"`
        `},`
        `"DO": {`
        `"element_clash": "人畜均衰、不兴旺 (decline for people and livestock, not prosperous)",`
        `"three_colors_same": {`
        `"白 (White)": "护法神逃逸，（需强化守护、安魂）(guardian spirits flee, need to strengthen protection, pacify soul)",`
        `"蓝 (Blue)": "口舌之争与水灾 (disputes and water disasters)",`
        `"绿 (Green)": "meeting with dragon (lu) —— 皮肤病 不宜动土 (skin disease, not suitable to break ground)",`
        `"黄 (Yellow)": "powerful ghost of hunting (Tsen)",`
        `"红 (Red)": "伤患 能量过低 (injury/illness, low energy)"`
        `}`
        `}`
        `}`

12. **Five Elements Destructive Cycle (五行相克 - Wǔxíng Xiāngkè):**
    *   `ELEMENT_CLASH_MAP = {`
        `"木 (Wood)": "土 (Earth)",`
        `"火 (Fire)": "金 (Metal)",`
        `"土 (Earth)": "水 (Water)",`
        `"金 (Metal)": "木 (Wood)",`
        `"水 (Water)": "火 (Fire)"`
        `}`

### III. Subsystem 1: Animal Sign and Element Calculation

**Purpose:** To determine the user's 60-cycle Animal-Element-Yin/Yang combination and Rabjung number from their Gregorian birth year.

**Inputs:**
1.  `gregorian_birth_year` (Integer, e.g., 1990).
2.  **(Optional but Recommended for Accuracy)** `tibetan_new_year_date_for_birth_year` (String or Date object, e.g., "YYYY-MM-DD"). If not provided, the system might assume the Gregorian year directly corresponds, or use a lookup table for Losar/Chinese New Year dates. The document mentions "日 --- 新年什么时候" [1], indicating this is a consideration.
    *   **Robustness:** If `tibetan_new_year_date_for_birth_year` is used, the input `gregorian_birth_date` (full date) would be needed to determine if the birth occurred before or after the Tibetan New Year in that Gregorian year. For simplicity, the current documentation follows the `n mod X` logic which seems to use the Gregorian year directly.

**Processing Logic:**
1.  Let `n = gregorian_birth_year`.
2.  **Calculate Rabjung (饶迥 - Ráojiǒng) Number (`m`):**
    *   Formula: `m = (n + 3 - 1026) mod 60`.[1]
    *   The result `m` is a number within the 60-year cycle. (Note: Rabjung itself is a 60-year *cycle period*, e.g., 17th Rabjung. The `m` here seems to be the position *within* a Rabjung cycle, or a direct 60-cycle identifier). The document is a bit ambiguous if `m` is the cycle number (like 1st, 2nd.. 17th Rabjung) or the year number within the 60-year sequence (1 to 60). Given `mod 60`, it's likely the year number within the sequence.
3.  **Determine Animal Sign (子集 A - 12 属相):**
    *   Formula: `animal_mod = n mod 12`.[1]
    *   `animal_sign = ANIMAL_SIGNS_MOD_12_MAP[animal_mod]`.
4.  **Determine Element and Yin/Yang (子集 B & C - 天干 derived):**
    *   Formula: `tiangan_mod = n mod 10`.[1]
    *   `element = TIANGAN_MAP_MOD_10[tiangan_mod]["element"]`.
    *   `yin_yang_from_tiangan = TIANGAN_MAP_MOD_10[tiangan_mod]["yin_yang"]`.
    *   **Consistency Check (Optional but good):** The document also states Yin/Yang can be derived from the animal: "阴阳配属相即可".[1]
        *   `yin_yang_from_animal = "阳 (Yang)" if animal_sign in YANG_ANIMALS else "阴 (Yin)"`.
        *   The AI agent should verify if `yin_yang_from_tiangan` and `yin_yang_from_animal` are consistent. Traditional Chinese astrology ensures this consistency in the 60-year cycle (Yang Heavenly Stems pair with Yang Earthly Branches). The provided `TIANGAN_MAP_MOD_10` and `ANIMAL_SIGNS_MOD_12_MAP` should inherently maintain this. Use `yin_yang_from_tiangan` as the primary, as it's part of the "天干" (Heavenly Stem) concept.
5.  **Form Combined 60-Cycle Name (输出组合结果):**
    *   `combined_name = element + yin_yang_from_tiangan + animal_sign` (e.g., "木阳鼠"). This name should match one of the entries in the `SIXTY_CYCLE_NAMES` list.

**Outputs:**
*   A structured object/dictionary, e.g.:
    ```json
    {
      "gregorian_birth_year": 1990,
      "rabjung_identifier_m": 47, // (1990+3-1026) mod 60 = 967 mod 60 = 7 (if 1026 is base for 0) or 1990 -> 庚午 (Geng Wu) which is 7th in cycle if JiaZi is 1. (1990+3-1026) mod 60 = 967 mod 60 = 7.  The document example for 1990 is 金阳马.
      "animal_sign": "马 (Horse)",
      "element": "金 (Metal)",
      "yin_yang": "阳 (Yang)",
      "sixty_cycle_name": "金阳马 (Metal-Yang-Horse)"
    }
    ```
    *Note on Rabjung `m`: The formula `(y+3-1026)mod60` implies 1027 (Fire-Hare) is year `m=4` in the cycle (1027+3-1026 = 4). The first year of the first Rabjung is 1027. If `m` is meant to be the index from 0-59, then `(y - 1027) mod 60` might be more direct if 1027 is index 0 of its cycle. Or `(y - (1027 - offset_for_first_year_of_cycle)) mod 60`. The document's formula is `(y+3-1026) mod 60`. Let's stick to this. For y=1984, m = (1984+3-1026)mod60 = 961 mod 60 = 1. For y=1990, m = (1990+3-1026)mod60 = 967 mod 60 = 7.*

**Robustness & Error Handling:**
*   Validate `gregorian_birth_year` (e.g., must be a reasonable integer, perhaps within a supported range like 1900-2100).
*   Handle potential discrepancies if `tibetan_new_year_date_for_birth_year` is implemented (ensure date parsing is robust).

### IV. Subsystem 2: Animal Sign to Mewa (Nine Palaces) Conversion

**Purpose:** To convert the 60-cycle sign (output from Subsystem 1) into three Mewa numbers: Life Mewa (命格), Body Mewa (体格), and Power Mewa (权格).

**Inputs:**
1.  `sixty_cycle_name` (String, e.g., "金阳马", from Subsystem 1).

**Processing Logic:**

**Method 1: Rotation System (轮流制)** [1]
1.  `life_mewa_number = LIFE_MEWA_ROTATION[sixty_cycle_name]`
2.  `body_mewa_number = BODY_MEWA_ROTATION[sixty_cycle_name]`
3.  `power_mewa_number = POWER_MEWA_ROTATION[sixty_cycle_name]`
    *   **Note:** The `LIFE_MEWA_ROTATION`, `BODY_MEWA_ROTATION`, `POWER_MEWA_ROTATION` lookup tables must be fully populated for all 60 cycle names, following the "倒转 9-8-7-6-5-4-3-2-1" (reversed sequence) pattern starting from the Mewa numbers given for "木阳鼠" (1 for Life, 4 for Body, 7 for Power).

**Method 2: Alternative Algorithm (另外一种算法)** [1]
1.  First, determine `life_mewa_number` using the Rotation System as above:
    `life_mewa_number = LIFE_MEWA_ROTATION[sixty_cycle_name]`
2.  Calculate `body_mewa_number`:
    *   `temp_body_mewa = life_mewa_number + 3`
    *   `body_mewa_number = temp_body_mewa if temp_body_mewa <= 9 else temp_body_mewa - 9` (cyclical 1-9).
3.  Calculate `power_mewa_number`:
    *   `temp_power_mewa = body_mewa_number + 3`
    *   `power_mewa_number = temp_power_mewa if temp_power_mewa <= 9 else temp_power_mewa - 9` (cyclical 1-9).

*   **AI Agent Choice:** The document presents both. The "另外一种算法" seems to be a derivation or simplification that should yield the same results as the full rotation tables if those tables are constructed correctly using the "+3" logic for Body and Power relative to Life's rotated value. The agent should ideally implement the full rotation tables first. If there's ambiguity in constructing the full tables, the "+3" method for Body/Power (once Life Mewa is found via its specific rotation) is more explicit. The document implies the "+3" rule should match the full rotation examples.

**Determine Colors:**
1.  `life_mewa_color = MEWA_COLORS[life_mewa_number]`
2.  `body_mewa_color = MEWA_COLORS[body_mewa_number]`
3.  `power_mewa_color = MEWA_COLORS[power_mewa_number]`

**Outputs:**
*   A structured object/dictionary, e.g.:
    ```json
    {
      "life_mewa": {"number": 1, "color": "白 (White)"},
      "body_mewa": {"number": 4, "color": "绿 (Green)"},
      "power_mewa": {"number": 7, "color": "红 (Red)"}
    }
    ```

**Robustness & Error Handling:**
*   Ensure `sixty_cycle_name` is valid and exists as a key in the rotation mapping tables.
*   Handle potential errors if Mewa numbers fall outside 1-9 (though the logic should prevent this).

### V. Subsystem 3: Mewa Interpretation - Obstacle System

**Purpose:** To identify and interpret four types of obstacles based on the user's calculated Mewas (from Subsystem 2), current year information, and user demographics.

**Inputs:**
1.  `user_mewas`: The output from Subsystem 2 (containing Life, Body, Power Mewa numbers and colors).
2.  `current_gregorian_year` (Integer, e.g., 2025).
3.  `user_age` (Integer).
4.  `user_gender` (String, e.g., "male", "female").
5.  `user_profession_or_status` (String, e.g., "sex_worker", "monastic", "lay_practitioner", "official", or "general" if none apply specifically for RO).

**Processing Logic:**

**Step 1: Calculate Current Year's Astrological Profile (specifically Body Mewa)**
1.  Use Subsystem 1 with `current_gregorian_year` to get the `current_year_sixty_cycle_name`.
2.  Use Subsystem 2 (specifically the Body Mewa calculation part, either Rotation or LifeMewa+3) with `current_year_sixty_cycle_name` to get `current_year_body_mewa_number` and `current_year_body_mewa_color`.
    *   Let `current_year_body_mewa_element = MEWA_ELEMENTS[current_year_body_mewa_number]`.
    *   Let `user_body_mewa_number = user_mewas["body_mewa"]["number"]`.
    *   Let `user_body_mewa_color = user_mewas["body_mewa"]["color"]`.
    *   Let `user_body_mewa_element = MEWA_ELEMENTS[user_body_mewa_number]`.

**Step 2: Obstacle Matching (二元制 o/x - success (no obstacle) = o, failure (obstacle) = x)**
The document states "输入是 ‘体格’ 匹配机制" (input is 'Body Mewa' matching mechanism) for the premise.

1.  **Regional Obstacle (RO - 方位障碍):**
    *   Determine the applicable `darkness_mewa_key` based on `user_age`, `user_gender`, `user_profession_or_status`.
        *   If `user_age < 9`, key is `"9_under"`.
        *   Else if `user_age >= 9 && user_age <= 18`, key is `"9_18"`.
        *   Else if `user_age >= 19`:
            *   If `user_age >= 60`, key is `"elderly_60_over"`.
            *   Else if `user_profession_or_status == "official"`, key is `"official_19_over"`.
            *   Else if `user_gender == "female"`:
                *   If `user_profession_or_status == "sex_worker"`, key is `"sex_worker_19_over"`.
                *   Else, key is `"female_19_over"`.
            *   Else if `user_gender == "male"`:
                *   If `user_profession_or_status == "monastic"`, key is `"monastic_19_over"`.
                *   Else if `user_profession_or_status == "lay_practitioner"`, key is `"lay_practitioner_19_over"`.
                *   Else, key is `"male_19_over"`.
    *   `target_darkness_mewa = DARKNESS_BODY_MEWA[darkness_mewa_key]` (if key exists).
    *   `is_ro_obstacle = (current_year_body_mewa_number == target_darkness_mewa)`.

2.  **Home Obstacle (HO - 家庭障碍):**
    *   Tibetan: `བསྐོར་སྨེ་གནམ་ལོའི་ལུས་སྨེར་བབ་པ།` (Current year's cycle Mewa falls upon one's own Body Mewa).
    *   `is_ho_obstacle = (current_year_body_mewa_number == user_body_mewa_number)`.

3.  **Bedding Obstacle (BO - 卧床障碍):**
    *   `is_bo_obstacle = (current_year_body_mewa_color == user_body_mewa_color)`.

4.  **Door Obstacle (DO - 门户障碍):**
    *   **Condition 1 (Element Clash):**
        *   `clash1 = (ELEMENT_CLASH_MAP[current_year_body_mewa_element] == user_body_mewa_element)`
        *   `clash2 = (ELEMENT_CLASH_MAP[user_body_mewa_element] == current_year_body_mewa_element)`
        *   `is_do_element_clash = clash1 or clash2`.
        *   The document also mentions "红蓝相遇" (Red-Blue meet) as an example. Red is Fire, Blue is Water. Water clashes Fire. This is covered by the general element clash.
    *   **Condition 2 (Three 格 Colors Same):**
        *   `user_life_color = user_mewas["life_mewa"]["color"]`
        *   `user_body_color = user_mewas["body_mewa"]["color"]`
        *   `user_power_color = user_mewas["power_mewa"]["color"]`
        *   `is_do_three_colors_same = (user_life_color == user_body_color && user_body_color == user_power_color)`.
    *   `is_do_obstacle = is_do_element_clash or is_do_three_colors_same`.

**Step 3: Get Interpretations and Solutions**
*   For each obstacle type where `is_X_obstacle` is true:
    *   If RO: `interpretation = OBSTACLE_INTERPRETATIONS["condition_met"]`.
    *   If HO: `interpretation = OBSTACLE_INTERPRETATIONS["HO"]["condition_met"]`.
    *   If BO: `interpretation = OBSTACLE_INTERPRETATIONS[user_body_mewa_color]` (Interpretation depends on the user's body Mewa color when the BO condition is met).
    *   If DO:
        *   If `is_do_element_clash`: `interpretation_clash = OBSTACLE_INTERPRETATIONS["element_clash"]`.
        *   If `is_do_three_colors_same`: `interpretation_3col = OBSTACLE_INTERPRETATIONS["three_colors_same"][user_life_color]` (Interpretation depends on the common color).
        *   Combine interpretations if both DO conditions are met.

**Outputs:**
*   A list of identified obstacles, each with its name, interpretation, and any specific conditional details.
    ```json
    {
      "obstacles_found":
    }
    ```

**Robustness & Error Handling:**
*   Validate `user_age` (e.g., non-negative).
*   Handle `user_gender` and `user_profession_or_status` with clear enumeration or case-insensitivity. Provide a default for profession if not applicable.
*   Ensure all Mewa numbers/colors used as keys in `OBSTACLE_INTERPRETATIONS` are valid.
*   Gracefully handle cases where a `darkness_mewa_key` might not be found (though the logic should cover all specified cases).

### VI. Prosperity Assessment (兴盛鉴 - Xīngshèng Jiàn)

**Purpose:** To assess the auspiciousness of various life events.

**Inputs (Tentative, based on sparse information "五行体系 + 时辰属相" [1]):**
1.  `event_type` (String from a predefined list: "屠杀 (Massacre)", "怀孕 (Pregnancy)", "成年 (Adulthood)", "生辰 (Birthday)", "洗礼 (Baptism)", "着衣 (Wearing new clothes)", "行事 (Undertaking activities)", "盛 (Prosperity)", "衰 (Decline)", "病 (Sickness)", "死 (Death)", "殡葬 (Funeral)").
2.  `event_date` (String or Date object, "YYYY-MM-DD").
3.  `event_hour_animal_sign` (String, e.g., "鼠 (Rat)"). This implies the user needs to know or input the animal sign for the specific 2-hour period of the event.
    *   A helper function to determine `event_hour_animal_sign` from `event_date` and `event_time` (HH:MM) would be useful. (Standard Chinese astrological hours: 23-01 Rat, 01-03 Ox, etc.)

**Processing Logic:**
*   The document [1] is very brief: "（五行体系 + 时辰属相）".
*   This suggests a rules-based system where:
    1.  The `event_type` is the primary factor.
    2.  The Five Element interactions (相生 xiāngshēng - generative, 相克 xiāngkè - destructive) between:
        *   The element of the `event_date` (derived via Subsystem 1).
        *   The element of the `event_hour_animal_sign` (each animal has an intrinsic element).
        *   Possibly the user's own natal elements (from Subsystem 1).
    3.  The relationship between the `event_hour_animal_sign` and:
        *   The animal sign of the `event_date`.
        *   The user's natal animal sign.
*   **AI Agent Action:** This subsystem requires significant further specification or access to traditional texts detailing these rules. For now, the agent can create a placeholder structure. If specific rules are found, they would be implemented here (e.g., "For 'Marriage' event, if day element 'Wood' nourishes hour element 'Fire', it is auspicious").

**Outputs (Tentative):**
*   An assessment string (e.g., "Auspicious", "Inauspicious", "Neutral") and perhaps a brief explanation.
    ```json
    {
      "event_type": "着衣 (Wearing new clothes)",
      "assessment": "Auspicious",
      "reasoning": "Day element Wood generates Hour element Fire, Hour animal Rat is compatible with Day animal Dragon."
    }
    ```

**Robustness & Error Handling:**
*   Validate `event_type` against the predefined list.
*   Robust date/time parsing for `event_date` and deriving `event_hour_animal_sign`.

### VII. General Implementation Guidelines

1.  **Modularity:** Implement each subsystem as a separate module/class with clear interfaces.
2.  **Configuration:** Store constants (animal lists, color maps, etc.) in configurable files or at the top of modules for easy modification.
3.  **Immutability:** Use immutable data structures where possible for inputs and outputs of functions to prevent side effects.
4.  **Logging:** Implement logging for debugging and tracing calculations, especially for complex rule-based logic.
5.  **Testing:**
    *   Unit tests for each calculation step (e.g., `n mod 12`, Mewa rotation, element clashes).
    *   Integration tests for each subsystem.
    *   Use the examples provided in the document [1] as test cases (e.g., 木阳鼠 -> Life 1, Body 4, Power 7).
6.  **Localization/Internationalization (i18n/l10n):**
    *   The current system uses Chinese characters for names and interpretations. If multiple languages are required, abstract these strings into resource files.
7.  **Tibetan New Year Precision:**
    *   For higher accuracy, especially for Subsystem 1, the exact date of the Tibetan New Year (Losar) or Chinese New Year for the given Gregorian year should be used to determine if a birth date falls into the previous or current Tibetan/Chinese year. This often involves a lookup table or a more complex calendrical algorithm. The current spec uses `n mod X` which simplifies this by likely using the Gregorian year directly. This simplification should be documented if chosen.

### VIII. API Design (Example)

If the system is to be exposed as an API (e.g., RESTful JSON API):

**Endpoints:**

1.  `POST /calculate/full_profile`
    *   **Request Body:**
        ```json
        {
          "gregorian_birth_year": 1990,
          "current_gregorian_year": 2025,
          "user_age": 35,
          "user_gender": "male", // e.g., "male", "female"
          "user_profession_or_status": "general" // e.g., "official", "monastic", etc.
        }
        ```
    *   **Response Body (Success 200 OK):**
        ```json
        {
          "user_profile": { // Output from Subsystem 1
            "gregorian_birth_year": 1990,
            "rabjung_identifier_m": 7,
            "animal_sign": "马 (Horse)",
            "element": "金 (Metal)",
            "yin_yang": "阳 (Yang)",
            "sixty_cycle_name": "金阳马 (Metal-Yang-Horse)"
          },
          "user_mewas": { // Output from Subsystem 2
            "life_mewa": {"number": 1, "color": "白 (White)"},
            "body_mewa": {"number": 4, "color": "绿 (Green)"},
            "power_mewa": {"number": 7, "color": "红 (Red)"}
          },
          "obstacle_analysis": { // Output from Subsystem 3
            "current_year_profile": {
              "sixty_cycle_name": "乙巳 (Wood-Yin-Snake)", // Example
              "body_mewa": {"number": 2, "color": "黑 (Black)", "element": "水 (Water)"}
            },
            "obstacles_found":
          }
        }
        ```
    *   **Response Body (Error 400 Bad Request, 500 Internal Server Error):**
        ```json
        {
          "error": "Invalid input: gregorian_birth_year must be an integer."
        }
        ```

2.  `POST /calculate/prosperity_assessment` (If Subsystem 4 is implemented)
    *   **Request Body:**
        ```json
        {
          "event_type": "着衣 (Wearing new clothes)",
          "event_date_time": "2025-07-15T10:00:00" // ISO 8601 format
          // Optionally, user's natal data can be included or fetched if needed by rules
        }
        ```
    *   **Response Body (Success 200 OK):**
        ```json
        { // Output from Subsystem 4
          "event_type": "着衣 (Wearing new clothes)",
          "assessment": "Auspicious",
          "reasoning": "..."
        }
        ```

### IX. Direct Output Formats

For direct output (e.g., console application, webpage display):

*   **Human-Readable Text:**
    *   Present information clearly section by section.
    *   Use descriptive labels.
    *   Example:
        Tibetan Astrological Profile
        -----------------------------
        Birth Year: 1990
        Astrological Sign: 金阳马 (Metal-Yang-Horse)
        Rabjung Identifier (m): 7

        Mewa Numbers:
          Life Mewa: 1 白 (White)
          Body Mewa: 4 绿 (Green)
          Power Mewa: 7 红 (Red)

        Obstacle Analysis for Current Year 2025:
        ---------------------------------------
        Current Year is Wood-Yin-Snake, Body Mewa is 2 黑 (Black) - 水 (Water)

        * Regional Obstacle: YES
          - Interpretation: 疾病、盗窃、遇一类遇事不顺的非人
          - Reason: Current Year Body Mewa (2) matched your Darkness Body Mewa (2 for Male 19+).

        * Home Obstacle: NO
          - Reason: Current Year Body Mewa (2) does not match your Body Mewa (4).

       ... and so on for other obstacles.
*   **HTML Web Page:**
    *   Use semantic HTML for structure.
    *   CSS for styling (e.g., using colors associated with Mewas).
    *   JavaScript for interactivity if needed (e.g., allowing users to input data).
*   **Considerations for Tibetan Script:** If outputting Tibetan script (like `བསྐོར་སྨེ།`), ensure the environment supports Unicode and has appropriate Tibetan fonts.

This comprehensive guide should provide a solid foundation for the AI agent to develop the Tibetan astrological calculation system in a structured and robust manner. The key will be careful implementation of the lookup tables and the conditional logic for obstacles.