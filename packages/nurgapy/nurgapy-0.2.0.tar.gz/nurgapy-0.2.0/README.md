# nurgapy

```bash  _   _                       ____
 | \ | |_   _ _ __ __ _  __ _|  _ \ _   _
 |  \| | | | | '__/ _` |/ _` | |_) | | | |
 | |\  | |_| | | | (_| | (_| |  __/| |_| |
 |_| \_|\__,_|_|  \__, |\__,_|_|    \__, |
                  |___/             |___/
```
---
📦 NurgaPy : A Small Convenience Python Library
---

NurgaPy is a small, convenient Python library designed to help you avoid copying code across multiple projects. It includes two main functions:

Currently, `nurgapy` library consists two functions:
- `tyme` - it is a small wrapper function, which is used for measuring execution time of functions. Also works for the class functions.
- `trackbar` - it is a simple progress bar, which just works without many imports. Inspired by [stackoverflow post](https://stackoverflow.com/a/34482761/15059130). There is well-known `tqdm` library, but it prevents user from using `print` statements. For simple use-cases this progress bar should be enough. There is another nice library `alive-progress`, which does not have this issue and many others. But I just wanted to have some simple progress bar, which lives in the single library with other convenience functions.

## Getting started 🚀

Install the [NurgaPy](https://pypi.org/project/nurgapy/) library using pip.
```
pip install nurgapy
```


### Examples 🌟

#### `tyme` function usage ⏳
```python
from nurgapy import tyme


@tyme
def my_pow(a: int, b: int):
    for _ in range(10000000):
        res = a**b
    return res
```

#### `trackbar` usage ⏲️

```python
for i in trackbar(range(10)):
    time.sleep(0.5)
```

For more usage examples check the [`examples`](/examples/) folder.

## Development and Architecture Docs 📚
If you want to get know more about how NurgaPy works, how to set up developement enviroment and how made architectural decisions behind, please check the [`docs`](/docs/docs.md).

## Roadmap 🗺️
- [x] ~~Add basic code~~
- [x] ~~Add pre-commit hook~~
    - Add more rules to pre-commit
- [x] ~~Add public API to the `init.py`~~
- [x] ~~Add tests~~
- [ ] Add tests automation [Nox](https://nox.thea.codes/en/stable/)
- [ ] Add badges
    - [ ] test coverage ([coveralls](https://coveralls.io/))
- [x] Add packaging
- [x] Publish nurgapy to pip
- [x] Add a runner, which automatically publishes a new version to pip
- [x] Add `documentation` folder
- [x] Create an `examples` folder

### Progress bar ⏲️
- [ ] Add percentages
- [ ] Flexible size
- [x] Progress bar runs in the independent thread
