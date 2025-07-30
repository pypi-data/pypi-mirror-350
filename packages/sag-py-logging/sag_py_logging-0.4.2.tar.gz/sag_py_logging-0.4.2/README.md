# sag_py_logging

[![Maintainability][codeclimate-image]][codeclimate-url]
[![Coverage Status][coveralls-image]][coveralls-url]
[![Known Vulnerabilities](https://snyk.io/test/github/SamhammerAG/sag_py_logging/badge.svg)](https://snyk.io/test/github/SamhammerAG/sag_py_logging)

[coveralls-image]:https://coveralls.io/repos/github/SamhammerAG/sag_py_logging/badge.svg?branch=master
[coveralls-url]:https://coveralls.io/github/SamhammerAG/sag_py_logging?branch=master
[codeclimate-image]:https://api.codeclimate.com/v1/badges/74139973d3df4567a67b/maintainability
[codeclimate-url]:https://codeclimate.com/github/SamhammerAG/sag_py_logging/maintainability

This library can be used to initialize the python logging by loading a config json.
Furthermore it provides a way to log extra fields.

## What it does
* Initialize logging from configuration json
* Placeholder support for the config json
* A log filter to log extra fields

## How to use

### Installation

pip install sag-py-logging

pip install sag-py-logging[jinia] (optional for templating)

pip install sag-py-logging[toml] (optional for toml file support)

### Initialize logging from json

Add the following as early as possible to your application code:

```python
from sag_py_logging.log_config_initializer import init_logging
from sag_py_logging.log_config_loader import JsonLoader, TomlLoader
from sag_py_logging.log_config_processors import FormatProcessor, JinjaProcessor

placeholder_container = { "host": "myhost.com", ...}

# For toml config with jinja templating
init_logging(
    "./log_config.toml",
    loader=TomlLoader(),
    processors=[JinjaProcessor(placeholder_container)]
)

# For json config with format templating
init_logging(
    "./log_config.json",
    loader=JsonLoader(),
    processors=[FormatProcessor(placeholder_container)]
)

```

Init logging returns the log configuration as dictionary if needed for further processing.

### The configuration

Json config:
```json
{
    "version": 1,
    "disable_existing_loggers": false,
    "root": {
        "handlers": ["myhandler"],
        "level": "INFO"
    },
    "handlers": {
        "myhandler": {
            "host": "${host}",
            "formatter": "handler_formatter"
        }
    }
}
```

Toml config:
```toml
version = 1
disable_existing_loggers = false

[root]
handlers = ["myhandler"]
level = "INFO"

[handlers.myhandler]
host = "${host}"
formatter = "handler_formatter"

```
This is a very basic sample on the format of the file including placeholders.

Read the following for a full schema reference: https://docs.python.org/3/library/logging.config.html#configuration-dictionary-schema

Read more on string templating here: https://docs.python.org/3/library/string.html#template-strings

Or if you use jinja templating there: https://jinja.palletsprojects.com/en/3.1.x/templates/#template-designer-documentation


### Configure extra field logging

It is possible to add a filter that extends log entries by a field for extra fields.

The filter is added like that if you initialize logging by code:
```python
from sag_py_logging.console_extra_field_filter import ConsoleExtraFieldFilter

console_handler = logging.StreamHandler(sys.stdout)
console_handler.addFilter(ConsoleExtraFieldFilter())
```

If you init logging by config file the filter is added like that:
```json
{
    "formatters": {
        "myformatter": {
            "format": "s%(asctime)s - %(name)s - %(message)s - %(stringified_extra)s",
        },
    },
    "filters": {
        "console_extra_field_filter": {"()": "sag_py_logging.console_extra_field_filter.ConsoleExtraFieldFilter"}
    },
    "handlers": {
        "myhandler": {
            "formatter": "myformatter",
            "filters": ["console_extra_field_filter"]
        }
    }
}
```

Afterwards you can use the field "stringified_extra" in your format string.

If you for example log the following:
```python
logging.warning('Watch out!', extra={"keyOne": "valueOne", "keyTwo": 2})
```

The resulting log entry would look like that if stringified_extra is added to the end of the format string:

```
Watch out! {"keyOne": "valueOne", "keyTwo": 2}
```

Note: Internally json.dumps is used to convert the object/data to a string


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
* Use the chosen tag in the requirements.txt-file of the project you want to test this library in, eg. `sag_py_logging==<your tag>`
* Rebuild/redeploy your project