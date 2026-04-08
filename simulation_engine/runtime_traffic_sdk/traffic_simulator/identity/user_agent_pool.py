import random


class UserAgentPool:

    def __init__(self):

        self.mobile_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
            "Mozilla/5.0 (Linux; Android 12)",
        ]

        self.desktop_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        ]

        self.tablet_agents = [
            "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)"
        ]

    def get_agent(self, device):

        if device == "mobile":
            return random.choice(self.mobile_agents)

        if device == "desktop":
            return random.choice(self.desktop_agents)

        return random.choice(self.tablet_agents)