import time
import urllib.request
import json
import time
import urllib.request
import json


def test_integration_data_endpoint():
    """Poll the running /data endpoint for up to 60s and assert the JSON message exists and is exact.

    This test waits until the service responds at /data and asserts the seeded message created by
    `app/init_db.py` is present and exactly equals the expected string.
    """
    url = "http://localhost:5000/data"
    timeout = 60
    deadline = time.time() + timeout
    expected_message = "Hello from Flask and PostgreSQL!"
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=5) as r:
                if r.status != 200:
                    time.sleep(1)
                    continue
                payload = r.read().decode()
                data = json.loads(payload)
                assert isinstance(data, dict)
                # Assert the message matches the seeded value exactly
                assert data.get("message") == expected_message
                return
        except Exception:
            time.sleep(1)
    # If we reach here the service never responded correctly
    assert False, "Integration check failed: /data did not return expected JSON within timeout"
