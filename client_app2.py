from flask import Flask, render_template_string, jsonify, request
from agent_sdk import Agent, monitor_performance
import requests
import logging
import time
import random
import threading
import json
from datetime import datetime
from sqlalchemy import create_engine, text
import traceback

app = Flask(__name__)

# ----------------------------
# Configuration
# ----------------------------
ERROR_CATEGORIES = {
    'HTTP_4XX': ['404', '403', '400'],
    'HTTP_5XX': ['500', '502', '503'],
    'DATABASE': ['connection', 'constraint', 'syntax'],
    'BUSINESS_LOGIC': ['validation', 'state', 'permission'],
    'PERFORMANCE': ['timeout', 'slow_query', 'deadlock'],
    'EXTERNAL_API': ['timeout', 'unavailable', 'rate_limit']
}

# ----------------------------
# Database (SQLite for testing)
# ----------------------------
engine = create_engine("sqlite:///test.db", echo=False)

with engine.connect() as conn:
    # Create tables
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            name TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    
    # Create error logs table for analysis
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS error_simulation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_type TEXT,
            category TEXT,
            timestamp TIMESTAMP,
            details TEXT
        )
    """))
    conn.commit()

# ----------------------------
# Initialize Agent 
# ----------------------------
Agent.init(
    api_key="private_test",
    api_secret="super-secret",
    endpoint="http://127.0.0.1:8000/api/logs",
    project="Online_website_logs",
    framework="flask",
    app=app,
    enable_http=True,
    enable_logging=True,
    enable_exceptions=True,
    enable_performance=True
)

# ----------------------------
# Dashboard UI (Enhanced)
# ----------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Agent SDK - Chaos Engineering Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial;
            background: #0a0e17;
            color: #e4e6f0;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 { 
            color: #00ffcc;
            font-size: 2.5em;
            margin-bottom: 30px;
        }
        .stats-panel {
            background: #1a1f2e;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
        }
        .stat-card {
            background: #262d3d;
            padding: 15px;
            border-radius: 8px;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #00ffcc;
        }
        .button-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        button {
            padding: 15px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,255,204,0.3);
        }
        .btn-http { background: #3399ff; color: white; }
        .btn-db { background: #9933ff; color: white; }
        .btn-business { background: #ff9933; color: white; }
        .btn-performance { background: #ffcc00; color: black; }
        .btn-external { background: #ff66b2; color: white; }
        .btn-chaos { background: #ff4d4d; color: white; }
        
        #result {
            margin-top: 30px;
            padding: 20px;
            background: #1a1f2e;
            border-radius: 8px;
            font-family: monospace;
            text-align: left;
            border-left: 4px solid #00ffcc;
        }
        .error-log {
            color: #ff6b6b;
        }
        .success-log {
            color: #51cf66;
        }
        .chaos-controls {
            margin: 20px 0;
            padding: 20px;
            background: #262d3d;
            border-radius: 8px;
        }
        input[type="range"] {
            width: 300px;
            margin: 0 10px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>🚀 Chaos Engineering Dashboard</h1>
    
    <div class="stats-panel" id="stats">
        <div class="stat-card">
            <div>Total Errors</div>
            <div class="stat-value" id="totalErrors">0</div>
        </div>
        <div class="stat-card">
            <div>HTTP Errors</div>
            <div class="stat-value" id="httpErrors">0</div>
        </div>
        <div class="stat-card">
            <div>DB Errors</div>
            <div class="stat-value" id="dbErrors">0</div>
        </div>
        <div class="stat-card">
            <div>Response Time</div>
            <div class="stat-value" id="avgResponse">0ms</div>
        </div>
    </div>

    <div class="chaos-controls">
        <h3>🤖 Chaos Automation</h3>
        <label>Frequency: <span id="freqValue">3s</span></label>
        <input type="range" id="chaosFreq" min="1" max="10" value="3">
        <button onclick="toggleChaos()" id="chaosToggle" class="btn-chaos">⏸️ Pause Chaos</button>
        <button onclick="resetStats()" class="btn-http">📊 Reset Stats</button>
    </div>

    <div class="button-grid">
        <button class="btn-http" onclick="hit('/http/200')">✅ HTTP Success</button>
        <button class="btn-http" onclick="hit('/http/404')">⚠️ 404 Not Found</button>
        <button class="btn-http" onclick="hit('/http/500')">🔥 500 Server Error</button>
        <button class="btn-http" onclick="hit('/http/403')">🔒 403 Forbidden</button>
        <button class="btn-http" onclick="hit('/http/429')">⏳ 429 Rate Limit</button>
        
        <button class="btn-db" onclick="hit('/db/insert')">💾 DB Insert</button>
        <button class="btn-db" onclick="hit('/db/select')">🔍 DB Select</button>
        <button class="btn-db" onclick="hit('/db/constraint')">⚠️ Constraint Error</button>
        <button class="btn-db" onclick="hit('/db/connection')">🔌 Connection Error</button>
        
        <button class="btn-business" onclick="hit('/business/validation')">📝 Validation Error</button>
        <button class="btn-business" onclick="hit('/business/state')">🔄 Invalid State</button>
        
        <button class="btn-performance" onclick="hit('/performance/slow')">🐢 Slow Query</button>
        <button class="btn-performance" onclick="hit('/performance/timeout')">⏰ Timeout</button>
        
        <button class="btn-external" onclick="hit('/external/api')">🌐 External API</button>
        <button class="btn-external" onclick="hit('/external/timeout')">⌛ API Timeout</button>
        
        <button class="btn-chaos" onclick="hit('/crash')">💥 Crash App</button>
        <button class="btn-chaos" onclick="hit('/memory-leak')">📈 Memory Leak</button>
    </div>

    <div id="result">Click any button to simulate an error...</div>
</div>

<script>
let chaosActive = true;
let chaosInterval;
let stats = {
    total: 0,
    http: 0,
    db: 0,
    responseTime: []
};

async function hit(route) {
    const start = performance.now();
    document.getElementById("result").innerHTML = `<span class="info">⏳ Calling ${route}...</span>`;
    
    try {
        const res = await fetch(route);
        const text = await res.text();
        const time = Math.round(performance.now() - start);
        
        document.getElementById("result").innerHTML = `
            <div class="${res.ok ? 'success-log' : 'error-log'}">
                ⏱️ ${time}ms | Status: ${res.status}<br>
                ${text}
            </div>
        `;
        
        // Update stats
        stats.total++;
        if (!res.ok) stats.http++;
        stats.responseTime.push(time);
        if (stats.responseTime.length > 100) stats.responseTime.shift();
        updateStats();
    } catch (e) {
        document.getElementById("result").innerHTML = `<span class="error-log">❌ Error: ${e}</span>`;
    }
}

function updateStats() {
    const avg = stats.responseTime.length ? 
        Math.round(stats.responseTime.reduce((a,b) => a+b, 0) / stats.responseTime.length) : 0;
    
    document.getElementById('totalErrors').innerText = stats.total;
    document.getElementById('httpErrors').innerText = stats.http;
    document.getElementById('avgResponse').innerText = avg + 'ms';
}

function toggleChaos() {
    chaosActive = !chaosActive;
    const btn = document.getElementById('chaosToggle');
    btn.innerText = chaosActive ? '⏸️ Pause Chaos' : '▶️ Resume Chaos';
    btn.style.background = chaosActive ? '#ff4d4d' : '#51cf66';
}

function resetStats() {
    stats = { total: 0, http: 0, db: 0, responseTime: [] };
    updateStats();
}

// Chaos automation
document.getElementById('chaosFreq').addEventListener('input', (e) => {
    document.getElementById('freqValue').innerText = e.target.value + 's';
    if (chaosInterval) {
        clearInterval(chaosInterval);
        chaosInterval = setInterval(() => {
            if (chaosActive) {
                const routes = [
                    '/http/404', '/http/500', '/http/403',
                    '/db/constraint', '/db/connection',
                    '/business/validation', '/performance/slow',
                    '/external/timeout'
                ];
                hit(routes[Math.floor(Math.random() * routes.length)]);
            }
        }, e.target.value * 1000);
    }
});

// Start chaos
chaosInterval = setInterval(() => {
    if (chaosActive) {
        const routes = [
            '/http/404', '/http/500', '/http/403',
            '/db/constraint', '/db/connection',
            '/business/validation', '/performance/slow',
            '/external/timeout'
        ];
        hit(routes[Math.floor(Math.random() * routes.length)]);
    }
}, 3000);
</script>
</body>
</html>
"""

