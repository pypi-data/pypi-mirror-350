from functools import wraps

from .utils import _millis


class stopwatch:
    def __enter__(self):
        self.start = _millis()
        return self

    def __exit__(self, *args):
        pass

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _start = _millis()
            result = func(*args, **kwargs)
            _end = _millis()
            _func_name = func.__name__
            print(
                f'Function \'{_func_name}\' executed in {_end - _start:.4f} ms'
            )
            return result
        return wrapper

    @property
    def elapsed(self) -> float:
        """
        Returns the elapsed time in milliseconds
        since the stopwatch was started.
        """
        self.end = _millis()
        return self.end - self.start
