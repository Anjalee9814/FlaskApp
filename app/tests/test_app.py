import os
import sys
import pytest

# Ensure the app module (app/app.py) can be imported when pytest runs from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app


def test_home():
    client = flask_app.test_client()
    res = client.get('/')
    assert res.status_code == 200
    assert b"Welcome to the Flask Web App!" in res.data


def test_health():
    client = flask_app.test_client()
    res = client.get('/health')
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}
