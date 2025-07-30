import time
from typing import Callable, Any


def tyme(some_function) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = some_function(*args, **kwargs)
        total_time = time.perf_counter() - start_time
        print(
            f"Function '{some_function.__name__}{args}' took {total_time:.2f} seconds."
        )
        return result

    return wrapper
