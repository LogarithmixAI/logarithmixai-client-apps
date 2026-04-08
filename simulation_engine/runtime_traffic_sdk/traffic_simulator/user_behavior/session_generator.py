import random
import threading
from traffic_simulator.user_behavior.session import Session
from traffic_simulator.user_behavior.user import User

class SessionGenerator:

    def __init__(self, config):

        self.config = config
        self.users = [User() for _ in range(config.users)]
        self.inactive_users = self.users
        self.active_users = []
        self.lock = threading.Lock()

    def activate_user(self):

        with self.lock:

            if not self.inactive_users:
                print("no user activate")
                return None

            user = random.choice(self.inactive_users)

            self.inactive_users.remove(user)
            self.active_users.append(user)

        session = Session(user)
        return session
    
    def deactivate_user(self, user):

        with self.lock:

            if user in self.active_users:
                self.active_users.remove(user)

            self.inactive_users.append(user)

    def think_time(self):
        return random.uniform(
            self.config.think_time_min,
            self.config.think_time_max
        )



