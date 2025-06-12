#!/usr/bin/env python3
"""
Test script for the Flask API
Run this after starting the Flask server to verify it works
"""

import requests
import json
from datetime import date

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_astrology_calculation():
    """Test the main astrology calculation endpoint"""
    print("\nTesting astrology calculation...")
    
    test_data = {
        "birth_year": 1990,
        "current_year": 2025,
        "age": 35,
        "gender": "male",
        "profession": "general"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/astrology/calculate",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Calculation successful!")
            data = result['data']
            profile = data['user_profile']
            mewas = data['user_mewas']
            
            print(f"Birth Year: {profile['gregorian_year']}")
            print(f"Sign: {profile['sixty_cycle_name']}")
            print(f"Animal: {profile['animal_sign']}")
            print(f"Mewas: Life={mewas['life_mewa']['number']}, Body={mewas['body_mewa']['number']}, Power={mewas['power_mewa']['number']}")
            print(f"Obstacles: {data['obstacle_analysis']['total_obstacles']}")
            
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_system_info():
    """Test the system info endpoint"""
    print("\nTesting system info...")
    try:
        response = requests.get(f"{BASE_URL}/api/astrology/info")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ System info retrieved!")
            data = result['data']
            print(f"System: {data['system_name']}")
            print(f"Version: {data['version']}")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_validation_errors():
    """Test that validation works correctly"""
    print("\nTesting validation errors...")
    
    # Test missing fields
    test_data = {
        "birth_year": 1990,
        # Missing other required fields
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/astrology/calculate",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            error = response.json()
            if 'MISSING_FIELDS' in error.get('code', ''):
                print("✅ Validation working correctly - missing fields detected")
                return True
            else:
                print(f"❌ Unexpected error: {error}")
                return False
        else:
            print(f"❌ Expected 400 error, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🏔️  Testing Tibetan Astrological Calculator API")
    print("=" * 60)
    
    tests = [
        test_health_check,
        test_astrology_calculation,
        test_system_info,
        test_validation_errors
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print("-" * 40)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API implementation.")

if __name__ == "__main__":
    main() 