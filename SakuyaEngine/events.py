"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from .clock import Clock


class BaseEvent:
    """Do not use this."""

    def __init__(self, name, method, args=[], kwargs={}):
        self.name = name
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.execute_time = None
        self.clock = None


class WaitEvent(BaseEvent):
    def __init__(self, name, time: int, method, args=[], kwargs={}):
        super().__init__(name, method, args=args, kwargs=kwargs)
        self.time = time


class RepeatEvent(BaseEvent):
    def __init__(self, name, method, args=[], kwargs={}, wait_time: int or None = None):
        """The method must return false if it wishes to be removed
        from the event list.
        """
        super().__init__(name, method, args=args, kwargs=kwargs)
        self.wait_time = wait_time


class EventSystem:
    def __init__(self, clock: Clock):
        """Initiate the Event module, you should only use this once"""
        self.clock = clock
        self._methods = []  # List[BaseEvent]

    def add(self, event: BaseEvent):
        self._methods.append(event)

    def update(self):
        """Updates the event system.

        Returns:
            A dictionary with names of events that were executed and cancelled.

        """
        output = {"executed": [], "cancelled": []}

        for m in self._methods:
            if isinstance(m, WaitEvent):
                if m.clock is None:
                    m.clock = self.clock
                    m.execute_time = m.time + self.clock.get_time()

                if self.clock.get_time() >= m.execute_time:
                    m.method(*m.args, **m.kwargs)
                    self._methods.remove(m)
                    output["cancelled"].append(m.name)

            if isinstance(m, RepeatEvent):
                if m.clock is None:
                    m.clock = self.clock
                    m.execute_time = m.wait_time + self.clock.get_time()

                if self.clock.get_time() >= m.execute_time or m.wait_time is None:
                    m.execute_time = m.wait_time + self.clock.get_time()
                    if not m.method(*m.args, **m.kwargs):
                        self._methods.remove(m)
                        output["cancelled"].append(m.name)

            output["executed"].append(m.name)

        return output
