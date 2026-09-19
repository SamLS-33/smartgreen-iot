from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/telemetry":
            self.send_error(404); return
        length = int(self.headers.get("Content-Length", "0"))
        try:
            message = json.loads(self.rfile.read(length).decode("utf-8"))
            print(json.dumps(message, ensure_ascii=False, indent=2))
            response = json.dumps({
                "status": "accepted",
                "message_id": message.get("message_id")
            }).encode()
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)
        except Exception as exc:
            self.send_error(400, str(exc))

if __name__ == "__main__":
    print("Receptor de prueba: http://localhost:8000/api/telemetry")
    ThreadingHTTPServer(("localhost", 8000), Handler).serve_forever()