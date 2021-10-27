import json

class Frame:
    def __init__(self, tick: int, methods=[]):
        """
        :param int tick:
        :param int[] methods:
        """
        self.methods = methods
        self.tick = tick

    def to_dict(self):
        data = {"methods": None, "tick": None}
        data["methods"] = self.methods
        data["tick"] = self.tick

        return data

class Replay:
    def __init__(self):
        self.frames = []
        self.methods = []

    def search_frame(self, tick):
        for f in self.frames:
            if f.tick == tick:
                return f

    def save(self, path):
        data = {"frames": []}
        for f in self.frames:
            data["frames"].append(f.to_dict())

        with open(f"{path}.json", 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def update(self, current_tick):
        f = self.search_frame(current_tick)
        for m in f.methods: m()