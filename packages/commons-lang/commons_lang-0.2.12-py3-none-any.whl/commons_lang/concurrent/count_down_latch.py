from threading import Lock, Event


class CountDownLatch:

    def __init__(self, count: int = 1):
        self.count = count
        self.lock = Lock()
        self.event = Event()

        if self.count <= 0:
            self.event.set()

    def count_down(self) -> None:
        with self.lock:
            if self.count > 0:
                self.count -= 1
                if self.count == 0:
                    self.event.set()

    def wait(self, timeout=None) -> bool:
        return self.event.wait(timeout)

    def get_count(self) -> int:
        with self.lock:
            return self.count

    def reset(self, count: int = 1) -> None:
        with self.lock:
            self.count = count
            if count > 0:
                self.event.clear()
            else:
                self.event.set()
