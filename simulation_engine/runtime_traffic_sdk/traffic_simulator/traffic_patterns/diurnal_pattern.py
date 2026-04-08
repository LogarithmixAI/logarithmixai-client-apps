from datetime import datetime
from zoneinfo import ZoneInfo
import math


class DiurnalPattern:

    def __init__(self, base_rate):
        self.base_rate = base_rate

    def current_rate(self):

        now = datetime.now(ZoneInfo("Asia/Kolkata"))

        hour = now.hour + now.minute/60 + now.second/3600
        weekday = now.weekday()   # 0=Mon, 6=Sun

        # ---- Day/Night traffic curve ----
        diurnal_factor = 0.5 + 0.5 * math.sin((hour - 6) * math.pi / 12)

        # ---- Weekday / Weekend adjustment ----
        if weekday < 5:          # Mon–Fri
            day_factor = 1.0
        elif weekday == 5:       # Saturday
            day_factor = 0.7
        else:                    # Sunday
            day_factor = 0.5

        rate = self.base_rate * (0.3 + diurnal_factor) * day_factor

        return max(rate, 0.1)