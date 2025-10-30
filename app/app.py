import os
from flask import Flask, jsonify, render_template_string, request, redirect, url_for
import psycopg2

# Read database URL from environment (provided by docker-compose)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://student:student123@db:5432/studentdb")

app = Flask(__name__)

# HTML template for the student form
STUDENT_FORM_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Student Management</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        form { background: #f4f4f4; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        label { display: block; margin-top: 10px; font-weight: bold; }
        input[type="text"], input[type="number"], input[type="email"] { 
            width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #ddd; border-radius: 4px; 
        }
        button { 
            background: #007bff; color: white; padding: 10px 20px; border: none; 
            border-radius: 4px; cursor: pointer; margin-top: 15px; 
        }
        button:hover { background: #0056b3; }
        .students-list { background: #fff; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .student-item { padding: 10px; border-bottom: 1px solid #eee; }
        .student-item:last-child { border-bottom: none; }
        .success { color: green; padding: 10px; background: #d4edda; border-radius: 4px; margin-bottom: 20px; }
        .nav { margin-bottom: 20px; }
        .nav a { margin-right: 15px; color: #007bff; text-decoration: none; }
        .nav a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Student Management System</h1>
    <div class="nav">
        <a href="/">Home</a>
        <a href="/students">View All Students</a>
        <a href="/health">Health Check</a>
        <a href="/data">Greetings Data</a>
    </div>
    
    {% if message %}
    <div class="success">{{ message }}</div>
    {% endif %}
    
    <form method="POST" action="/add-student">
        <h2>Add New Student</h2>
        <label>Name:</label>
        <input type="text" name="name" required>
        
        <label>Age:</label>
        <input type="number" name="age" min="1" max="150" required>
        
        <label>Email:</label>
        <input type="email" name="email" required>
        
        <label>Course:</label>
        <input type="text" name="course" required>
        
        <button type="submit">Add Student</button>
    </form>
    
    <div class="students-list">
        <h2>Recent Students (Last 10)</h2>
        {% if students %}
            {% for s in students %}
            <div class="student-item">
                <strong>{{ s[1] }}</strong> - Age: {{ s[2] }}, Email: {{ s[3] }}, Course: {{ s[4] }}
            </div>
            {% endfor %}
        {% else %}
            <p>No students in the database yet.</p>
        {% endif %}
    </div>
</body>
</html>
'''

def init_students_table():
    """Create students table if it doesn't exist"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INTEGER NOT NULL,
                email VARCHAR(100) NOT NULL,
                course VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating students table: {e}")

# Initialize the students table on startup
init_students_table()

@app.route('/')
def home():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('SELECT * FROM students ORDER BY created_at DESC LIMIT 10;')
        students = cur.fetchall()
        cur.close()
        conn.close()
        return render_template_string(STUDENT_FORM_HTML, students=students, message=request.args.get('message'))
    except Exception as e:
        return render_template_string(STUDENT_FORM_HTML, students=[], message=None)

@app.route('/add-student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    age = request.form.get('age')
    email = request.form.get('email')
    course = request.form.get('course')
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO students (name, age, email, course) VALUES (%s, %s, %s, %s);',
            (name, age, email, course)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('home', message=f'Student {name} added successfully!'))
    except Exception as e:
        return redirect(url_for('home', message=f'Error: {str(e)}'))

@app.route('/students')
def list_students():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('SELECT * FROM students ORDER BY created_at DESC;')
        students = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify([{
            'id': s[0],
            'name': s[1],
            'age': s[2],
            'email': s[3],
            'course': s[4],
            'created_at': str(s[5])
        } for s in students])
    except Exception as e:
        return jsonify(error=str(e)), 500

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
