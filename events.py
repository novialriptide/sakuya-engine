import pygame

class BaseEvent:
    """Do not use this.
    """
    def __init__(self, name, method, args=[], kwargs={}):
        self.name = name
        self.method = method
        self.args = args
        self.kwargs = kwargs

class WaitEvent(BaseEvent):
    def __init__(self, name, time: int, method, args=[], kwargs={}):
        super().__init__(name, method, args=args, kwargs=kwargs)
        self.time = time
        self.execute_time = time + pygame.time.get_ticks()

class RepeatEvent(BaseEvent):
    def __init__(self, name, method, args=[], kwargs={}):
        """The method must return false if it wishes to be removed
        from the event list.
        """
        super().__init__(name, method, args=args, kwargs=kwargs)

class EventSystem:
    def __init__(self):
        """Initiate the Event module, you should only use this once
        """
        self._methods = [] # List[BaseEvent]

    def add(self, event: BaseEvent):
        self._methods.append(event)
        
    def update(self, delta_time):
        """Updates the event system.
        
        Parameters:
            delta_time: The game's delta time.
        
        Returns:
            A dictionary with names of events that were executed and cancelled.

        """
        output = {"executed": [], "cancelled": []}

        for m in self._methods:
            if isinstance(m, WaitEvent) and pygame.time.get_ticks() >= m.execute_time:
                m.method(*m.args, **m.kwargs)
                self._methods.remove(m)
                output["cancelled"].append(m.name)
            
            if isinstance(m, RepeatEvent):
                if not m.method(*m.args, **m.kwargs):
                    self._methods.remove(m)
                    output["cancelled"].append(m.name)

            output["executed"].append(m.name)

        return output