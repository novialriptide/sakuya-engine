import time

__all__ = ["Clock"]


class Clock:
    def __init__(self, pause_upon_start: bool = False) -> None:
        self._accum = 0

        self._started_running_at = time.time()
        self._running = not pause_upon_start
        self._speed = 1

    @property
    def running(self) -> bool:
        return self._running

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, speed) -> None:
        self._accum += (time.time() - self._started_running_at) * self._speed
        self._started_running_at = time.time()
        self._speed = speed

    def reset(self) -> None:
        self._accum = 0
        self._started_running_at = time.time()

    def resume(self) -> bool:
        if not self._running:
            self._started_running_at = time.time()
            self._running = True

    def pause(self) -> bool:
        if self._running:
            self._accum += (time.time() - self._started_running_at) * self._speed
            self._running = False

    def get_time(self) -> float:
        """Returns time in milliseconds
        """
        if self._running:
            return (
                (self._accum + time.time() - self._started_running_at)
                * self._speed
                * 1000
            )
        else:
            return self._accum * 1000

    def set_time(self, val: int) -> None:
        """val must be milliseconds
        """
        self._accum = val / 1000
