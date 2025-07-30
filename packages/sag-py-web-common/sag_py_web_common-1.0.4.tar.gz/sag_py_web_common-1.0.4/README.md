# sag_py_web_common

[![Maintainability][codeclimate-image]][codeclimate-url]
[![Coverage Status][coveralls-image]][coveralls-url]
[![Known Vulnerabilities][snyk-image]][snyk-url]

This contains samhammer specific and internally used helper functions for web projects.

Requirements for code to be added here:

- It's sag/project specific and not of general/public use, so that it does not make sense to create a individual lib
- It's nothing private either, that should not be publically on the internet
- It has no, or very little dependencies
  (because the deps are in all projects using the lib, even if the feaute isn't required)

Note: See this as last option and try to create individual libs as much as possible.

### Installation

pip install sag-py-web-common

## How to use

### Default routing

All requests to the main route / are redirected to /swagger if nothing specified.

```python
from sag_py_web_common.default_route import build_default_route

app: FastAPI = FastAPI(...)

app.include_router(build_default_route(ingress_base_path=config.ingress_base_path))
```

- ingress_base_path: Empty or a path starting with / if proxy hosting like kubernetes is used
- default_redirect_path: Per default /swagger but can be configured to an alternative route

### Filtered access logging

Extends the asgi-logger and adds a log entry for received requests.
Furthermore the requests can be filtered, so that health checks (or similar) don't spam the logs.

Requests can be filtered via one of two ways:

- via the optional parameter "excluded_paths": Simply append all paths that should be ignored, separated by comma.
- via the optional parameter "exclude_header": This one will require you to define a name for the header (f.ex. 'myHeaderExclude'), and then also send this defined header as an HTTP Header with your requests.

This filter will apply to substrings, as well since the filter is using a contains-search.

```python
from sag_py_web_common.filtered_access_logger import FilteredAccessLoggerMiddleware

app: FastAPI = FastAPI(...)

app.add_middleware(
    FilteredAccessLoggerMiddleware,
    format="Completed: %(R)s - %(st)s - %(L)s",
    logger=logging.getLogger("access"),
    excluded_paths=["pathPart/partOne", "pathPart/partTwo"], # optional
    exclude_header="myHeaderExclude" # optional
)
```

Also see this page for further configuration details: https://github.com/Kludex/asgi-logger

### Json exception handler

Per default fastapi falls back to text responses if there are unknown exceptions.
That's not the desired behaviour for json api's.

This handler ensures that a json is returned. It contains the field "detail" with the exception message.

```python
from sag_py_web_common.json_exception_handler import handle_unknown_exception

app.add_exception_handler(Exception, handle_unknown_exception)
```

For logging any HHTP-Exception use the **log_exception** function.

```python
from starlette.exceptions import HTTPException as StarletteHTTPException
from sag_py_web_common.json_exception_handler import log_exception

app.add_exception_handler(StarletteHTTPException, log_exception)
```

Json Exception handler uses logger "http_error_logger", which could be used for reporting concepts.

## How to start developing

### With vscode

Just install vscode with dev containers extension. All required extensions and configurations are prepared automatically.

### With pycharm

- Install latest pycharm
- Install pycharm plugin BlackConnect
- Install pycharm plugin Mypy
- Configure the python interpreter/venv
- pip install requirements-dev.txt
- pip install black[d]
- Ctl+Alt+S => Check Tools => BlackConnect => Trigger when saving changed files
- Ctl+Alt+S => Check Tools => BlackConnect => Trigger on code reformat
- Ctl+Alt+S => Click Tools => BlackConnect => "Load from pyproject.yaml" (ensure line length is 120)
- Ctl+Alt+S => Click Tools => BlackConnect => Configure path to the blackd.exe at the "local instance" config (e.g. C:\Python310\Scripts\blackd.exe)
- Ctl+Alt+S => Click Tools => Actions on save => Reformat code
- Restart pycharm

## How to publish

- Update the version in setup.py and commit your change
- Create a tag with the same version number
- Let github do the rest

## How to test

To avoid publishing to pypi unnecessarily you can do as follows

- Tag your branch however you like
- Use the chosen tag in the requirements.txt-file of the project you want to test this library in, eg. `sag_py_web_common==<your tag>`
- Rebuild/redeploy your project

[codeclimate-image]: https://api.codeclimate.com/v1/badges/533686a1f4d644151adb/maintainability
[codeclimate-url]: https://codeclimate.com/github/SamhammerAG/sag_py_web_common/maintainability
[coveralls-image]: https://coveralls.io/repos/github/SamhammerAG/sag_py_web_common/badge.svg?branch=master
[coveralls-url]: https://coveralls.io/github/SamhammerAG/sag_py_web_common?branch=master
[snyk-image]: https://snyk.io/test/github/SamhammerAG/sag_py_web_common/badge.svg
[snyk-url]: https://snyk.io/test/github/SamhammerAG/sag_py_web_common
