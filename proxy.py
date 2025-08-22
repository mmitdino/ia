
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, requests

PORT = 5000
OPENROUTER_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_headers()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length)
        try:
            resp = requests.post(API_URL, headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            }, data=body)
            self.send_response(resp.status_code)
            self._set_headers()
            self.end_headers()
            self.wfile.write(resp.content)
        except Exception as e:
            self.send_response(500)
            self._set_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

HTTPServer(("localhost", PORT), Handler).serve_forever()
