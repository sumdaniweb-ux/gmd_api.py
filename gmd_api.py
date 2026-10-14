import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

API_KEY = "95eb0c8897ab1034b4555491a306879df6c3d81ada67173839cdb6c81beb2785"
PORT = int(os.environ.get("PORT", 8000))

class GMDHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.headers.get("X-GMD-Key") != API_KEY:
            self.send_response(401)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "unauthorized"}).encode())
            return
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            data = json.loads(post_data)
            user_input = data.get('input', '').strip()
            if not user_input: raise ValueError("input required")
            response = {"status": "ok", "action": "log", "stored": True, "echo": user_input}
            self.send_response(200)
        except Exception as e:
            response = {"error": str(e)}
            self.send_response(400)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        if self.path == '/api/v1/health' or self.path == '/':
            response = {"status": "gmd_offline_active", "message": "Engine Running Successfully", "version": "2.0", "project": "GMD Spark Pakistan"}
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    print(f"✅ GMD API Running on port {PORT}")
    server = HTTPServer(('0.0.0.0', PORT), GMDHandler)
    server.serve_forever()