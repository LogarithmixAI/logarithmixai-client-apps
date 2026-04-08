import random


class PoissonArrival:

    def __init__(self, rate_per_sec):

        self.rate = rate_per_sec

    def next_interval(self):

        return random.expovariate(self.rate)