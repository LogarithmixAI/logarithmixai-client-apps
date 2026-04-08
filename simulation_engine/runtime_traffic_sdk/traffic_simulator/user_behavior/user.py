import random
import uuid
from traffic_simulator.user_behavior.navigation_model import NavigationModel

class User:

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.active = True
        self.sessions = []
        self.nav = NavigationModel()
        self.user_active_count = 0
 