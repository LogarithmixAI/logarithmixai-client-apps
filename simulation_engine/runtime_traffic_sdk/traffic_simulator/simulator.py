from traffic_simulator.engine.traffic_engine import TrafficEngine
from traffic_simulator.config.simulator_config import SimulatorConfig

load_profile = [
            (60, 2),   # normal
            (30, 9),  # peak
            (15, 15), # burst
            (60, 6)    # cooldown
        ]

class TrafficSimulator:

    def __init__(
        self,
        base_url: str,
        users: int = 100,
        duration: int = 60,
        max_concurrency=5, 
        debug=True, 
        user_request_rate=5, 
        load_profile= [(60, 2),(30, 9),(15, 11),(60, 6)],
        bot_request_rate = 5,
        max_rps=20
    ):
        self.config = SimulatorConfig(
            base_url=base_url,
            users=users,
            duration=duration,
            max_concurrency=max_concurrency, 
            debug=debug, 
            user_request_rate=user_request_rate, 
            load_profile=load_profile,
            bot_request_rate = bot_request_rate,
            max_rps=max_rps

        )

        self.engine = TrafficEngine(self.config)

    def start(self):
        print("🚀 Starting Traffic Simulator")
        self.engine.start()