"""
VULNERABLE_APP.PY - Demo Application with Known Vulnerabilities
========================================================================
⚠️  WARNING: This application intentionally contains security vulnerabilities
               for testing and educational purposes only.
               
DO NOT use in production. DO NOT expose to the internet.
========================================================================
"""

from flask import Flask, render_template_string, request
import sqlite3

app = Flask(__name__)

# Initialize vulnerable database
def init_db():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('''CREATE TABLE users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute("INSERT INTO users VALUES (1, 'admin', 'password123')")
    c.execute("INSERT INTO users VALUES (2, 'user', 'secret456')")
    conn.commit()
    return conn

db = init_db()

# VULNERABLE: Reflected XSS
@app.route('/vulnerable-xss')
def vulnerable_xss():
    search = request.args.get('q', '')
    html = f"""
    <html>
    <body style="font-family: Arial; padding: 20px;">
        <h1>Search Results</h1>
        <p>You searched for: {search}</p>
        <p>No results found.</p>
    </body>
    </html>
    """
    return render_template_string(html)

# VULNERABLE: SQL Injection
@app.route('/vulnerable-sqli')
def vulnerable_sqli():
    username = request.args.get('username', '')
    
    try:
        # VULNERABLE: Direct string concatenation
        query = f"SELECT * FROM users WHERE username = '{username}'"
        c = db.cursor()
        c.execute(query)
        result = c.fetchone()
        
        if result:
            return f"""
            <html>
            <body style="font-family: Arial; padding: 20px;">
                <h1>User Found!</h1>
                <p>Username: {result[1]}</p>
                <p>Password: {result[2]}</p>
            </body>
            </html>
            """
        else:
            return """
            <html>
            <body style="font-family: Arial; padding: 20px;">
                <h1>User Not Found</h1>
            </body>
            </html>
            """
    except Exception as e:
        # VULNERABLE: Displays database errors
        return f"""
        <html>
        <body style="font-family: Arial; padding: 20px;">
            <h1>Error</h1>
            <p style="color: red;">SQL Error: {str(e)}</p>
        </body>
        </html>
        """

# VULNERABLE: Combined form
@app.route('/vulnerable-form', methods=['GET', 'POST'])
def vulnerable_form():
    message = ''
    
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        
        # VULNERABLE: XSS - Direct insertion into HTML
        message = f"<p style='color: green;'>Thank you {name}, we will contact you at {email}</p>"
    
    html = f"""
    <html>
    <body style="font-family: Arial; padding: 20px;">
        <h1>Contact Form</h1>
        <form method="POST">
            <input type="text" name="name" placeholder="Your Name" required>
            <input type="email" name="email" placeholder="Your Email" required>
            <button type="submit">Submit</button>
        </form>
        {message}
    </body>
    </html>
    """
    return render_template_string(html)

# VULNERABLE: Search with filter bypass
@app.route('/search-users')
def search_users():
    search_term = request.args.get('q', '')
    
    try:
        # VULNERABLE: SQLi - Using string formatting
        query = f"SELECT username FROM users WHERE username LIKE '%{search_term}%'"
        c = db.cursor()
        c.execute(query)
        results = c.fetchall()
        
        # VULNERABLE: XSS - Results displayed without encoding
        html = "<html><body style='font-family: Arial; padding: 20px;'>"
        html += f"<h1>Search Results for: {search_term}</h1>"
        html += "<ul>"
        for result in results:
            html += f"<li>{result[0]}</li>"
        html += "</ul></body></html>"
        
        return render_template_string(html)
    except Exception as e:
        return f"<html><body>Error: {str(e)}</body></html>"

# Safe example (for comparison)
@app.route('/safe-example')
def safe_example():
    search = request.args.get('q', '')
    
    # SAFE: Using template escaping
    html = """
    <html>
    <body style="font-family: Arial; padding: 20px;">
        <h1>Safe Search</h1>
        <p>You searched for: <strong>{{ search }}</strong></p>
    </body>
    </html>
    """
    return render_template_string(html, search=search)

@app.route('/')
def index():
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial; padding: 20px; background: #f5f5f5; }
            .endpoint { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .vulnerable { border-left: 4px solid red; }
            .safe { border-left: 4px solid green; }
            a { color: #0066cc; text-decoration: none; }
            a:hover { text-decoration: underline; }
            code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🔒 Vulnerable Application - FOR TESTING ONLY</h1>
        <p>⚠️  This application intentionally contains security vulnerabilities for educational testing.</p>
        
        <h2>Vulnerable Endpoints (for scanner testing):</h2>
        
        <div class="endpoint vulnerable">
            <h3>1. Reflected XSS</h3>
            <p><a href="/vulnerable-xss?q=<script>alert('xss')</script>">/vulnerable-xss</a></p>
            <p>Try payload: <code>&lt;script&gt;alert('xss')&lt;/script&gt;</code></p>
        </div>
        
        <div class="endpoint vulnerable">
            <h3>2. SQL Injection</h3>
            <p><a href="/vulnerable-sqli?username=' OR '1'='1">/vulnerable-sqli</a></p>
            <p>Try payload: <code>' OR '1'='1</code></p>
        </div>
        
        <div class="endpoint vulnerable">
            <h3>3. Form-based Injection</h3>
            <p><a href="/vulnerable-form">/vulnerable-form</a></p>
            <p>POST name and email parameters with XSS payload</p>
        </div>
        
        <div class="endpoint vulnerable">
            <h3>4. Combined XSS + SQLi</h3>
            <p><a href="/search-users?q=<img src=x onerror=alert('xss')>">/search-users</a></p>
            <p>Try SQLi: <code>%' OR '1'='1</code></p>
        </div>
        
        <div class="endpoint safe">
            <h3>5. Safe Example (for comparison)</h3>
            <p><a href="/safe-example?q=hello">/safe-example</a></p>
            <p>This endpoint properly escapes output</p>
        </div>
        
        <h2>Testing Instructions:</h2>
        <ol>
            <li>Run this app: <code>python vulnerable_app.py</code> (on different port)</li>
            <li>Go back to VulnScan at http://localhost:5000</li>
            <li>Scan: <code>http://localhost:5001</code></li>
            <li>Scanner should detect vulnerabilities automatically</li>
        </ol>
        
        <h2>Manual Testing Examples:</h2>
        <ul>
            <li><a href="/vulnerable-xss?q=<script>alert('XSS Detected!')</script>">Test XSS - Alert Box</a></li>
            <li><a href="/vulnerable-xss?q=<img src=x onerror='alert(document.cookie)'>">Test XSS - Image Tag</a></li>
            <li><a href="/vulnerable-sqli?username=' OR 1=1--">Test SQLi - Boolean</a></li>
            <li><a href="/search-users?q=%' OR '1'='1--">Test SQLi in Search</a></li>
        </ul>
        
        <hr>
        <p style="color: red;"><strong>⚠️  SECURITY WARNING:</strong> This is a deliberately vulnerable application for testing purposes only. Never use this in production or with real data.</p>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    print("=" * 60)
    print("VULNERABLE APP - FOR TESTING VulnScan ONLY")
    print("=" * 60)
    print("⚠️  This app has intentional vulnerabilities!")
    print("🔗 Access at: http://localhost:5001")
    print("=" * 60)
    app.run(debug=True, port=5001)
