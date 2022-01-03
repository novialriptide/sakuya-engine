import time

class Clock:
    def __init__(self):
        self._accum = 0
        
        self._started_running_at = time.time()
        self._is_running = True
    
    @property
    def is_running(self):
        return self._is_running
        
    def resume(self):
        if not self._is_running:
            self._started_running_at = time.time()
            self._is_running = True
            
    def pause(self):
        if self._is_running:
            self._accum += time.time() - self._started_running_at
            self._is_running = False
    
    def get_time(self):
        if self._is_running:
            return (self._accum + time.time() - self._started_running_at) * 1000
        else:
            return self._accum * 1000