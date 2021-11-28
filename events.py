import pygame

class BaseEvent:
    """Do not use this.
    """
    def __init__(self, method, args=[], kwargs={}):
        self.method = method
        self.args = args
        self.kwargs = kwargs

class WaitEvent(BaseEvent):
    def __init__(self, time: int, method, args=[], kwargs={}):
        super().__init__(method, args=args, kwargs=kwargs)
        self.time = time
        self.execute_time = time + pygame.time.get_ticks()

class RepeatEvent(BaseEvent):
    def __init__(self, method, args=[], kwargs={}):
        super().__init__(method, args=args, kwargs=kwargs)

class EventSystem:
    def __init__(self):
        """
        Initiate the Event module, you should only use this once
        """
        self._methods = [] # List[BaseEvent]

    def wait(self, event: BaseEvent):
        self._methods.append(event)
        
    def update(self):
        for m in self._methods:
            if isinstance(m, WaitEvent) and pygame.time.get_ticks() >= m.execute_time:
                m.method(*m.args, **m.kwargs)
                self._methods.remove(m)
            
            if isinstance(m, RepeatEvent):
                m.method(*m.args, **m.kwargs)