@app.route("/")
def dashboard():
    return render_template_string(HTML_PAGE)

# ----------------------------
# HTTP Error Routes
# ----------------------------
@app.route("/http/<int:code>")
def http_error(code):
    """Simulate HTTP errors"""
    error_map = {
        200: "✅ Success",
        400: "⚠️ Bad Request",
        403: "🔒 Forbidden",
        404: "🔍 Not Found",
        429: "⏳ Too Many Requests",
        500: "🔥 Internal Server Error",
        502: "🌐 Bad Gateway",
        503: "🚧 Service Unavailable"
    }
    
    message = error_map.get(code, f"HTTP {code} Error")
    
    # Log the error for analysis
    log_error_simulation('HTTP', str(code), message)
    
    return message, code

# ----------------------------
# Database Error Routes
# ----------------------------
@app.route("/db/insert")
def db_insert():
    """Successful DB operation"""
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO users (name, email) VALUES (:name, :email)"),
            {"name": f"User{random.randint(1,1000)}", 
             "email": f"user{random.randint(1,1000)}@test.com"}
        )
        conn.commit()
    return "✅ User inserted successfully"

@app.route("/db/select")
def db_select():
    """DB select operation"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users ORDER BY RANDOM() LIMIT 1"))
        user = result.fetchone()
    return f"✅ Found user: {user}" if user else "ℹ️ No users found"

@app.route("/db/constraint")
def db_constraint():
    """Simulate constraint violation"""
    with engine.connect() as conn:
        # Try to insert duplicate (if you have unique constraint)
        conn.execute(
            text("INSERT INTO users (id, name) VALUES (1, 'Duplicate')")
        )
        conn.commit()
    return "⚠️ Should fail", 400

@app.route("/db/connection")
def db_connection():
    """Simulate connection error"""
    # Use wrong database name
    bad_engine = create_engine("sqlite:///nonexistent.db")
    with bad_engine.connect() as conn:
        conn.execute(text("SELECT * FROM users"))
    return "🔌 Connection error", 500

# ----------------------------
# Business Logic Errors
# ----------------------------
@app.route("/business/validation")
def validation_error():
    """Simulate validation error"""
    data = request.args.get('data', '')
    if not data:
        log_error_simulation('BUSINESS', 'validation', 'Missing required data')
        return "❌ Validation Error: Data is required", 400
    return "✅ Data validated"

@app.route("/business/state")
def invalid_state():
    """Simulate invalid state error"""
    states = ['draft', 'pending', 'approved']
    current = random.choice(states)
    invalid_transition = 'deleted'
    
    log_error_simulation('BUSINESS', 'state', f'Invalid transition from {current} to {invalid_transition}')
    return f"❌ Cannot transition from {current} to {invalid_transition}", 409

# ----------------------------
# Performance Issues
# ----------------------------
@monitor_performance(threshold_ms=300)
@app.route("/performance/slow")
def slow_query():
    """Simulate slow database query"""
    time.sleep(random.uniform(0.5, 2.0))
    
    with engine.connect() as conn:
        # Simulate complex query
        result = conn.execute(text("""
            WITH RECURSIVE cnt(x) AS (
                SELECT 1
                UNION ALL
                SELECT x+1 FROM cnt WHERE x<1000
            )
            SELECT count(*) FROM cnt
        """))
    
    log_error_simulation('PERFORMANCE', 'slow_query', f'Query took >500ms')
    return f"🐢 Slow query completed"

@app.route("/performance/timeout")
def timeout():
    """Simulate timeout"""
    time.sleep(5)  # This will timeout if you have a timeout configured
    return "⏰ Should timeout"

# ----------------------------
# External API Errors
# ----------------------------
@app.route("/external/api")
def external_api():
    """Simulate external API call"""
    endpoints = [
        "https://httpbin.org/get",
        "https://httpbin.org/status/500",
        "https://httpbin.org/delay/3"
    ]
    
    try:
        response = requests.get(random.choice(endpoints), timeout=2)
        return f"🌐 External API responded with {response.status_code}"
    except requests.exceptions.Timeout:
        log_error_simulation('EXTERNAL', 'timeout', 'External API timeout')
        return "⌛ External API timeout", 504
    except Exception as e:
        log_error_simulation('EXTERNAL', 'error', str(e))
        return f"❌ External API error: {str(e)}", 502

@app.route("/external/timeout")
def external_timeout():
    """Simulate external API timeout"""
    try:
        response = requests.get("https://httpbin.org/delay/5", timeout=1)
        return response.text
    except requests.exceptions.Timeout:
        log_error_simulation('EXTERNAL', 'timeout', 'API timeout after 1s')
        return "⌛ API Timeout", 504

# ----------------------------
# Critical Errors
# ----------------------------
@app.route("/crash")
def crash():
    """Simulate application crash"""
    log_error_simulation('CRITICAL', 'crash', 'Application crash simulated')
    raise Exception("💥 Simulated application crash")

@app.route("/memory-leak")
def memory_leak():
    """Simulate memory leak"""
    data = []
    for i in range(1000000):
        data.append(f"Item {i}" * 100)
    return "📈 Memory leak simulated (this might crash)"

# ----------------------------
# Legacy Routes (for backward compatibility)
# ----------------------------
@app.route("/external")
def external_legacy():
    return http_error(200)

@app.route("/http-error")
def http_error_legacy():
    return http_error(404)

@app.route("/crash")
def crash_legacy():
    return crash()

@app.route("/log-error")
def log_error():
    logging.error("This is a test error log")
    log_error_simulation('LOG', 'error', 'Test error log')
    return "📝 Logged error"

@app.route("/slow")
def slow_legacy():
    return slow_query()

@app.route("/db")
def db_test_legacy():
    return db_insert()

@app.route("/db-error")
def db_error_legacy():
    return db_constraint()

# ----------------------------
# Helper Functions
# ----------------------------
def log_error_simulation(error_type, category, details):
    """Log error simulations for analysis"""
    try:
        with engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO error_simulation_logs 
                    (error_type, category, timestamp, details) 
                    VALUES (:type, :category, :timestamp, :details)
                """),
                {
                    "type": error_type,
                    "category": category,
                    "timestamp": datetime.now(),
                    "details": details
                }
            )
            conn.commit()
    except:
        pass  # Don't let logging errors affect the main functionality

