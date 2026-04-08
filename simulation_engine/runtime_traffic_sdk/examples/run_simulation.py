# from traffic_simulator.simulator import TrafficSimulator
from traffic_simulator import TrafficSimulator
sim = TrafficSimulator(
     base_url="http://127.0.0.1:5000",
    users=5,
    duration=30,
    max_concurrency= 4,
    # debug=False,
    debug=True,
    user_request_rate=5,
    load_profile= [
        (10, 2),   # normal
        (5, 9),  # peak
        (3, 15), # burst
        (10, 3)    # cooldown
    ],
)

sim.start()
