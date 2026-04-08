import requests
import time

from traffic_simulator.identity.header_generator import HeaderGenerator


class HTTPClient:

    def __init__(self, base_url):

        self.base_url = base_url
        self.header_gen = HeaderGenerator()

    def send_request(self, endpoint, session, method, thread):

        url = self.base_url + endpoint
        headers = self.header_gen.generate()

        cookies = {
            "user_id": session["user_id"],
            "session_id": session["session_id"]
        }

        start = time.time()
        try:


            
            if method == "POST":

                payload = self.generate_payload(endpoint)

                r = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    cookies=cookies,
                    timeout = (2, 5)
                )

            else:

                r = requests.get(
                    url,
                    headers=headers,
                    cookies=cookies,
                    timeout = (2, 5)
                )

            latency = (time.time() - start) * 1000

            return {
                "status": r.status_code,
                "latency_ms": int(latency),
                "method" : method,
                "worker_thread" : thread,
                "user_id": session['user_id']
            }

        except Exception as e:
            latency = (time.time() - start) * 1000
            return {
                "status": 500,
                "latency_ms": latency,
                "error": str(e),
                "method" : method,
                "thread" : thread
            }

    def generate_payload(self, path):

        if path == "/login":
            return {
                "username": random.choice(["alice", "bob", "john"])
            }

        if path == "/cart/add":
            return {
                "product_id": random.randint(1, 10),
                "qty": 1
            }

        if path == "/checkout":
            return {
                "payment": "card",
                "address": "test address"
            }

        return {}