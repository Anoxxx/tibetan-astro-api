#!/usr/bin/env python3
"""
Test script for the deployed Vercel API
"""

import requests
import json

# Your Vercel API URL (update this after deployment)
API_BASE_URL = "https://tibetan-astro-api.vercel.app"

def test_deployed_api():
    """Test the deployed API with a sample calculation"""
    print("🧪 Testing Deployed Tibetan Astrology API")
    print("=" * 50)
    
    # Test data
    test_data = {
        "birth_year": 1990,
        "current_year": 2025,
        "age": 35,
        "gender": "male",
        "profession": "general"
    }
    
    try:
        print(f"🌐 API URL: {API_BASE_URL}/api/astrology/calculate")
        print(f"📤 Sending request: {test_data}")
        
        response = requests.post(
            f"{API_BASE_URL}/api/astrology/calculate",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📨 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print("✅ API Test SUCCESSFUL!")
                print("\n📊 Results:")
                
                profile = result['data']['user_profile']
                mewas = result['data']['user_mewas']
                obstacles = result['data']['obstacle_analysis']
                
                print(f"Birth Year: {profile['gregorian_year']}")
                print(f"Sign: {profile['sixty_cycle_name']}")
                print(f"Animal: {profile['animal_sign']}")
                print(f"Element: {profile['element']}")
                
                print(f"\n🔢 Mewa Numbers:")
                print(f"Life:  {mewas['life_mewa']['number']} {mewas['life_mewa']['color']}")
                print(f"Body:  {mewas['body_mewa']['number']} {mewas['body_mewa']['color']}")
                print(f"Power: {mewas['power_mewa']['number']} {mewas['power_mewa']['color']}")
                
                print(f"\n⚠️ Obstacles: {obstacles['total_obstacles']} detected")
                for obs in obstacles['obstacles_found']:
                    print(f"- {obs['name']}: {obs['interpretation']}")
                
                print("\n🎉 Your API is working perfectly!")
                return True
            else:
                print(f"❌ API returned error: {result}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - API might still be starting up")
        print("💡 Try again in 1-2 minutes")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check the API URL")
        print("💡 Make sure the Vercel deployment completed successfully")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_check():
    """Test the health check endpoint"""
    try:
        print(f"\n🏥 Testing health check...")
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health Check: {result.get('status', 'unknown')}")
            print(f"Version: {result.get('version', 'unknown')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    print("🏔️ Tibetan Astrology API Deployment Test")
    print("=" * 60)
    print("📝 Instructions:")
    print("1. Update API_BASE_URL with your actual Vercel URL")
    print("2. Run this script to test your deployed API")
    print("=" * 60)
    
    # Test health check first
    if test_health_check():
        # Test main calculation
        test_deployed_api()
    else:
        print("\n💡 Troubleshooting:")
        print("- Make sure Vercel deployment completed successfully")
        print("- Check that the API URL is correct")
        print("- Wait a few minutes for cold start") 