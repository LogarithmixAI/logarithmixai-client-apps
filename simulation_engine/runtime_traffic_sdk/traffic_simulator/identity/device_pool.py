import random


class DevicePool:

    def __init__(self):

        self.devices = {
            "mobile": 0.6,
            "desktop": 0.35,
            "tablet": 0.05
        }

        self.types = list(self.devices.keys())
        self.weights = list(self.devices.values())

    def random_device(self):

        return random.choices(
            self.types,
            weights=self.weights
        )[0]