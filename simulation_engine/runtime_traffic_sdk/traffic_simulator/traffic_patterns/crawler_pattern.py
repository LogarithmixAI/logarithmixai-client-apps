import time
import random
class CrawlerPattern:

    def __init__(self, base_rate):
        self.crawling = False
        self.end_time = 0
        self.base_rate = base_rate

    def current_rate(self):

        now = time.time()
        
        if self.crawling and now < self.end_time:
            return self.base_rate

        r = random.random()

        if r < 0.08:
            self.crawling = True
            self.end_time = now + random.uniform(5,30)

        return 0