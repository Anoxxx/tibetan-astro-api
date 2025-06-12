#!/usr/bin/env python3
"""
Flask API Example for Tibetan Astrological Calculator
Use this as a starting point for integrating with zhengfei.info
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, date
import logging
import traceback

# Import our calculation modules
from tibetan_astro_core import TibetanAstroCalculator
from tibetan_astro_tables import PROSPERITY_EVENT_TYPES

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["https://zhengfei.info", "http://localhost:3000"])  # Configure CORS for your domain

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize calculator
calculator = TibetanAstroCalculator()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': calculator.version
    })

@app.route('/api/astrology/calculate', methods=['POST'])
def calculate_astrology():
    """
    Main endpoint for astrological calculations
    """
    try:
        # Get and validate JSON data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON data',
                'code': 'INVALID_JSON'
            }), 400

        # Validate required fields
        required_fields = ['birth_year', 'current_year', 'age', 'gender']
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'code': 'MISSING_FIELDS'
            }), 400

        # Validate data types and ranges
        try:
            birth_year = int(data['birth_year'])
            current_year = int(data['current_year'])
            age = int(data['age'])
            gender = str(data['gender']).lower()
            profession = str(data.get('profession', 'general')).lower()
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'Invalid data types. birth_year, current_year, and age must be integers.',
                'code': 'INVALID_DATA_TYPE'
            }), 400

        # Validate ranges
        if not (1900 <= birth_year <= 2100):
            return jsonify({
                'success': False,
                'error': 'birth_year must be between 1900 and 2100',
                'code': 'INVALID_BIRTH_YEAR'
            }), 400

        if not (1900 <= current_year <= 2100):
            return jsonify({
                'success': False,
                'error': 'current_year must be between 1900 and 2100',
                'code': 'INVALID_CURRENT_YEAR'
            }), 400

        if not (0 <= age <= 150):
            return jsonify({
                'success': False,
                'error': 'age must be between 0 and 150',
                'code': 'INVALID_AGE'
            }), 400

        if gender not in ['male', 'female']:
            return jsonify({
                'success': False,
                'error': 'gender must be either "male" or "female"',
                'code': 'INVALID_GENDER'
            }), 400

        valid_professions = ['general', 'official', 'monastic', 'lay_practitioner', 'sex_worker']
        if profession not in valid_professions:
            return jsonify({
                'success': False,
                'error': f'profession must be one of: {", ".join(valid_professions)}',
                'code': 'INVALID_PROFESSION'
            }), 400

        # Perform calculation
        logger.info(f"Calculating astrology for birth_year={birth_year}, current_year={current_year}, age={age}, gender={gender}")
        
        result = calculator.full_analysis(
            birth_year=birth_year,
            current_year=current_year,
            user_age=age,
            user_gender=gender,
            user_profession=profession
        )
        
        logger.info(f"Calculation successful for birth_year={birth_year}")
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 'VALIDATION_ERROR'
        }), 400
        
    except Exception as e:
        logger.error(f"Calculation error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Internal server error. Please try again later.',
            'code': 'SERVER_ERROR'
        }), 500

@app.route('/api/astrology/prosperity', methods=['POST'])
def assess_prosperity():
    """
    Endpoint for prosperity assessment
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON data',
                'code': 'INVALID_JSON'
            }), 400

        # Validate required fields
        required_fields = ['event_type', 'event_date', 'event_hour']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'code': 'MISSING_FIELDS'
            }), 400

        # Validate event type
        event_type = data['event_type']
        if event_type not in PROSPERITY_EVENT_TYPES:
            return jsonify({
                'success': False,
                'error': f'event_type must be one of: {PROSPERITY_EVENT_TYPES}',
                'code': 'INVALID_EVENT_TYPE'
            }), 400

        # Validate and parse event date
        try:
            event_date = datetime.strptime(data['event_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'event_date must be in YYYY-MM-DD format',
                'code': 'INVALID_DATE_FORMAT'
            }), 400

        # Validate event hour
        try:
            event_hour = int(data['event_hour'])
            if not (0 <= event_hour <= 23):
                raise ValueError("Hour out of range")
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'event_hour must be an integer between 0 and 23',
                'code': 'INVALID_HOUR'
            }), 400

        # Get optional user profile
        user_profile = data.get('user_profile')

        # Perform prosperity assessment
        logger.info(f"Assessing prosperity for event_type={event_type}, date={event_date}")
        
        result = calculator.assess_prosperity(
            event_type=event_type,
            event_date=event_date,
            event_hour=event_hour,
            user_profile=user_profile
        )
        
        logger.info(f"Prosperity assessment successful for {event_type}")
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"Prosperity assessment error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Internal server error. Please try again later.',
            'code': 'SERVER_ERROR'
        }), 500

@app.route('/api/astrology/info', methods=['GET'])
def get_system_info():
    """
    Get information about the astrology system
    """
    try:
        return jsonify({
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
                ],
                'mewa_colors': ['白 (White)', '黑 (Black)', '蓝 (Blue)', '绿 (Green)', '黄 (Yellow)', '红 (Red)'],
                'elements': ['木 (Wood)', '火 (Fire)', '土 (Earth)', '金 (Metal)', '水 (Water)']
            }
        })
    except Exception as e:
        logger.error(f"System info error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve system information',
            'code': 'SERVER_ERROR'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'code': 'NOT_FOUND'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 'Method not allowed',
        'code': 'METHOD_NOT_ALLOWED'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'code': 'SERVER_ERROR'
    }), 500

if __name__ == '__main__':
    # For development only
    print("🏔️  Tibetan Astrological Calculator API")
    print("=" * 50)
    print(f"System Version: {calculator.version}")
    print("Available endpoints:")
    print("  GET  /health                      - Health check")
    print("  POST /api/astrology/calculate     - Main calculation")
    print("  POST /api/astrology/prosperity    - Prosperity assessment")
    print("  GET  /api/astrology/info          - System information")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 