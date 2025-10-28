import os
from flask import Flask, jsonify
import psycopg2

# Read database URL from environment (provided by docker-compose)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://student:student123@db:5432/studentdb")

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask Web App!"

@app.route('/health')
def health():
    # Simple health check for readiness probes
    return jsonify(status="ok")

@app.route('/data')
def get_data():
    # Connect to PostgreSQL and fetch a single message
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT message FROM greetings LIMIT 1;')
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify(message=None), 404
    return jsonify(message=row[0])

if __name__ == '__main__':
    # Useful for local debugging if you run `python app.py` directly
    app.run(host='0.0.0.0', port=5000)
