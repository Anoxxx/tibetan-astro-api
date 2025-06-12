"""
Vercel Serverless Function for Tibetan Astrological Calculator
"""

import json
import sys
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add the parent directory to Python path to import our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from tibetan_astro_core import TibetanAstroCalculator
from tibetan_astro_tables import PROSPERITY_EVENT_TYPES

# Initialize calculator
calculator = TibetanAstroCalculator()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        # For Vercel, support both root path and explicit paths
        if parsed_path.path == '/health' or parsed_path.path == '/':
            self.send_health_check()
        elif parsed_path.path == '/info' or parsed_path.path == '/api/astrology/info':
            self.send_system_info()
        else:
            self.send_error(404, 'Endpoint not found')
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        # For Vercel, the path will be just "/" when accessed via /api/index
        if parsed_path.path == '/' or parsed_path.path == '/api/astrology/calculate':
            self.handle_calculate()
        elif parsed_path.path == '/prosperity' or parsed_path.path == '/api/astrology/prosperity':
            self.handle_prosperity()
        else:
            self.send_error(404, 'Endpoint not found')
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def get_request_body(self):
        """Get and parse request body"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            return json.loads(body.decode('utf-8'))
        return {}
    
    def handle_calculate(self):
        """Handle astrology calculation requests"""
        try:
            data = self.get_request_body()
            
            # Validate required fields
            required_fields = ['birth_year', 'current_year', 'age', 'gender']
            missing_fields = [field for field in required_fields if field not in data or data[field] is None]
            
            if missing_fields:
                self.send_json_response({
                    'success': False,
                    'error': f'Missing required fields: {", ".join(missing_fields)}',
                    'code': 'MISSING_FIELDS'
                }, 400)
                return

            # Validate data types and ranges
            try:
                birth_year = int(data['birth_year'])
                current_year = int(data['current_year'])
                age = int(data['age'])
                gender = str(data['gender']).lower()
                profession = str(data.get('profession', 'general')).lower()
            except (ValueError, TypeError):
                self.send_json_response({
                    'success': False,
                    'error': 'Invalid data types. birth_year, current_year, and age must be integers.',
                    'code': 'INVALID_DATA_TYPE'
                }, 400)
                return

            # Validate ranges
            if not (1900 <= birth_year <= 2100):
                self.send_json_response({
                    'success': False,
                    'error': 'birth_year must be between 1900 and 2100',
                    'code': 'INVALID_BIRTH_YEAR'
                }, 400)
                return

            if not (1900 <= current_year <= 2100):
                self.send_json_response({
                    'success': False,
                    'error': 'current_year must be between 1900 and 2100',
                    'code': 'INVALID_CURRENT_YEAR'
                }, 400)
                return

            if not (0 <= age <= 150):
                self.send_json_response({
                    'success': False,
                    'error': 'age must be between 0 and 150',
                    'code': 'INVALID_AGE'
                }, 400)
                return

            if gender not in ['male', 'female']:
                self.send_json_response({
                    'success': False,
                    'error': 'gender must be either "male" or "female"',
                    'code': 'INVALID_GENDER'
                }, 400)
                return

            valid_professions = ['general', 'official', 'monastic', 'lay_practitioner', 'sex_worker']
            if profession not in valid_professions:
                self.send_json_response({
                    'success': False,
                    'error': f'profession must be one of: {", ".join(valid_professions)}',
                    'code': 'INVALID_PROFESSION'
                }, 400)
                return

            # Perform calculation
            result = calculator.full_analysis(
                birth_year=birth_year,
                current_year=current_year,
                user_age=age,
                user_gender=gender,
                user_profession=profession
            )
            
            self.send_json_response({
                'success': True,
                'data': result
            })
            
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': 'Internal server error. Please try again later.',
                'code': 'SERVER_ERROR'
            }, 500)
    
    def handle_prosperity(self):
        """Handle prosperity assessment requests"""
        self.send_json_response({
            'success': True,
            'message': 'Prosperity assessment endpoint - implementation pending'
        })
    
    def send_system_info(self):
        """Send system information"""
        try:
            self.send_json_response({
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
            })
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': 'Failed to retrieve system information',
                'code': 'SERVER_ERROR'
            }, 500)
    
    def send_health_check(self):
        """Send health check response"""
        self.send_json_response({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': calculator.version
        })

# This function will be automatically called by Vercel 