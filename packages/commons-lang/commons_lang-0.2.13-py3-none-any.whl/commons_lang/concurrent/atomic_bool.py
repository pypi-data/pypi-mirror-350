import threading
from typing import Optional


class AtomicBool:

    def __init__(self, initial_value: bool = False):
        self._value = initial_value
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._cached_value = initial_value
        self._cache_valid = True

    def set(self, value: bool) -> 'AtomicBool':
        with self._condition:
            if self._value != value:
                self._value = value
                self._cached_value = value
                self._cache_valid = True
                self._condition.notify_all()
        return self

    def get(self) -> bool:
        if self._cache_valid:
            return self._cached_value

        with self._lock:
            self._cached_value = self._value
            self._cache_valid = True
            return self._value

    def get_and_set(self, new_value: bool) -> bool:
        """原子地获取旧值并设置新值（修复返回值一致性）"""
        with self._condition:
            old_value = self._value
            if self._value != new_value:
                self._value = new_value
                self._cached_value = new_value
                self._cache_valid = True
                self._condition.notify_all()
            return old_value

    def compare_and_set(self, expected: bool, new_value: bool) -> bool:
        """原子地比较并设置（CAS操作）"""
        with self._condition:
            if self._value == expected:
                if self._value != new_value:
                    self._value = new_value
                    self._cached_value = new_value
                    self._cache_valid = True
                    self._condition.notify_all()
                return True
            return False

    def compare_and_set_weak(self, expected: bool, new_value: bool) -> tuple[bool, bool]:
        """弱CAS操作，返回(是否成功, 当前实际值)"""
        with self._condition:
            current = self._value
            if current == expected:
                if current != new_value:
                    self._value = new_value
                    self._cached_value = new_value
                    self._cache_valid = True
                    self._condition.notify_all()
                return True, new_value
            return False, current

    def toggle(self) -> bool:
        """原子地切换值，返回新值"""
        with self._condition:
            self._value = not self._value
            self._cached_value = self._value
            self._cache_valid = True
            new_value = self._value
            self._condition.notify_all()
            return new_value

    def wait_for(self, value: bool, timeout: Optional[float] = None) -> bool:
        """等待值变为指定值"""
        with self._condition:
            start_time = time.time() if timeout else None

            while self._value != value:
                if timeout:
                    remaining = timeout - (time.time() - start_time)
                    if remaining <= 0:
                        return False
                    if not self._condition.wait(remaining):
                        return False
                else:
                    self._condition.wait()

            return True

    def wait_for_true(self, timeout: Optional[float] = None) -> bool:
        """等待值变为True"""
        return self.wait_for(True, timeout)

    def wait_for_false(self, timeout: Optional[float] = None) -> bool:
        """等待值变为False"""
        return self.wait_for(False, timeout)

    def __bool__(self):
        """修复4: 优化bool转换性能"""
        return self.get()

    def __str__(self):
        return str(self.get())

    def __repr__(self):
        return f"AtomicBool({self.get()})"

    def __enter__(self):
        """上下文管理器支持"""
        self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器支持"""
        self._lock.release()