# ----------------------------
# Advanced Chaos Generator
# ----------------------------
class ChaosEngine:
    def __init__(self):
        self.running = True
        self.intensity = 0.3  # 30% error rate
        self.scenarios = [
            # (route, weight)
            ('/http/200', 70),   # 70% success
            ('/http/404', 5),    # 5% 404
            ('/http/500', 5),    # 5% 500
            ('/http/403', 3),    # 3% 403
            ('/http/429', 2),    # 2% rate limit
            ('/db/insert', 30),  # 30% success
            ('/db/constraint', 5), # 5% error
            ('/db/connection', 3), # 3% error
            ('/business/validation', 8), # 8% error
            ('/performance/slow', 10), # 10% slow
            ('/external/api', 15), # 15% external
            ('/external/timeout', 4) # 4% timeout
        ]
        
    def generate_event(self):
        """Generate weighted random event"""
        if random.random() > self.intensity:
            # Generate success event
            with app.test_client() as client:
                client.get('/http/200')
        else:
            # Generate error based on weights
            routes = []
            weights = []
            for route, weight in self.scenarios:
                if '200' not in route and 'insert' not in route:  # Only error routes
                    routes.append(route)
                    weights.append(weight)
            
            if routes:
                route = random.choices(routes, weights=weights, k=1)[0]
                with app.test_client() as client:
                    try:
                        client.get(route)
                    except:
                        pass
        
    def chaos_loop(self):
        """Main chaos loop"""
        while self.running:
            time.sleep(random.uniform(1, 5))
            self.generate_event()

# ----------------------------
# Start Chaos Engine
# ----------------------------
chaos_engine = ChaosEngine()

@app.route("/chaos/control", methods=['POST'])
def control_chaos():
    """Control chaos parameters"""
    data = request.json
    if 'intensity' in data:
        chaos_engine.intensity = float(data['intensity'])
    if 'running' in data:
        chaos_engine.running = data['running']
    return jsonify({"status": "ok", "intensity": chaos_engine.intensity})

# ----------------------------
# Run Server
# ----------------------------
if __name__ == "__main__":
    print("""
    🚀 Chaos Engineering Dashboard Started!
    =======================================
    📊 Simulating production-like errors
    🔥 Error categories: HTTP, Database, Business, Performance, External
    🤖 Automated chaos running in background
    
    Access the dashboard: http://localhost:5000
    =======================================
    """)
    
    # Start chaos in background
    chaos_thread = threading.Thread(target=chaos_engine.chaos_loop, daemon=True)
    chaos_thread.start()
    
    app.run(port=3000, debug=True, use_reloader=False)