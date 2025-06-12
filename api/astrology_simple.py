from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'status': 'healthy',
            'message': 'Tibetan Astrology API is working!',
            'endpoints': {
                'POST /api/astrology': 'Main calculation endpoint',
                'GET /api/astrology': 'Health check'
            }
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
        
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Get request body
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode('utf-8'))
            except:
                data = {}
        else:
            data = {}
        
        # Mock response for now
        response = {
            'success': True,
            'message': 'Tibetan Astrology calculation will be implemented here',
            'received_data': data,
            'mock_result': {
                'user_profile': {
                    'birth_year': data.get('birth_year', 1990),
                    'sixty_cycle_name': '金阳马 (Metal-Yang-Horse)',
                    'animal_sign': '马 (Horse)',
                    'element': '金 (Metal)',
                    'yin_yang': '阳 (Yang)'
                },
                'user_mewas': {
                    'life_mewa': {'number': 4, 'color': '绿 (Green)'},
                    'body_mewa': {'number': 7, 'color': '红 (Red)'},
                    'power_mewa': {'number': 1, 'color': '白 (White)'}
                },
                'obstacles_found': []
            }
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 