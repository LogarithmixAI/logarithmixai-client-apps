from flask import Flask, request, jsonify, session
from agent_sdk import Agent, monitor_performance
import random
import logging
import sqlite3
import time
import requests
import random
from sqlalchemy import create_engine, text

app = Flask(__name__)

# engine = create_engine("sqlite:///testing.db")

# with engine.connect() as conn:
#     conn.execute(text("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)"))
#     conn.commit()

def get_db():
    return sqlite3.connect("testing.db", check_same_thread=False)

app.secret_key = "test-secret"

Agent.init(
    api_key="demo-key",
    api_secret="super-secret",
    endpoint="http://127.0.0.1:8000/api/logs",  
    project="client-test-app",
    framework="flask",
    app=app,
    enable_http=True,
    enable_logging=True,
    enable_exceptions=True,
    enable_performance=True
)

def maybe_fail():

    r = random.random()

    if r < 0.05:
        return jsonify({"error": "temporary failure"}), 500

    if r < 0.1:
        return jsonify({"error": "service unavailable"}), 503

    return None

@app.route("/")
def home():
    return jsonify({"message": "welcome"})

@app.route("/products")
def products():

    db = get_db()
    cur = db.cursor()

    try:

        cur.execute("CREATE TABLE IF NOT EXISTS products(id INTEGER)")

        if random.random() < 0.1:
            x = None
            x["error"]  # TypeError

        cur.execute("SELECT * FROM products")

    except Exception:

        logging.exception("Products processing failed")
        return {"error": "internal processing failure"}, 500

    finally:
        db.close()

    return {"products": []}

@app.route("/product/<pid>")
def product(pid):

    try:
        pid = int(pid)
    except:
        return jsonify({"error": "invalid product id"}), 400

    if pid > 100:
        return jsonify({"error": "product not found"}), 404

    return jsonify({"product": pid})

@app.route("/cart")
def cart():

    if "user" not in session:
        return jsonify({"error": "login required"}), 401

    return jsonify({"cart": []})

@app.route("/checkout", methods=["POST", "GET"])
def checkout():

    db = get_db()
    cur = db.cursor()

    try:

        if random.random() < 0.15:
            price = "100"
            total = price + 50   # TypeError

        cur.execute("CREATE TABLE IF NOT EXISTS orders(id INTEGER)")
        cur.execute("INSERT INTO orders VALUES(1)")
        db.commit()

    except Exception:

        logging.exception("Checkout failure")
        return {"error": "checkout processing failed"}, 500

    finally:
        db.close()

    return {"status": "order placed"}

@app.route("/search")
def search():

    q = request.args.get("q")

    try:

        if not q:
            return {"error": "query parameter required"}, 400

        if random.random() < 0.1:
            data = {"query": q}
            return {"len": len(data["missing"])}

    except Exception:

        logging.exception("Search processing failed")
        return {"error": "search engine failure"}, 500

    return {"results": []}

@app.route("/db")
def db_insert():

    err = maybe_fail()
    if err:
        return err

    conn = get_db()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT)")
    cur.execute("INSERT INTO users VALUES('John')")

    conn.commit()
    conn.close()

    return jsonify({"db": "inserted"})

@app.route("/db-error")
def db_error():

    conn = get_db()
    cur = conn.cursor()

    # invalid query
    cur.execute("INSERT INTO invalid_table VALUES(1)")

    conn.commit()
    conn.close()

    return "should fail"

@app.route("/login", methods=["POST"])
def login():

    username = request.json.get("username")

    if not username:
        return jsonify({"error": "username required"}), 400

    session["user"] = username

    return jsonify({"status": "logged in"})

@app.route("/dashboard")
def dashboard():

    try:

        if "user" not in session:
            return {"error": "unauthorized"}, 401

        if random.random() < 0.1:
            user = None
            return {"name": user["name"]}

    except Exception:

        logging.exception("Dashboard rendering error")
        return {"error": "dashboard failure"}, 500

    return {"dashboard": "data"}

@app.route("/admin")
def admin():

    if session.get("role") != "admin":
        return {"error": "forbidden"}, 403

    return {"admin": "panel"}

@app.route("/orders")
def orders():

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("SELECT * FROM orders")
    except:
        logging.error("Database query failed")
        return {"error": "database failure"}, 500

    return {"orders": []}

@app.route("/analytics")
def analytics():

    try:

        time.sleep(random.uniform(0.3, 1.2))

        if random.random() < 0.1:
            arr = []
            return {"value": arr[10]}

    except Exception:

        logging.exception("Analytics computation failed")
        return {"error": "analytics error"}, 500

    return {"stats": "ok"}

@app.route("/login-redirect", methods=["POST"])
def login_redirect():

    session["user"] = "demo"

    return "", 302, {"Location": "/dashboard"}

@app.route("/sale")
def sale():

    return "", 307, {"Location": "/products"}

@app.route("/external-payment")
def external_payment():

    try:

        r = requests.get("http://localhost:9999/payment")

        return {"payment": r.status_code}

    except Exception:

        logging.exception("Payment service unreachable")

        return {"error": "payment gateway unreachable"}, 502

@app.route("/external-slow")
def external_slow():

    r = requests.get("https://httpbin.org/delay/2")

    return {"status": r.status_code}

@app.route("/loop")
def loop():

    return "", 302, {"Location": "/loop"}

@app.errorhandler(404)
def not_found(e):

    logging.warning("User accessed invalid route")

    return {
        "error": "route not found",
        "hint": "check URL spelling"
    }, 404

@app.route("/api/payment")
def payment():

    token = request.headers.get("Authorization")

    if not token:
        return {"error": "missing token"}, 401

    return {"payment": "processed"}

@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return {"error": "file missing"}, 400

    return {"status": "uploaded"}

@app.route("/blog")
def blog():

    page = request.args.get("page", 1)

    try:
        page = int(page)
    except:
        return {"error": "invalid page"}, 400

    return {
        "page": page,
        "posts": ["post1", "post2", "post3"]
    }

@app.route("/products/page/<int:p>")
def product_page(p):

    if p > 50:
        return {"error": "page limit"}, 404

    return {
        "page": p, 
        "products": []
    }

@app.route("/sitemap.xml")
def sitemap():

    return {
        "urls": [
            "/",
            "/products",
            "/blog",
            "/search"
        ]
    }

@app.route("/robots.txt")
def robots():

    return "User-agent: *\nAllow: /\nDisallow: /admin"

@app.route("/category/<name>")
def category(name):

    page = request.args.get("page", 1)

    return {
        "category": name,
        "page": page
    }

@app.route("/cart/add", methods=["POST"])
def add_to_cart():

    product_id = request.json.get("product_id")

    if not product_id:
        return {"error": "product_id required"}, 400

    return {"status": "added"}

@app.route("/crawl-check")
def crawl_check():

    if random.random() < 0.2:
        return {"error": "too many requests"}, 429

    return {"status": "ok"}

@app.route("/feed")
def feed():

    cursor = request.args.get("cursor", "0")

    return {
        "cursor": cursor,
        "items": ["item1", "item2", "item3"]
    }


if __name__ == "__main__":
    app.run(port=3000, debug=False, use_reloader=False)

