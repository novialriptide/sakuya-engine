import pygame

class Event:
    def __init__(self, time: int, method, args=[], kwargs={}):
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.time = time
        self.execute_time = time + pygame.time.get_ticks()

class Time:
    def __init__(self):
        """
        Initiate the Time module, you should only use this once
        """
        self._methods = []

    def wait(self, event: Event):
        self._methods.append(event)
        
    def update(self):
        for m in self._methods:
            if pygame.time.get_ticks() >= m.execute_time:
                m.method(*m.args, **m.kwargs)
                self._methods.remove(m)
        