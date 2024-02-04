import time


class CronosClock:

    def __init__(self) -> None:
        self.time_reference = time.perf_counter()

    def has_seconds_passed(self, time_sec: float) -> bool:
        return time_sec <= time.perf_counter() - self.time_reference

    def restart_time(self) -> None:
        self.time_reference = time.perf_counter()

    def get_time_passed(self) -> float:
        return time.perf_counter() - self.time_reference

    def watch_variable(self) -> None:
        raise NotImplemented
