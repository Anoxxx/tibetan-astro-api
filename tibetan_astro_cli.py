#!/usr/bin/env python3
"""
Tibetan Astrological Calculation System - Command Line Interface
Interactive CLI for calculating astrological profiles and obstacle analysis
"""

import argparse
import sys
from datetime import datetime, date
from typing import Optional

from tibetan_astro_core import TibetanAstroCalculator, quick_analysis
from tibetan_astro_tables import PROSPERITY_EVENT_TYPES


def interactive_mode():
    """Interactive mode for step-by-step user input"""
    print("=" * 60)
    print("🏔️  TIBETAN ASTROLOGICAL CALCULATION SYSTEM")
    print("   Based on Nine Palaces Outer Calculation (九宫外算)")
    print("=" * 60)
    
    calculator = TibetanAstroCalculator()
    
    try:
        # Get user input
        print("\n📅 BIRTH INFORMATION")
        print("-" * 30)
        
        while True:
            try:
                birth_year = int(input("Enter your birth year (e.g., 1990): "))
                if 1900 <= birth_year <= 2100:
                    break
                else:
                    print("⚠️  Please enter a year between 1900 and 2100")
            except ValueError:
                print("⚠️  Please enter a valid year (numbers only)")
        
        while True:
            try:
                current_year = int(input("Enter current year for analysis (e.g., 2025): "))
                if 1900 <= current_year <= 2100:
                    break
                else:
                    print("⚠️  Please enter a year between 1900 and 2100")
            except ValueError:
                print("⚠️  Please enter a valid year (numbers only)")
        
        while True:
            try:
                user_age = int(input("Enter your current age: "))
                if 0 <= user_age <= 150:
                    break
                else:
                    print("⚠️  Please enter a valid age (0-150)")
            except ValueError:
                print("⚠️  Please enter a valid age (numbers only)")
        
        print("\n👤 DEMOGRAPHIC INFORMATION")
        print("-" * 30)
        
        while True:
            gender = input("Gender (male/female): ").lower().strip()
            if gender in ['male', 'female', 'm', 'f']:
                user_gender = 'male' if gender in ['male', 'm'] else 'female'
                break
            else:
                print("⚠️  Please enter 'male' or 'female'")
        
        print("\n📋 PROFESSION/STATUS (optional, press Enter for general)")
        print("Available options: general, official, monastic, lay_practitioner, sex_worker")
        profession_input = input("Profession/status: ").strip().lower()
        
        valid_professions = ['general', 'official', 'monastic', 'lay_practitioner', 'sex_worker']
        user_profession = profession_input if profession_input in valid_professions else 'general'
        
        # Perform analysis
        print("\n🔮 CALCULATING YOUR ASTROLOGICAL PROFILE...")
        print("=" * 60)
        
        result = calculator.full_analysis(
            birth_year=birth_year,
            current_year=current_year,
            user_age=user_age,
            user_gender=user_gender,
            user_profession=user_profession
        )
        
        # Display results
        print(calculator.to_human_readable(result))
        
        # Offer additional options
        print("\n" + "=" * 60)
        print("📊 ADDITIONAL OPTIONS")
        print("=" * 60)
        
        while True:
            print("\nWhat would you like to do next?")
            print("1. Save results to file")
            print("2. Prosperity assessment for an event")
            print("3. Alternative Mewa calculation method")
            print("4. Export as JSON")
            print("5. Exit")
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                save_results(result, calculator)
            elif choice == '2':
                prosperity_assessment(calculator, result.get('user_profile'))
            elif choice == '3':
                alternative_mewa_calculation(calculator, result['user_profile'])
            elif choice == '4':
                export_json(result, calculator)
            elif choice == '5':
                print("\n🙏 Thank you for using the Tibetan Astrological System!")
                break
            else:
                print("⚠️  Please enter a number between 1 and 5")
                
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thank you for using the system.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)


def save_results(result, calculator):
    """Save analysis results to a text file"""
    try:
        birth_year = result['user_profile']['gregorian_year']
        filename = f"tibetan_astro_analysis_{birth_year}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(calculator.to_human_readable(result))
        
        print(f"✅ Results saved to: {filename}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")


def export_json(result, calculator):
    """Export analysis results as JSON"""
    try:
        birth_year = result['user_profile']['gregorian_year']
        filename = f"tibetan_astro_analysis_{birth_year}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(calculator.to_json(result))
        
        print(f"✅ JSON exported to: {filename}")
    except Exception as e:
        print(f"❌ Error exporting JSON: {e}")


