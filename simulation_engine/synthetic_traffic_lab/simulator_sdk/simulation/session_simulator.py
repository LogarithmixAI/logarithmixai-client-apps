import threading
import random
import time
import requests
import uuid

class SessionSimulator:

    def __init__(self, base_url, users=5):
        self.base_url = base_url
        self.users = users
        self.running = False

        self.routes = [
            "/external",
            "/db",
            "/slow",
            "/log-error",
            "/http-error"
        ]

    def simulate_user(self, user_id):

        while self.running:
            route = random.choice(self.routes)

            headers = {
                "x-session-id": str(uuid.uuid4()),
                "x-user-id": str(user_id)
            }

            try:
                requests.get(self.base_url + route, headers=headers, timeout=5)
            except:
                pass

            time.sleep(random.uniform(1,3))

    def start(self):
        self.running = True

        for i in range(self.users):
            threading.Thread(
                target=self.simulate_user,
                args=(i,),
                daemon=True
            ).start()

    def stop(self):
        self.running = False