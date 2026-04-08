import math

load_profile = [
            (60, 2),   # normal
            (30, 9),  # peak
            (15, 15), # burst
            (60, 6)    # cooldown
        ]

class SimulatorConfig:

    def __init__(
        self,
        base_url, users,
        duration, 
        max_concurrency=5, 
        debug=True, 
        user_request_rate=5, 
        load_profile=load_profile,
        bot_request_rate = 5,
        max_rps=20
        ):

        self.base_url = base_url
        self.users = users
        self.duration = duration
        self.debug = debug


        # requests per second
        self.request_rate = user_request_rate
        self.load_profile = load_profile
        self.bot_request_rate = bot_request_rate

        # think time (seconds)
        self.think_time_min = 0.5
        self.think_time_max = 3
        self.random_access_probability = 0.1
        self.max_rps = max_rps
        self.max_concurrency = max_concurrency
        self.user_workers = self.custom_round(0.5)
        self.api_workers = self.custom_round(0.25)
        self.bot_workers = self.custom_round(0.15)

    def custom_round(self, value):
        value = self.max_concurrency * value
        decimal = value - math.floor(value)

        if decimal >= 0.5:
            return math.ceil(value)
        else:
            return math.floor(value)
        