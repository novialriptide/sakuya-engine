import json
import pygame

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
        self._is_recording = True
        self._executed_ticks = []

    @property
    def is_recording(self):
        return self._is_recording

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

    def load(self, path):
        self.frames = []
        data = json.load(open(path))
        for f in data["frames"]:
            self.frames.append(Frame(f["tick"], f["methods"]))

    def update(self, current_tick):
        if current_tick not in self._executed_ticks:
            f = self.search_frame(current_tick)
            if f != None:
                for m in f.methods:
                    self.methods[m]()
                self._executed_ticks.append(current_tick)