import json
import os


class SaveManager:
    def __init__(self, path="data/save.json"):
        self.path = path

    def load(self):
        if not os.path.exists(self.path):
            return {"day": 1, "has_save": False}

        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_day(self):
        return self.load().get("day", 1)

    def set_day(self, day):
        data = self.load()
        data["day"] = day
        self.save(data)

    def next_day(self):
        day = self.get_day() + 1
        self.set_day(day)
        return day

    def has_save(self):
        return self.load().get("has_save", False)
    
    def set_has_save(self, value: bool):
        data = self.load()
        data["has_save"] = value
        self.save(data)