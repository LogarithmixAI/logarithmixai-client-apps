import random
import uuid

class Session:

    def __init__(self, user):
        self.id = f'Sn_{str(uuid.uuid4())}'
        self.user = user
        self.user_id = self.user.id
        self.active = True
        self.nav = user.nav
        self.current_page = "/"
        self.actions = 0
        self.max_actions = random.randint(5, 20)

    def next_request(self):

        next_page = self.nav.next_page(self.current_page)

        self.current_page = next_page
        self.actions += 1

        return next_page

    def expired(self): 
        if self.actions >= self.max_actions:
            self.active = False
            return True 