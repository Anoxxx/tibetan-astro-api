#!/usr/bin/env python3
"""
Tibetan Astrological Calculation System - Core Engine
Based on the Nine Palaces Outer Calculation (九宫外算) system

This module provides the main calculation functions for:
- Subsystem 1: Animal Sign and Element Calculation
- Subsystem 2: Mewa (Nine Palaces) Conversion
- Subsystem 3: Obstacle Analysis
- Subsystem 4: Prosperity Assessment
"""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, date
import json

import tibetan_astro_tables as tables

# Import all constants 
ANIMAL_SIGNS_MOD_12_MAP = tables.ANIMAL_SIGNS_MOD_12_MAP
TIANGAN_MAP_MOD_10 = tables.TIANGAN_MAP_MOD_10
SIXTY_CYCLE_NAMES = tables.SIXTY_CYCLE_NAMES
LIFE_MEWA_ROTATION = tables.LIFE_MEWA_ROTATION
BODY_MEWA_ROTATION = tables.BODY_MEWA_ROTATION
POWER_MEWA_ROTATION = tables.POWER_MEWA_ROTATION
MEWA_COLORS = tables.MEWA_COLORS
MEWA_ELEMENTS = tables.MEWA_ELEMENTS
DARKNESS_BODY_MEWA = tables.DARKNESS_BODY_MEWA
ELEMENT_CLASH_MAP = tables.ELEMENT_CLASH_MAP
OBSTACLE_INTERPRETATIONS = tables.OBSTACLE_INTERPRETATIONS
PROSPERITY_EVENT_TYPES = tables.PROSPERITY_EVENT_TYPES
HOUR_ANIMAL_MAP = tables.HOUR_ANIMAL_MAP
ANIMAL_ELEMENT_MAP = tables.ANIMAL_ELEMENT_MAP
ELEMENT_GENERATE_MAP = tables.ELEMENT_GENERATE_MAP


