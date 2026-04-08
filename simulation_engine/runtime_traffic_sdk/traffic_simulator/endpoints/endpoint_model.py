class Endpoint:

    def __init__(self, path, weight=1, cost="light", method="GET"):

        self.path = path
        self.weight = weight
        self.cost = cost
        self.method = method