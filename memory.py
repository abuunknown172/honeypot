import json
import os

class Memory:
    def __init__(self, cid):
        self.file = f"mem_{cid}.json"
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                self.history = json.load(f)
        else:
            self.history = []

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        with open(self.file, "w") as f:
            json.dump(self.history, f)

    def get(self):
        return self.history
