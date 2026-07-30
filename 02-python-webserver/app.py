import http.server
import socketserver
import json
import os
from datetime import datetime

PORT = 8888

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/status' or self.path == '/json':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response_data = {
                "status": "success",
                "message": "CSE644 Python Web Server is running",
                "port": PORT,
                "timestamp": datetime.now().isoformat(),
                "hostname": os.uname().nodename if hasattr(os, 'uname') else os.environ.get('COMPUTERNAME', 'container')
            }
            self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CSE644 Python Web Server (Port 8888)</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #0d1117; color: #c9d1d9; padding: 40px; text-align: center; }}
        .card {{ background: #161b22; max-width: 550px; margin: auto; padding: 30px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }}
        h1 {{ color: #58a6ff; font-size: 1.8rem; margin-bottom: 10px; }}
        .port-tag {{ background: #238636; color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; display: inline-block; margin-bottom: 20px; }}
        p {{ color: #8b949e; line-height: 1.6; }}
        code {{ background: #21262d; color: #79c0ff; padding: 4px 8px; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="card">
        <span class="port-tag">LISTENING ON PORT 8888</span>
        <h1>Python Web Server Application</h1>
        <p>This simple web server is written in <code>Python</code> and containerized with <code>Docker</code> for <strong>CSE644 Requirement #6</strong>.</p>
        <p style="margin-top:20px; color:#58a6ff;">✓ HTTP/1.1 200 OK Response</p>
    </div>
</body>
</html>"""
            self.wfile.write(html_content.encode('utf-8'))

    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}")

if __name__ == '__main__':
    with socketserver.TCPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler) as httpd:
        print(f"Server started successfully on 0.0.0.0:{PORT}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()
