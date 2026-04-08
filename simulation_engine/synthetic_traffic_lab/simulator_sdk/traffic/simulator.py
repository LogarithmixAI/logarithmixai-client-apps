import random
import time
from agent_sdk.error_patterns.patterns import PATTERNS

class TrafficSimulator:

    def __init__(self, intensity=1):
        self.intensity = intensity

    def run(self):
        for _ in range(self.intensity):
            action = random.choice(PATTERNS)
            try:
                action()
            except Exception:
                pass
            time.sleep(random.uniform(0.2, 1.5))