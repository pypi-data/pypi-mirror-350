import sys
from datetime import datetime
from datetime import timedelta
import threading
import time
from typing import Iterator, Any, TextIO, Sized


def chop_microseconds(delta: timedelta) -> timedelta:
    """
    Chop off the microseconds part of a timedelta object.
    Args:
        delta (timedelta): The timedelta object to chop.

    Returns:
        timedelta: A new timedelta object with microseconds chopped off.
    """
    return delta - timedelta(microseconds=delta.microseconds)


class TrackbarThread(threading.Thread):
    def __init__(self, it: Sized, prefix: str, size: int, out: TextIO) -> None:
        super().__init__()
        self.it = it
        self.prefix = prefix
        self.size = size
        self.out = out
        self.count = len(it)
        self.current_index = 0
        self.start_time = datetime.now()
        self.running = True

    def run(self) -> None:
        while self.running:
            elapsed_time = chop_microseconds(datetime.now() - self.start_time)
            self.show(self.current_index, elapsed_time)
            time.sleep(0.1)  # Update every 100ms

    def show(self, j: int, current_time: timedelta) -> None:
        x = int(self.size * j / self.count)
        bar = f"{self.prefix}[{u'█'*x}{('.'*(self.size-x))}] {j}/{self.count}"
        self.out.write(f"\r{current_time} {bar}\x1b[K ")  # Clear to end of line
        self.out.flush()

    def clear_line(self) -> None:
        self.out.write("\r\x1b[K")
        self.out.flush()

    def update_index(self, index: int) -> None:
        self.current_index = index

    def stop(self) -> None:
        self.running = False


def trackbar(it, prefix: str = "", size: int = 60, out=sys.stdout) -> Iterator[Any]:
    trackbar_thread = TrackbarThread(it, prefix, size, out)
    trackbar_thread.start()

    for i, item in enumerate(it):
        trackbar_thread.update_index(i + 1)
        yield item
        # If something is printed, clear the trackbar line first
        if hasattr(out, "isatty") and out.isatty():
            trackbar_thread.clear_line()

    trackbar_thread.stop()
    trackbar_thread.join()
    # Show the final state of the trackbar
    elapsed_time = chop_microseconds(datetime.now() - trackbar_thread.start_time)
    trackbar_thread.show(trackbar_thread.count, elapsed_time)
    out.write("\n")
    out.flush()
