import json
import os

class TimerBackend:
    def __init__(self, focus_minutes=25):
        self.focus_seconds = focus_minutes * 60
        self.time_left = self.focus_seconds
        self.total_focus_minutes = 0
        self.data_file = "whale_stats.json"
        self.load_data()

    def tick(self):
        if self.time_left > 0:
            self.time_left -= 1
            return True
        return False

    def get_time_str(self):
        m, s = divmod(self.time_left, 60)
        return f"{m:02d}:{s:02d}"

    def reset(self):
        self.time_left = self.focus_seconds

    def save_data(self, minutes):
        self.total_focus_minutes += minutes
        with open(self.data_file, "w") as f:
            json.dump({"total_minutes": self.total_focus_minutes}, f)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.total_focus_minutes = json.load(f).get("total_minutes", 0)

    def get_level(self):
        if self.total_focus_minutes < 60: return "初生小鲸"
        return "海洋领主"