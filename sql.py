from flask import Flask, request, redirect, render_template_string, session, url_for
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = "vulnerable_demo_key"  # Needed for session management
DB = 'vuln.db'

def hash_md5(password):
    return hashlib.md5(password.encode()).hexdigest()

# Fake user data
FAKE_USERS = [
    ("admin", "admin@example.com", "1234567890", hash_md5("admin123")),
    ("john_doe", "john@example.com", "9876543210", hash_md5("password123")),
    ("alice", "alice@demo.com", "8887776666", hash_md5("qwerty")),
    ("bob_smith", "bob@gmail.com", "7778889999", hash_md5("letmein")),
    ("charlie", "charlie@somewhere.com", "9990001111", hash_md5("123456")),
]

def init_db():
    if os.path.exists(DB):
        return
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    c.executemany("INSERT INTO users (username, email, mobile, password) VALUES (?, ?, ?, ?)", FAKE_USERS)
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = hash_md5(password)

        # ❌ Still vulnerable to SQLi
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed}'"
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        try:
            print(f"[DEBUG] SQL: {query}")
            cursor.execute(query)
            result = cursor.fetchone()
        except Exception as e:
            print(f"[ERROR] {e}")
            result = None
        conn.close()

        if result:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            msg = "<div class='alert alert-danger'>❌ Login failed</div>"

    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
        <title>SQLi Demo Login</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #f0f2f5;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .login-box {
                background-color: white;
                padding: 2rem;
                border-radius: 1rem;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
                width: 100%;
                max-width: 400px;
            }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2 class="mb-4 text-center">🔐 SQL Injection Demo</h2>
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label">Username</label>
                    <input name="username" class="form-control" placeholder="Enter username" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Password</label>
                    <input name="password" type="password" class="form-control" placeholder="Enter password" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Login</button>
            </form>
            <div class="mt-3">
                {{ msg|safe }}
            </div>
        </div>
    </body>
    </html>
    ''', msg=msg)

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect('/')
    return f'''
    <!doctype html>
    <html lang="en">
    <head>
        <title>Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="p-5">
        <h1>✅ Welcome, {user}!</h1>
        <p>This is a fake dashboard. Feel free to simulate an attack here 😈</p>
        <a class="btn btn-secondary" href="/">Logout</a>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host="192.168.93.48", port=5000, debug=True)
