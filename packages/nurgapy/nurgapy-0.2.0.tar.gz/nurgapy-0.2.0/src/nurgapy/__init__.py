from nurgapy.tyme import tyme
from nurgapy.trackbar import trackbar


# module level doc-string
__doc__ = """
nurgapy - is a convenience library for Python.
=====================================================================

**nurgapy** is a Python package providing a number of convenience functions,
which are usually found in other libraries.

Main Features
-------------
Here are the things that nurgapy does:

  - Measuring the function execution time by using @timeit annotation.
  - Providing a simple progress bar with zero dependencies, which
  supports the print() statement.
"""

__all__ = [
    "tyme",
    "trackbar",
]
