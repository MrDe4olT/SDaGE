import json
import os


class SaveManager:
    def __init__(self, path="data/save.json"):
        self.path = path

    def load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_day(self):
        return self.load().get("day", 1)

    def set_day(self, day):
        self.save({"day": day})

    def next_day(self):
        day = self.get_day() + 1
        self.set_day(day)
        return day

    def has_save(self):
        return os.path.exists(self.path)