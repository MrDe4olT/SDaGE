import json


class DifficultyManager:
    def __init__(self, path="data/difficulty.json"):
        self.path = path

        with open(self.path, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def get_day_config(self, day):
        difficulty = self.data["difficulty"]
        per_day = self.data["per_day"]

        return {
            "TASK_FAIL_CHANCE": difficulty["TASK_FAIL_CHANCE"] + (day - 1) * per_day["TASK_FAIL_CHANCE"],
            "ANXIETY_PASSIVE_GAIN_PER_SEC": difficulty["ANXIETY_PASSIVE_GAIN_PER_SEC"] + (day - 1) * per_day["ANXIETY_PASSIVE_GAIN_PER_SEC"],
            "ANXIETY_RELIEF_PER_SEC": difficulty["ANXIETY_RELIEF_PER_SEC"] + (day - 1) * per_day["ANXIETY_RELIEF_PER_SEC"]
        }