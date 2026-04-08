import uuid
class BotBehavior:

    def __init__(self, crawler):
        self.crawler = crawler
        self.bot_id = f'bot_{str(uuid.uuid4())}'
    
    def identity(self):
        return{
                    "user_id": self.bot_id,
                    "session_id": None
            }

    def next_action(self):

        endpoint = self.crawler.next_endpoint()
        return endpoint, "GET"