import random
from traffic_simulator.endpoints.endpoint_model import Endpoint


class EndpointPool:

    def __init__(self):

        self.endpoints = [

            # ----------------
            # Core pages
            # ----------------
            Endpoint("/", 30, "light", "GET"),
            Endpoint("/products", 20, "medium", "GET"),
            Endpoint(f"/search?q={random.choice(['phone','laptop','tv'])}", 15, "heavy", "GET"),
            Endpoint("/cart", 8, "medium", "GET"),

            # checkout realistic POST
            Endpoint("/checkout", 5, "heavy", "POST"),

            # ----------------
            # Product browsing
            # ----------------
            Endpoint("/product/1", 5, "medium", "GET"),
            Endpoint("/product/2", 5, "medium", "GET"),

            # ----------------
            # Pagination / scrolling
            # ----------------
            Endpoint("/products/page/1", 3, "medium", "GET"),
            Endpoint("/products/page/2", 3, "medium", "GET"),

            # ----------------
            # Bot crawler pages
            # ----------------
            Endpoint("/blog?page=1", 2, "light", "GET"),
            Endpoint("/blog?page=2", 2, "light", "GET"),
            Endpoint("/feed?cursor=1", 2, "medium", "GET"),

            # ----------------
            # Auth related
            # ----------------
            Endpoint("/dashboard", 2, "medium", "GET"),
            Endpoint("/admin", 1, "heavy", "GET"),

            # login should be POST
            Endpoint("/login", 3, "medium", "POST"),
            Endpoint("/login", 3, "medium", "GET"),

            # ----------------
            # Cart actions
            # ----------------
            Endpoint("/cart/add", 4, "medium", "POST"),
            Endpoint("/cart/add", 4, "medium", "GET"),

            # ----------------
            # External API
            # ----------------
            Endpoint("/external", 2, "medium", "GET"),

            # ----------------
            # Typo / broken routes
            # ----------------
            Endpoint("/produts", 3, "light", "GET"),
            Endpoint("/cartt", 2, "light", "GET"),
            Endpoint("/seach", 2, "light", "GET"),

            Endpoint("/login-redirect", 6, "light", "POST"),
            Endpoint("/login-redirect", 6, "light", "GET"),
            Endpoint("/old-products", 5, "light", "GET"),
            Endpoint("/sale", 4, "light", "GET"),
            Endpoint("/sale", 4, "light", "POST"),

            Endpoint("/external-call", 7, "medium", "GET"),
            Endpoint("/external-payment", 8, "medium", "GET"),
            Endpoint("/external-payment", 3, "medium", "POST"),
            Endpoint("/api/sign_up?email=user123@gamil", 3, "medium", "GET"),
            Endpoint("/external-slow", 8, "heavy", "GET"),

        ]
        self.weights = [e.weight for e in self.endpoints]

    def next_endpoint(self):

        endpoint = random.choices(
            self.endpoints,
            weights=self.weights
        )[0]

        return endpoint