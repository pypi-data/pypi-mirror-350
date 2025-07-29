class Argument:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def to_dict(self):
        return {"key": self.key, "value": self.value}

    def __repr__(self):
        return f"Argument(key={self.key!r}, value={self.value!r})"


import time
from functools import wraps


def time_process(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        result = func(self, *args, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time

        if isinstance(result, tuple) and len(result) > 1 and isinstance(result[1], dict):
            debug_info = result[1]
            debug_info.setdefault("metrics", [])
            debug_info["metrics"].append({"key": "time", "value": execution_time})
            return result[0], debug_info
        else:
            return result

    return wrapper
