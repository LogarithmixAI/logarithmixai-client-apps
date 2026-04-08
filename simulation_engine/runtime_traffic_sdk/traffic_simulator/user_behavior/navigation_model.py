import random


class NavigationModel:

    def __init__(self):

        self.graph = {

            "/": [
                ("/products", 0.6),
                ("/search?q=phone", 0.25),
                ("/blog?page=1", 0.15)
            ],

            "/products": [
                ("/product/1", 0.4),
                ("/product/2", 0.4),
                ("/products/page/1", 0.2)
            ],

            "/products/page/1": [
                ("/product/1", 0.4),
                ("/product/2", 0.4),
                ("/products/page/2", 0.2)
            ],

            "/products/page/2": [
                ("/product/1", 0.5),
                ("/product/2", 0.3),
                ("/products", 0.2)
            ],

            "/product/1": [
                ("/cart", 0.4),
                ("/products", 0.4),
                ("/search?q=phone", 0.2)
            ],

            "/product/2": [
                ("/cart", 0.4),
                ("/products", 0.4),
                ("/search?q=laptop", 0.2)
            ],

            "/cart": [
                ("/checkout", 0.5),
                ("/products", 0.3),
                ("/", 0.2)
            ],

            "/blog?page=1": [
                ("/blog?page=2", 0.7),
                ("/", 0.3)
            ],

            "/blog?page=2": [
                ("/blog?page=1", 0.5),
                ("/", 0.5)
            ],

            "/search?q=phone": [
                ("/product/1", 0.5),
                ("/product/2", 0.3),
                ("/products", 0.2)
            ],

            "/search?q=laptop": [
                ("/product/1", 0.4),
                ("/product/2", 0.4),
                ("/products", 0.2)
            ]
        }

    def next_page(self, current):

        options = self.graph.get(current, [("/", 1)])

        pages = [p for p, _ in options]
        weights = [w for _, w in options]

        return random.choices(pages, weights=weights, k=1)[0]