class TibetanAstroCalculator:
    """Main calculator for Tibetan astrological calculations"""
    
    def __init__(self):
        self.version = "1.0.0"
    
    # =================================================================
    # SUBSYSTEM 1: Animal Sign and Element Calculation
    # =================================================================
    
    def calculate_astrological_profile(self, gregorian_year: int) -> Dict[str, Any]:
        """
        Calculate the 60-cycle astrological profile for a given Gregorian year.
        
        Args:
            gregorian_year: Gregorian year (e.g., 1990)
            
        Returns:
            Dictionary containing:
            - gregorian_year: Input year
            - rabjung_identifier_m: Rabjung cycle position
            - animal_sign: Animal sign
            - element: Element
            - yin_yang: Yin/Yang
            - sixty_cycle_name: Combined name (e.g., "金阳马")
        """
        if not isinstance(gregorian_year, int) or gregorian_year < 1000 or gregorian_year > 3000:
            raise ValueError("Gregorian year must be a valid integer between 1000 and 3000")
        
        n = gregorian_year
        
        # Calculate Rabjung identifier
        rabjung_m = (n + 3 - 1026) % 60
        
        # Determine animal sign
        animal_mod = n % 12
        animal_sign = ANIMAL_SIGNS_MOD_12_MAP[animal_mod]
        
        # Determine element and yin/yang from Tiangan
        tiangan_mod = n % 10
        tiangan_info = TIANGAN_MAP_MOD_10[tiangan_mod]
        element = tiangan_info["element"]
        yin_yang = tiangan_info["yin_yang"]
        
        # Form combined sixty-cycle name
        element_clean = element.split(' ')[0]  # "木 (Wood)" -> "木"
        yin_yang_clean = yin_yang.split(' ')[0]  # "阳 (Yang)" -> "阳"
        animal_clean = animal_sign.split(' ')[0]  # "鼠 (Rat)" -> "鼠"
        sixty_cycle_name = f"{element_clean}{yin_yang_clean}{animal_clean}"
        
        return {
            "gregorian_year": gregorian_year,
            "rabjung_identifier_m": rabjung_m,
            "animal_sign": animal_sign,
            "element": element,
            "yin_yang": yin_yang,
            "sixty_cycle_name": sixty_cycle_name
        }
    
    # =================================================================
    # SUBSYSTEM 2: Mewa (Nine Palaces) Conversion
    # =================================================================
    
    def calculate_mewa_numbers(self, sixty_cycle_name: str) -> Dict[str, Dict[str, Any]]:
        """
        Convert 60-cycle name to Life, Body, and Power Mewa numbers.
        
        Args:
            sixty_cycle_name: 60-cycle name (e.g., "金阳马")
            
        Returns:
            Dictionary containing life_mewa, body_mewa, power_mewa with number and color
        """
        if sixty_cycle_name not in LIFE_MEWA_ROTATION:
            raise ValueError(f"Invalid sixty_cycle_name: {sixty_cycle_name}")
        
        # Get Mewa numbers from rotation tables
        life_mewa_number = LIFE_MEWA_ROTATION[sixty_cycle_name]
        body_mewa_number = BODY_MEWA_ROTATION[sixty_cycle_name]
        power_mewa_number = POWER_MEWA_ROTATION[sixty_cycle_name]
        
        # Get corresponding colors
        life_mewa_color = MEWA_COLORS[life_mewa_number]
        body_mewa_color = MEWA_COLORS[body_mewa_number]
        power_mewa_color = MEWA_COLORS[power_mewa_number]
        
        # Get corresponding elements
        life_mewa_element = MEWA_ELEMENTS[life_mewa_number]
        body_mewa_element = MEWA_ELEMENTS[body_mewa_number]
        power_mewa_element = MEWA_ELEMENTS[power_mewa_number]
        
        return {
            "life_mewa": {
                "number": life_mewa_number,
                "color": life_mewa_color,
                "element": life_mewa_element
            },
            "body_mewa": {
                "number": body_mewa_number,
                "color": body_mewa_color,
                "element": body_mewa_element
            },
            "power_mewa": {
                "number": power_mewa_number,
                "color": power_mewa_color,
                "element": power_mewa_element
            }
        }
    
    def calculate_mewa_alternative_method(self, sixty_cycle_name: str) -> Dict[str, Dict[str, Any]]:
        """
        Alternative method: Calculate Body and Power Mewa using +3 rule from Life Mewa.
        
        Args:
            sixty_cycle_name: 60-cycle name (e.g., "金阳马")
            
        Returns:
            Same format as calculate_mewa_numbers()
        """
        if sixty_cycle_name not in LIFE_MEWA_ROTATION:
            raise ValueError(f"Invalid sixty_cycle_name: {sixty_cycle_name}")
        
        # Get Life Mewa from rotation table
        life_mewa_number = LIFE_MEWA_ROTATION[sixty_cycle_name]
        
        # Calculate Body Mewa: Life + 3 (cyclical 1-9)
        temp_body = life_mewa_number + 3
        body_mewa_number = temp_body if temp_body <= 9 else temp_body - 9
        
        # Calculate Power Mewa: Body + 3 (cyclical 1-9)
        temp_power = body_mewa_number + 3
        power_mewa_number = temp_power if temp_power <= 9 else temp_power - 9
        
        return {
            "life_mewa": {
                "number": life_mewa_number,
                "color": MEWA_COLORS[life_mewa_number],
                "element": MEWA_ELEMENTS[life_mewa_number]
            },
            "body_mewa": {
                "number": body_mewa_number,
                "color": MEWA_COLORS[body_mewa_number],
                "element": MEWA_ELEMENTS[body_mewa_number]
            },
            "power_mewa": {
                "number": power_mewa_number,
                "color": MEWA_COLORS[power_mewa_number],
                "element": MEWA_ELEMENTS[power_mewa_number]
            }
        }
    
    # =================================================================
    # SUBSYSTEM 3: Obstacle Analysis
    # =================================================================
    
    def determine_darkness_mewa_key(self, user_age: int, user_gender: str, 
                                   user_profession: str = "general") -> str:
        """
        Determine the appropriate darkness mewa key based on demographics.
        
        Args:
            user_age: User's age
            user_gender: "male" or "female"
            user_profession: Profession/status for special categories
            
        Returns:
            Key for DARKNESS_BODY_MEWA lookup
        """
        if user_age < 9:
            return "9_under"
        elif 9 <= user_age <= 18:
            return "9_18"
        elif user_age >= 19:
            if user_age >= 60:
                return "elderly_60_over"
            elif user_profession == "official":
                return "official_19_over"
            elif user_gender == "female":
                if user_profession == "sex_worker":
                    return "sex_worker_19_over"
                else:
                    return "female_19_over"
            elif user_gender == "male":
                if user_profession == "monastic":
                    return "monastic_19_over"
                elif user_profession == "lay_practitioner":
                    return "lay_practitioner_19_over"
                else:
                    return "male_19_over"
        
        # Default fallback
        return "male_19_over" if user_gender == "male" else "female_19_over"
    
    def analyze_obstacles(self, user_mewas: Dict[str, Dict[str, Any]], 
                         current_year: int, user_age: int, user_gender: str,
                         user_profession: str = "general") -> Dict[str, Any]:
        """
        Analyze four types of obstacles based on user's Mewas and current year.
        
        Args:
            user_mewas: Output from calculate_mewa_numbers()
            current_year: Current Gregorian year
            user_age: User's age
            user_gender: "male" or "female" 
            user_profession: User's profession/status
            
        Returns:
            Dictionary containing obstacle analysis results
        """
        # Calculate current year's astrological profile
        current_year_profile = self.calculate_astrological_profile(current_year)
        current_year_mewas = self.calculate_mewa_numbers(current_year_profile["sixty_cycle_name"])
        
        # Extract relevant values
        current_year_body_mewa = current_year_mewas["body_mewa"]
        user_body_mewa = user_mewas["body_mewa"]
        user_life_mewa = user_mewas["life_mewa"]
        user_power_mewa = user_mewas["power_mewa"]
        
        obstacles_found = []
        
        # 1. Regional Obstacle (RO)
        darkness_key = self.determine_darkness_mewa_key(user_age, user_gender, user_profession)
        target_darkness_mewa = DARKNESS_BODY_MEWA[darkness_key]
        is_ro_obstacle = (current_year_body_mewa["number"] == target_darkness_mewa)
        
        if is_ro_obstacle:
            obstacles_found.append({
                "type": "RO",
                "name": "Regional Obstacle (方位障碍)",
                "condition_met": True,
                "interpretation": OBSTACLE_INTERPRETATIONS["RO"]["condition_met"],
                "details": {
                    "current_year_body_mewa": current_year_body_mewa["number"],
                    "target_darkness_mewa": target_darkness_mewa,
                    "darkness_category": darkness_key
                }
            })
        
        # 2. Home Obstacle (HO)
        is_ho_obstacle = (current_year_body_mewa["number"] == user_body_mewa["number"])
        
        if is_ho_obstacle:
            obstacles_found.append({
                "type": "HO",
                "name": "Home Obstacle (家庭障碍)",
                "condition_met": True,
                "interpretation": OBSTACLE_INTERPRETATIONS["HO"]["condition_met"],
                "details": {
                    "current_year_body_mewa": current_year_body_mewa["number"],
                    "user_body_mewa": user_body_mewa["number"]
                }
            })
        
        # 3. Bedding Obstacle (BO)
        is_bo_obstacle = (current_year_body_mewa["color"] == user_body_mewa["color"])
        
        if is_bo_obstacle:
            color_key = user_body_mewa["color"]
            interpretation = OBSTACLE_INTERPRETATIONS["BO"].get(color_key, "Unknown color interpretation")
            obstacles_found.append({
                "type": "BO",
                "name": "Bedding Obstacle (卧床障碍)",
                "condition_met": True,
                "interpretation": interpretation,
                "details": {
                    "current_year_body_color": current_year_body_mewa["color"],
                    "user_body_color": user_body_mewa["color"]
                }
            })
        
        # 4. Door Obstacle (DO)
        current_year_body_element = current_year_body_mewa["element"]
        user_body_element = user_body_mewa["element"]
        
        # DO Condition 1: Element Clash
        clash1 = (ELEMENT_CLASH_MAP.get(current_year_body_element) == user_body_element)
        clash2 = (ELEMENT_CLASH_MAP.get(user_body_element) == current_year_body_element)
        is_do_element_clash = clash1 or clash2
        
        # DO Condition 2: Three Colors Same
        user_life_color = user_life_mewa["color"]
        user_body_color = user_body_mewa["color"]
        user_power_color = user_power_mewa["color"]
        is_do_three_colors_same = (user_life_color == user_body_color == user_power_color)
        
        is_do_obstacle = is_do_element_clash or is_do_three_colors_same
        
        if is_do_obstacle:
            do_interpretations = []
            do_details = {}
            
            if is_do_element_clash:
                do_interpretations.append(OBSTACLE_INTERPRETATIONS["DO"]["element_clash"])
                do_details["element_clash"] = {
                    "current_year_element": current_year_body_element,
                    "user_element": user_body_element,
                    "clash_direction": "current_destroys_user" if clash1 else "user_destroys_current"
                }
            
            if is_do_three_colors_same:
                common_color = user_life_color
                three_color_interpretation = OBSTACLE_INTERPRETATIONS["DO"]["three_colors_same"].get(
                    common_color, "Unknown color interpretation")
                do_interpretations.append(three_color_interpretation)
                do_details["three_colors_same"] = {
                    "common_color": common_color,
                    "life_color": user_life_color,
                    "body_color": user_body_color,
                    "power_color": user_power_color
                }
            
            obstacles_found.append({
                "type": "DO",
                "name": "Door Obstacle (门户障碍)",
                "condition_met": True,
                "interpretation": " | ".join(do_interpretations),
                "details": do_details
            })
        
        return {
            "current_year_profile": current_year_profile,
            "current_year_mewas": current_year_mewas,
            "obstacles_found": obstacles_found,
            "total_obstacles": len(obstacles_found),
            "obstacle_types_present": [obs["type"] for obs in obstacles_found]
        }
    
    # =================================================================
    # SUBSYSTEM 4: Prosperity Assessment
    # =================================================================
    
    def get_hour_animal_from_time(self, hour: int) -> str:
        """
        Get the animal sign for a given hour (0-23).
        
        Args:
            hour: Hour in 24-hour format (0-23)
            
        Returns:
            Animal sign for that hour period
        """
        if 0 <= hour <= 23:
            return HOUR_ANIMAL_MAP.get(hour, "鼠 (Rat)")  # Default to Rat if not found
        else:
            raise ValueError("Hour must be between 0 and 23")
    
    def assess_prosperity(self, event_type: str, event_date: date, event_hour: int,
                         user_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Assess the prosperity/auspiciousness of an event.
        
        Args:
            event_type: Type of event from PROSPERITY_EVENT_TYPES
            event_date: Date of the event
            event_hour: Hour of the event (0-23)
            user_profile: Optional user's astrological profile
            
        Returns:
            Dictionary containing prosperity assessment
        """
        if event_type not in PROSPERITY_EVENT_TYPES:
            raise ValueError(f"Event type must be one of: {PROSPERITY_EVENT_TYPES}")
        
        # Get event date's astrological profile
        event_profile = self.calculate_astrological_profile(event_date.year)
        event_mewas = self.calculate_mewa_numbers(event_profile["sixty_cycle_name"])
        
        # Get hour animal and its element
        hour_animal = self.get_hour_animal_from_time(event_hour)
        hour_element = ANIMAL_ELEMENT_MAP[hour_animal]
        
        # Get day element (from the day's profile)
        day_element = event_profile["element"]
        
        # Basic prosperity rules (simplified implementation)
        assessment_factors = []
        
        # Factor 1: Element relationship between day and hour
        if ELEMENT_GENERATE_MAP.get(day_element) == hour_element:
            assessment_factors.append("Day element generates Hour element (Auspicious)")
        elif ELEMENT_CLASH_MAP.get(day_element) == hour_element:
            assessment_factors.append("Day element clashes with Hour element (Inauspicious)")
        elif ELEMENT_GENERATE_MAP.get(hour_element) == day_element:
            assessment_factors.append("Hour element generates Day element (Moderately Auspicious)")
        else:
            assessment_factors.append("Neutral element relationship")
        
        # Factor 2: Event type considerations (simplified)
        positive_events = ["怀孕 (Pregnancy)", "成年 (Adulthood)", "生辰 (Birthday)", 
                          "洗礼 (Baptism)", "着衣 (Wearing new clothes)", "盛 (Prosperity)"]
        negative_events = ["屠杀 (Massacre)", "衰 (Decline)", "病 (Sickness)", "死 (Death)"]
        
        if event_type in positive_events:
            base_assessment = "Favorable"
        elif event_type in negative_events:
            base_assessment = "Unfavorable"
        else:
            base_assessment = "Neutral"
        
        # Combine factors for final assessment
        if "Auspicious" in assessment_factors[0] and base_assessment == "Favorable":
            final_assessment = "Highly Auspicious"
        elif "Inauspicious" in assessment_factors[0] or base_assessment == "Unfavorable":
            final_assessment = "Inauspicious"
        elif "Moderately Auspicious" in assessment_factors[0]:
            final_assessment = "Moderately Auspicious"
        else:
            final_assessment = "Neutral"
        
        return {
            "event_type": event_type,
            "event_date": event_date.isoformat(),
            "event_hour": event_hour,
            "assessment": final_assessment,
            "reasoning": " | ".join(assessment_factors),
            "event_profile": event_profile,
            "event_mewas": event_mewas,
            "hour_animal": hour_animal,
            "hour_element": hour_element,
            "day_element": day_element
        }
    
    # =================================================================
    # CONVENIENCE METHODS
    # =================================================================
    
    def full_analysis(self, birth_year: int, current_year: int, user_age: int,
                     user_gender: str, user_profession: str = "general") -> Dict[str, Any]:
        """
        Perform complete astrological analysis combining all subsystems.
        
        Args:
            birth_year: User's birth year
            current_year: Current year for obstacle analysis
            user_age: User's age
            user_gender: "male" or "female"
            user_profession: User's profession/status
            
        Returns:
            Complete analysis results
        """
        # Subsystem 1: Calculate user's astrological profile
        user_profile = self.calculate_astrological_profile(birth_year)
        
        # Subsystem 2: Calculate user's Mewa numbers
        user_mewas = self.calculate_mewa_numbers(user_profile["sixty_cycle_name"])
        
        # Subsystem 3: Analyze obstacles
        obstacle_analysis = self.analyze_obstacles(
            user_mewas, current_year, user_age, user_gender, user_profession
        )
        
        return {
            "user_profile": user_profile,
            "user_mewas": user_mewas,
            "obstacle_analysis": obstacle_analysis,
            "analysis_timestamp": datetime.now().isoformat(),
            "system_version": self.version
        }
    
    def to_json(self, analysis_result: Dict[str, Any], indent: int = 2) -> str:
        """Convert analysis result to JSON string."""
        return json.dumps(analysis_result, ensure_ascii=False, indent=indent)
    
    def to_human_readable(self, analysis_result: Dict[str, Any]) -> str:
        """Convert analysis result to human-readable text format."""
        lines = []
        lines.append("=" * 60)
        lines.append("TIBETAN ASTROLOGICAL ANALYSIS REPORT")
        lines.append("=" * 60)
        
        # User Profile
        profile = analysis_result["user_profile"]
        lines.append(f"\nBirth Year: {profile['gregorian_year']}")
        lines.append(f"Astrological Sign: {profile['sixty_cycle_name']}")
        lines.append(f"  - Animal: {profile['animal_sign']}")
        lines.append(f"  - Element: {profile['element']}")
        lines.append(f"  - Yin/Yang: {profile['yin_yang']}")
        lines.append(f"Rabjung Identifier: {profile['rabjung_identifier_m']}")
        
        # Mewa Numbers
        mewas = analysis_result["user_mewas"]
        lines.append(f"\nMewa Numbers:")
        lines.append(f"  Life Mewa:  {mewas['life_mewa']['number']} {mewas['life_mewa']['color']}")
        lines.append(f"  Body Mewa:  {mewas['body_mewa']['number']} {mewas['body_mewa']['color']}")
        lines.append(f"  Power Mewa: {mewas['power_mewa']['number']} {mewas['power_mewa']['color']}")
        
        # Obstacle Analysis
        obstacle_analysis = analysis_result["obstacle_analysis"]
        current_profile = obstacle_analysis["current_year_profile"]
        current_mewas = obstacle_analysis["current_year_mewas"]
        
        lines.append(f"\nObstacle Analysis for Current Year {current_profile['gregorian_year']}:")
        lines.append("-" * 50)
        lines.append(f"Current Year Sign: {current_profile['sixty_cycle_name']}")
        lines.append(f"Current Year Body Mewa: {current_mewas['body_mewa']['number']} {current_mewas['body_mewa']['color']} - {current_mewas['body_mewa']['element']}")
        
        obstacles = obstacle_analysis["obstacles_found"]
        if obstacles:
            lines.append(f"\n⚠️  {len(obstacles)} OBSTACLE(S) DETECTED:")
            for i, obs in enumerate(obstacles, 1):
                lines.append(f"\n{i}. {obs['name']} ({obs['type']})")
                lines.append(f"   Interpretation: {obs['interpretation']}")
                if 'details' in obs:
                    lines.append(f"   Details: {obs['details']}")
        else:
            lines.append(f"\n✅ NO OBSTACLES DETECTED")
            lines.append("   Current year conditions are favorable.")
        
        lines.append(f"\n" + "=" * 60)
        lines.append(f"Report generated: {analysis_result.get('analysis_timestamp', 'Unknown')}")
        lines.append(f"System version: {analysis_result.get('system_version', 'Unknown')}")
        
        return "\n".join(lines)


# Convenience function for quick analysis
def quick_analysis(birth_year: int, current_year: int, user_age: int, 
                  user_gender: str, user_profession: str = "general") -> str:
    """
    Quick analysis function that returns human-readable results.
    
    Args:
        birth_year: User's birth year
        current_year: Current year
        user_age: User's age
        user_gender: "male" or "female"
        user_profession: User's profession/status
        
    Returns:
        Human-readable analysis report
    """
    calculator = TibetanAstroCalculator()
    result = calculator.full_analysis(birth_year, current_year, user_age, user_gender, user_profession)
    return calculator.to_human_readable(result) 