def alternative_mewa_calculation(calculator, user_profile):
    """Show alternative Mewa calculation method"""
    try:
        print("\n🔄 ALTERNATIVE MEWA CALCULATION METHOD")
        print("Using the +3 rule: Body = Life + 3, Power = Body + 3")
        print("-" * 50)
        
        alt_mewas = calculator.calculate_mewa_alternative_method(user_profile['sixty_cycle_name'])
        
        print(f"Alternative Mewa Numbers for {user_profile['sixty_cycle_name']}:")
        print(f"  Life Mewa:  {alt_mewas['life_mewa']['number']} {alt_mewas['life_mewa']['color']}")
        print(f"  Body Mewa:  {alt_mewas['body_mewa']['number']} {alt_mewas['body_mewa']['color']}")
        print(f"  Power Mewa: {alt_mewas['power_mewa']['number']} {alt_mewas['power_mewa']['color']}")
        
    except Exception as e:
        print(f"❌ Error in alternative calculation: {e}")


def prosperity_assessment(calculator, user_profile):
    """Perform prosperity assessment for an event"""
    try:
        print("\n🌟 PROSPERITY ASSESSMENT")
        print("-" * 30)
        
        print("Available event types:")
        for i, event_type in enumerate(PROSPERITY_EVENT_TYPES, 1):
            print(f"{i:2d}. {event_type}")
        
        while True:
            try:
                choice = int(input(f"\nSelect event type (1-{len(PROSPERITY_EVENT_TYPES)}): "))
                if 1 <= choice <= len(PROSPERITY_EVENT_TYPES):
                    event_type = PROSPERITY_EVENT_TYPES[choice - 1]
                    break
                else:
                    print(f"⚠️  Please enter a number between 1 and {len(PROSPERITY_EVENT_TYPES)}")
            except ValueError:
                print("⚠️  Please enter a valid number")
        
        print(f"\nSelected event: {event_type}")
        
        # Get event date
        while True:
            date_str = input("Enter event date (YYYY-MM-DD, e.g., 2025-07-15): ").strip()
            try:
                event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                break
            except ValueError:
                print("⚠️  Please enter date in YYYY-MM-DD format")
        
        # Get event hour
        while True:
            try:
                event_hour = int(input("Enter event hour (0-23, e.g., 14 for 2 PM): "))
                if 0 <= event_hour <= 23:
                    break
                else:
                    print("⚠️  Please enter hour between 0 and 23")
            except ValueError:
                print("⚠️  Please enter a valid hour (numbers only)")
        
        # Perform prosperity assessment
        assessment = calculator.assess_prosperity(event_type, event_date, event_hour, user_profile)
        
        print("\n" + "=" * 50)
        print("🌟 PROSPERITY ASSESSMENT RESULTS")
        print("=" * 50)
        print(f"Event: {assessment['event_type']}")
        print(f"Date: {assessment['event_date']}")
        print(f"Hour: {assessment['event_hour']}:00")
        print(f"Assessment: {assessment['assessment']}")
        print(f"Reasoning: {assessment['reasoning']}")
        print(f"Hour Animal: {assessment['hour_animal']}")
        print(f"Day Element: {assessment['day_element']}")
        print(f"Hour Element: {assessment['hour_element']}")
        
    except Exception as e:
        print(f"❌ Error in prosperity assessment: {e}")


def command_line_mode():
    """Command-line argument mode"""
    parser = argparse.ArgumentParser(
        description="Tibetan Astrological Calculation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tibetan_astro_cli.py --birth-year 1990 --current-year 2025 --age 35 --gender male
  python tibetan_astro_cli.py -b 1984 -c 2025 -a 41 -g female --profession official
  python tibetan_astro_cli.py --interactive
        """
    )
    
    parser.add_argument('-b', '--birth-year', type=int, help='Birth year (e.g., 1990)')
    parser.add_argument('-c', '--current-year', type=int, help='Current year for analysis (e.g., 2025)')
    parser.add_argument('-a', '--age', type=int, help='Current age')
    parser.add_argument('-g', '--gender', choices=['male', 'female'], help='Gender')
    parser.add_argument('-p', '--profession', 
                       choices=['general', 'official', 'monastic', 'lay_practitioner', 'sex_worker'],
                       default='general', help='Profession/status (default: general)')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    parser.add_argument('--save', type=str, help='Save results to specified file')
    
    args = parser.parse_args()
    
    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
        return
    
    # Validate required arguments
    required_args = ['birth_year', 'current_year', 'age', 'gender']
    missing_args = [arg for arg in required_args if getattr(args, arg) is None]
    
    if missing_args:
        print(f"❌ Missing required arguments: {', '.join(missing_args)}")
        print("Use --help for usage information or --interactive for interactive mode")
        sys.exit(1)
    
    try:
        calculator = TibetanAstroCalculator()
        result = calculator.full_analysis(
            birth_year=args.birth_year,
            current_year=args.current_year,
            user_age=args.age,
            user_gender=args.gender,
            user_profession=args.profession
        )
        
        if args.json:
            output = calculator.to_json(result)
        else:
            output = calculator.to_human_readable(result)
        
        if args.save:
            with open(args.save, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✅ Results saved to: {args.save}")
        else:
            print(output)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    try:
        command_line_mode()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main() 