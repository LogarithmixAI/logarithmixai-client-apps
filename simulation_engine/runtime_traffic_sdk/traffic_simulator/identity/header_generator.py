import random

from traffic_simulator.identity.device_pool import DevicePool
from traffic_simulator.identity.user_agent_pool import UserAgentPool


class HeaderGenerator:

    def __init__(self):

        self.device_pool = DevicePool()
        self.ua_pool = UserAgentPool()

        self.languages = [
            "en-US",
            "en-GB",
            "hi-IN"
        ]

    def generate(self):

        device = self.device_pool.random_device()

        headers = {
            "User-Agent": self.ua_pool.get_agent(device),
            "Accept-Language": random.choice(self.languages),
            "Accept": "text/html",
            "Connection": "keep-alive"
        }

        return headers