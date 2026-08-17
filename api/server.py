"""Small secure AEON status API for deployment behind a managed HTTPS host."""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "outputs" / "aeon-react" / "public" / "data" / "status.json"
TOKEN = os.environ.get("AEON_API_TOKEN", "")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/api/status":
            self.send_error(404)
            return
        self.send_json(json.loads(STATUS.read_text(encoding="utf-8")))

    def do_POST(self) -> None:
        if self.path != "/api/status" or not TOKEN or self.headers.get("Authorization") != f"Bearer {TOKEN}":
            self.send_error(401)
            return
        size = min(int(self.headers.get("Content-Length", "0")), 100_000)
        try:
            payload = json.loads(self.rfile.read(size))
            safe = {"updated_at": payload.get("updated_at"), "status": payload.get("status"), "next_action": payload.get("next_action"), "validation": payload.get("validation", []), "components": payload.get("components", {})}
            STATUS.write_text(json.dumps(safe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            self.send_json({"ok": True, "status": safe})
        except (ValueError, TypeError, json.JSONDecodeError):
            self.send_error(400)

    def send_json(self, payload: dict) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "https://igorvieira50002.github.io")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, *_: object) -> None:
        return


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", int(os.environ.get("PORT", "8790"))), Handler).serve_forever()
