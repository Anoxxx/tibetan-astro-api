"""
Vercel Serverless Function for Tibetan Astrological Calculator
This replaces the Flask API for deployment on Vercel
"""

import json
import sys
import os
from datetime import datetime

# Add the parent directory to Python path to import our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from tibetan_astro_core import TibetanAstroCalculator
from tibetan_astro_tables import PROSPERITY_EVENT_TYPES

# Initialize calculator
calculator = TibetanAstroCalculator()

def handler(request):
    """
    Main Vercel serverless function handler
    """
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        # Parse request path to determine endpoint
        path = request.url.path if hasattr(request.url, 'path') else '/'
        
        if path == '/api/astrology/calculate' and request.method == 'POST':
            return calculate_astrology(request, headers)
        elif path == '/api/astrology/prosperity' and request.method == 'POST':
            return assess_prosperity(request, headers)
        elif path == '/api/astrology/info' and request.method == 'GET':
            return get_system_info(headers)
        elif path == '/health' and request.method == 'GET':
            return health_check(headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'Endpoint not found',
                    'code': 'NOT_FOUND'
                })
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'error': 'Internal server error',
                'code': 'SERVER_ERROR'
            })
        }

def calculate_astrology(request, headers):
    """Handle astrology calculation requests"""
    try:
        # Parse JSON body
        if hasattr(request, 'body'):
            data = json.loads(request.body)
        else:
            data = request.json
            
        if not data:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'Invalid JSON data',
                    'code': 'INVALID_JSON'
                })
            }

        # Validate required fields
        required_fields = ['birth_year', 'current_year', 'age', 'gender']
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        
        if missing_fields:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': f'Missing required fields: {", ".join(missing_fields)}',
                    'code': 'MISSING_FIELDS'
                })
            }

        # Validate data types and ranges
        try:
            birth_year = int(data['birth_year'])
            current_year = int(data['current_year'])
            age = int(data['age'])
            gender = str(data['gender']).lower()
            profession = str(data.get('profession', 'general')).lower()
        except (ValueError, TypeError):
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'Invalid data types. birth_year, current_year, and age must be integers.',
                    'code': 'INVALID_DATA_TYPE'
                })
            }

        # Validate ranges
        if not (1900 <= birth_year <= 2100):
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'birth_year must be between 1900 and 2100',
                    'code': 'INVALID_BIRTH_YEAR'
                })
            }

        if not (1900 <= current_year <= 2100):
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'current_year must be between 1900 and 2100',
                    'code': 'INVALID_CURRENT_YEAR'
                })
            }

        if not (0 <= age <= 150):
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'age must be between 0 and 150',
                    'code': 'INVALID_AGE'
                })
            }

        if gender not in ['male', 'female']:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'gender must be either "male" or "female"',
                    'code': 'INVALID_GENDER'
                })
            }

        valid_professions = ['general', 'official', 'monastic', 'lay_practitioner', 'sex_worker']
        if profession not in valid_professions:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': f'profession must be one of: {", ".join(valid_professions)}',
                    'code': 'INVALID_PROFESSION'
                })
            }

        # Perform calculation
        result = calculator.full_analysis(
            birth_year=birth_year,
            current_year=current_year,
            user_age=age,
            user_gender=gender,
            user_profession=profession
        )
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'success': True,
                'data': result
            }, ensure_ascii=False)
        }
        
    except ValueError as e:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'error': str(e),
                'code': 'VALIDATION_ERROR'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'error': 'Internal server error. Please try again later.',
                'code': 'SERVER_ERROR'
            })
        }

def assess_prosperity(request, headers):
    """Handle prosperity assessment requests"""
    # Similar implementation to Flask version
    # (Simplified for brevity - full implementation would mirror Flask API)
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'success': True,
            'message': 'Prosperity assessment endpoint - implementation pending'
        })
    }

def get_system_info(headers):
    """Get system information"""
    try:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'success': True,
                'data': {
                    'system_name': 'Nine Palaces Outer Calculation (九宫外算)',
                    'version': calculator.version,
                    'supported_professions': ['general', 'official', 'monastic', 'lay_practitioner', 'sex_worker'],
                    'supported_genders': ['male', 'female'],
                    'year_range': {'min': 1900, 'max': 2100},
                    'age_range': {'min': 0, 'max': 150},
                    'prosperity_event_types': PROSPERITY_EVENT_TYPES,
                    'obstacle_types': [
                        {'code': 'RO', 'name': 'Regional Obstacle (方位障碍)'},
                        {'code': 'HO', 'name': 'Home Obstacle (家庭障碍)'},
                        {'code': 'BO', 'name': 'Bedding Obstacle (卧床障碍)'},
                        {'code': 'DO', 'name': 'Door Obstacle (门户障碍)'}
                    ]
                }
            }, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'error': 'Failed to retrieve system information',
                'code': 'SERVER_ERROR'
            })
        }

def health_check(headers):
    """Health check endpoint"""
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': calculator.version
        })
    }

# For local testing
if __name__ == "__main__":
    class MockRequest:
        def __init__(self, method, path, body=None):
            self.method = method
            self.url = type('obj', (object,), {'path': path})
            self.body = body
            self.json = json.loads(body) if body else None
    
    # Test the function
    test_request = MockRequest(
        'POST', 
        '/api/astrology/calculate',
        json.dumps({
            "birth_year": 1990,
            "current_year": 2025,
            "age": 35,
            "gender": "male",
            "profession": "general"
        })
    )
    
    result = handler(test_request)
    print("Test result:", result) 