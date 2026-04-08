import random


class BotCrawler:

    def __init__(self):

        self.blog_page = 1
        self.product_page = 1
        self.feed_cursor = 1

    def next_endpoint(self):

        mode = random.choice(["blog", "products", "feed"])

        if mode == "blog":

            endpoint = f"/blog?page={self.blog_page}"
            self.blog_page += 1

            if self.blog_page > 10:
                self.blog_page = 1

            return endpoint


        if mode == "products":

            endpoint = f"/products/page/{self.product_page}"
            self.product_page += 1

            if self.product_page > 20:
                self.product_page = 1

            return endpoint


        if mode == "feed":

            endpoint = f"/feed?cursor={self.feed_cursor}"
            self.feed_cursor += 1

            if self.feed_cursor > 15:
                self.feed_cursor = 1

            return endpoint