import time
import urllib.request
import json
import sys

URL = "http://localhost:5000/data"
TIMEOUT = 60
DELAY = 2

end = time.time() + TIMEOUT
while time.time() < end:
    try:
        with urllib.request.urlopen(URL, timeout=5) as r:
            if r.status == 200:
                payload = r.read().decode()
                data = json.loads(payload)
                if data.get("message"):
                    print("Integration check passed: ", data)
                    sys.exit(0)
                else:
                    print("No message field yet, retrying...")
    except Exception as e:
        print(f"Waiting for service: {e}")
    time.sleep(DELAY)

print("Integration check failed: service not ready or returned unexpected data", file=sys.stderr)
sys.exit(1)
