# sag_py_cache_decorator
[![Maintainability][codeclimate-image]][codeclimate-url]
[![Coverage Status][coveralls-image]][coveralls-url]
[![Known Vulnerabilities][snyk-image]][snyk-url]

A cache annotation that can be used to cache calls to a method

## What it does
- Caches calls to methods if the same parameters are used
- Removes the least recently used cache item if a optional maximum is reached
- Supports sync and async functions
- Possibility to skip the cache by parameter
- Possibility to clear the cache entirely or for one set of parameters

### Installation
pip install sag-py-cache-decorator

## How to use
```python
from sag_py_cache_decorator.lru_cache import lru_cache

@lru_cache(maxsize=3)
def my_function(str: str, str2: str) -> str:
    return f"{str}-{str2}"
```

This is the regular use case of the cache.

Available decorator arguments:

| Argument | Description                                                                                                                | Default |
|----------|----------------------------------------------------------------------------------------------------------------------------|---------|
| maxsize  | If this size is reached, the least recently used cache item will be removed. Can be set to None to have a unlimited cache. | 128     |

```python
from sag_py_cache_decorator.lru_cache import lru_cache

@lru_cache(maxsize=3)
def my_function(
    str: str,
    lru_clear_cache: bool = False,
) -> str:
    return f"{str}-{str2}"

my_function("one")
my_function("two")
# Before executing the next function the cache is cleared and then
# rebuilt with the results of three and four because of lru_clear_cache = True
my_function("three", lru_clear_cache = True)
my_function("four")
```
Available function arguments:
| Argument            | Description                                                                                                                           | Default |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------|---------|
| lru_use_cache       | If set to false, the function call skips the cache. Existing cached items are ignored and new ones are not written for that call.     | True    |
| lru_clear_cache     | If set to true, the cache is cleared entirely before executing the method. The result of the call is then cached again.               | False   |
| lru_clear_arg_cache | If set to true, the result for this set of parameters is removed from cache(if present). The result of the call is then cached again. | False   |

## How to start developing

### With vscode

Just install vscode with dev containers extension. All required extensions and configurations are prepared automatically.

### With pycharm

* Install latest pycharm
* Install pycharm plugin BlackConnect
* Install pycharm plugin Mypy
* Configure the python interpreter/venv
* pip install requirements-dev.txt
* pip install black[d]
* Ctl+Alt+S => Check Tools => BlackConnect => Trigger when saving changed files
* Ctl+Alt+S => Check Tools => BlackConnect => Trigger on code reformat
* Ctl+Alt+S => Click Tools => BlackConnect => "Load from pyproject.yaml" (ensure line length is 120)
* Ctl+Alt+S => Click Tools => BlackConnect => Configure path to the blackd.exe at the "local instance" config (e.g. C:\Python310\Scripts\blackd.exe)
* Ctl+Alt+S => Click Tools => Actions on save => Reformat code
* Restart pycharm

## How to publish
* Update the version in setup.py and commit your change
* Create a tag with the same version number
* Let github do the rest

## How to test

To avoid publishing to pypi unnecessarily you can do as follows

* Tag your branch however you like
* Use the chosen tag in the requirements.txt-file of the project you want to test this library in, eg. `sag_py_cache_decorator==<your tag>`
* Rebuild/redeploy your project

[codeclimate-image]:https://api.codeclimate.com/v1/badges/e29dcd8f76877962c93b/maintainability
[codeclimate-url]:https://codeclimate.com/github/SamhammerAG/sag_py_cache_decorator/maintainability
[coveralls-image]:https://coveralls.io/repos/github/SamhammerAG/sag_py_cache_decorator/badge.svg?branch=master
[coveralls-url]:https://coveralls.io/github/SamhammerAG/sag_py_cache_decorator?branch=master
[snyk-image]:https://snyk.io/test/github/SamhammerAG/sag_py_cache_decorator/badge.svg
[snyk-url]:https://snyk.io/test/github/SamhammerAG/sag_py_cache_decorator
