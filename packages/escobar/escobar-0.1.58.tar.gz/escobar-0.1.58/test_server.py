from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
from datetime import datetime

# Create test files for different paths
with open('test.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Hello from Test Server</h1>
    <p>This is a test page served by a simple Python HTTP server.</p>
    <p>Current time: <span id="time"></span></p>
    
    <script>
        document.getElementById('time').textContent = new Date().toLocaleString();
    </script>
</body>
</html>
''')

# Create a directory for nested path testing
os.makedirs('api', exist_ok=True)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Received request for path: {self.path}")
        
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
<!DOCTYPE html>
<html>
<head>
    <title>Test Server Index</title>
</head>
<body>
    <h1>Test Server Index</h1>
    <p>Available test paths:</p>
    <ul>
        <li><a href="/test.html">Test HTML Page</a></li>
        <li><a href="/api/data">API Data Endpoint</a></li>
        <li><a href="/api/time">API Time Endpoint</a></li>
    </ul>
</body>
</html>
''')
        elif self.path == '/test.html':
            with open('test.html', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = {
                'message': 'This is test data from the API',
                'items': ['item1', 'item2', 'item3'],
                'count': 3
            }
            self.wfile.write(json.dumps(data).encode())
        elif self.path == '/api/time':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            time_data = {
                'current_time': datetime.now().isoformat(),
                'timestamp': datetime.now().timestamp()
            }
            self.wfile.write(json.dumps(time_data).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

# Set up the server
port = 3000
server_address = ('', port)
httpd = HTTPServer(server_address, Handler)

print(f"Starting test server on port {port}...")
print(f"Visit http://localhost:{port}/test.html to see the test page")
httpd.serve_forever()
