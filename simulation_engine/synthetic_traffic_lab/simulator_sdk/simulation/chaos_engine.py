import random
import threading
import time
import requests
import logging

class ChaosEngine:

    def __init__(self, base_url):
        self.base_url = base_url
        self.running = False

        # weighted traffic pattern (production style)
        self.routes = [
            ("/external", 40),
            ("/db", 25),
            ("/slow", 15),
            ("/log-error", 8),
            ("/http-error", 6),
            ("/db-error", 4),
            ("/crash", 2)
        ]

    def pick_route(self):
        routes, weights = zip(*self.routes)
        return random.choices(routes, weights)[0]

    def trigger(self):
        route = self.pick_route()

        try:
            requests.get(self.base_url + route, timeout=5)
        except Exception as e:
            logging.error(f"Chaos error: {e}")

    def start(self, interval=(1,4)):
        self.running = True

        def loop():
            while self.running:
                self.trigger()
                time.sleep(random.uniform(*interval))

        threading.Thread(target=loop, daemon=True).start()

    def stop(self):
        self.running = False