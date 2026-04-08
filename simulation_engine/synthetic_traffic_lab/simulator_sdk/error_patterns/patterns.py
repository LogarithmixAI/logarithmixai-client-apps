import random
import time
import logging
import requests

def http_spike():
    requests.get("https://httpbin.org/status/500")

def db_timeout(engine):
    time.sleep(2)
    with engine.connect() as conn:
        conn.execute("SELECT 1")

def exception_chain():
    try:
        x = 1 / 0
    except:
        raise RuntimeError("Chained failure")

def memory_pressure():
    data = []
    for _ in range(100000):
        data.append("x" * 1000)

def log_noise():
    logging.warning("Traffic noise warning")

PATTERNS = [
    http_spike,
    exception_chain,
    memory_pressure,
    log_noise,
]