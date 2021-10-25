import pygame

class event:
    def __init__(self, time: int, method, args=[], kwargs={}):
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.time = time
        self.execute_time = time + pygame.time.get_ticks()

class time:
    def __init__(self):
        self._methods = []

    def wait(self, event: event):
        self._methods.append(event)
        
    def update(self):
        for m in self._methods:
            if pygame.time.get_ticks() >= m.execute_time:
                m.method(*m.args, **m.kwargs)
                self._methods.remove(m)
        