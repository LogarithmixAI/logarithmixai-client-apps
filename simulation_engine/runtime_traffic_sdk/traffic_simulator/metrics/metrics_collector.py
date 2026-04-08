import time
import threading


class MetricsCollector:

    def __init__(self):

        self.total_requests = 0
        self.errors = 0
        self.total_latency = 0

        self.start_time = time.time()
        self.lock = threading.Lock()

    def record(self, latency, status):

        with self.lock:

            self.total_requests += 1
            self.total_latency += latency

            if status >= 400:
                self.errors += 1

    def snapshot(self):

        elapsed = time.time() - self.start_time

        if elapsed == 0:
            return

        rps = self.total_requests / elapsed
        avg_latency = 0

        if self.total_requests > 0:
            avg_latency = self.total_latency / self.total_requests

        return {
            "rps": round(rps, 2),
            "requests": self.total_requests,
            "errors": self.errors,
            "avg_latency": round(avg_latency, 2)
        }

class MetricsReporter:

    def __init__(self, collector, interval=5):

        self.collector = collector
        self.interval = interval
        self.running = True

    def start(self):

        while self.running:

            time.sleep(self.interval)

            data = self.collector.snapshot()

            if data:

                print(
                    f"[METRICS] RPS={data['rps']} "
                    f"REQ={data['requests']} "
                    f"ERR={data['errors']} "
                    f"LAT={data['avg_latency']}ms"
                )