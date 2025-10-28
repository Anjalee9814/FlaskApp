import urllib.request
import json
import sys

URL = "http://localhost:5000/health"

try:
    with urllib.request.urlopen(URL, timeout=5) as r:
        if r.status != 200:
            print(f"Unexpected status: {r.status}", file=sys.stderr)
            sys.exit(1)
        payload = r.read().decode()
        data = json.loads(payload)
        if data.get("status") == "ok":
            sys.exit(0)
        else:
            print(f"Unexpected payload: {data}", file=sys.stderr)
            sys.exit(1)
except Exception as e:
    print(e, file=sys.stderr)
    sys.exit(1)
