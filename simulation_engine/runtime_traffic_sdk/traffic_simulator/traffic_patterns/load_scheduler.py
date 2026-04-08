import time


class LoadScheduler:

    def __init__(self, profile):

        """
        profile example:
        [
            (60, 20),   # 60 seconds → 20 rps
            (30, 200),  # 30 seconds → 200 rps
            (60, 40)    # 60 seconds → 40 rps
        ]
        """

        self.profile = profile
        self.start_time = time.time()

    def current_rate(self):

        elapsed = time.time() - self.start_time

        total = 0

        for duration, rate in self.profile:

            total += duration

            if elapsed <= total:
                return rate

        return self.profile[-1][1]