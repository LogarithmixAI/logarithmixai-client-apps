import threading
import time
import requests

class TrafficSpike:

    def __init__(self, base_url):
        self.base_url = base_url

    def burst(self, requests_count=50):

        def hit():
            try:
                requests.get(self.base_url + "/external", timeout=3)
            except:
                pass

        threads = []

        for _ in range(requests_count):
            t = threading.Thread(target=hit)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def schedule_spike(self, every=30):

        def loop():
            while True:
                self.burst()
                time.sleep(every)

        threading.Thread(target=loop, daemon=True).start()