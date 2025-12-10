import os, sys
from io import BytesIO
from pathlib import Path

# Ensure repo root is importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tictactoe.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

def handler(event, context):
    method = event.get("method", "GET")
    headers = event.get("headers", {}) or {}
    path = event.get("path", "/")
    body = event.get("body", "")
    query = event.get("queryString", "")

    environ = {
        "REQUEST_METHOD": method,
        "SCRIPT_NAME": "",
        "PATH_INFO": path,
        "QUERY_STRING": query,
        "SERVER_NAME": "vercel",
        "SERVER_PORT": "443",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": "https",
        "wsgi.input": BytesIO(body.encode() if isinstance(body, str) else body or b""),
        "wsgi.errors": BytesIO(),
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": True,
    }
    for k, v in headers.items():
        environ["HTTP_" + k.upper().replace("-", "_")] = v

    status = {}
    def start_response(s, h, exc_info=None):
        status["code"] = int(s.split(" ")[0]); status["headers"] = h

    result = application(environ, start_response)
    body_bytes = b"".join(result)
    return {
        "statusCode": status.get("code", 500),
        "headers": {k: v for k, v in status.get("headers", [])},
        "body": body_bytes.decode("utf-8", errors="replace"),
    }