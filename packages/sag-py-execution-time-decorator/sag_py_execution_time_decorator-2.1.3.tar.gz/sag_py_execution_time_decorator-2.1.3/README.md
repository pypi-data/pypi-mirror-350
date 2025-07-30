# sag_py_execution_time_decorator
[![Maintainability][codeclimate-image]][codeclimate-url]
[![Coverage Status][coveralls-image]][coveralls-url]
[![Known Vulnerabilities][snyk-image]][snyk-url]

A decorator for methods to log the execution time (sync and async)

## What it does
- Logs the execution time in milliseconds

Sample log entry:
```
decorated_sync_method took 1000 ms.
```

The entry contains "function_name" and "execution_time" as extra data.

## Installation
pip install sag-py-execution-time-decorator

## How to use
Decorate your methods like that:
```python
from sag_py_execution_time_decorator.execution_time_decorator import log_execution_time

@log_execution_time()
def decorated_sync_method(param: str) -> str:
    time.sleep(SLEEP_TIME_MS / 1000)
    return f"test: {param}"


@log_execution_time(log_level=logging.ERROR, log_params=("param",))
async def decorated_async_method(param: str) -> str:
    await asyncio.sleep(SLEEP_TIME_MS / 1000)
    return f"test: {param}"

```

Optional arguments:
| Argument    | Description                                                          | Default                  |
|-------------|----------------------------------------------------------------------|--------------------------|
| log_level   | The log level integar. Use logging.* constants                       | logging.INFO             |
| logger_name | The name of the logger that is internally used for logging.getLogger | execution_time_decorator |
| log_params  | A tuple of parameter names to be logged with their values in 'extra' | ()                       |

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
* Use the chosen tag in the requirements.txt-file of the project you want to test this library in, eg. `sag_py_execution_time_decorator==<your tag>`
* Rebuild/redeploy your project

[codeclimate-image]:https://api.codeclimate.com/v1/badges/fa4312e587c8185db077/maintainability
[codeclimate-url]:https://codeclimate.com/github/SamhammerAG/sag_py_execution_time_decorator/maintainability
[coveralls-image]:https://coveralls.io/repos/github/SamhammerAG/sag_py_execution_time_decorator/badge.svg?branch=master
[coveralls-url]:https://coveralls.io/github/SamhammerAG/sag_py_execution_time_decorator?branch=master
[snyk-image]:https://snyk.io/test/github/SamhammerAG/sag_py_execution_time_decorator/badge.svg
[snyk-url]:https://snyk.io/test/github/SamhammerAG/sag_py_execution_time_decorator