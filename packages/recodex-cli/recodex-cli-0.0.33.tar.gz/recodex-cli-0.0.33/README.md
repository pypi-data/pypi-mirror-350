# ReCodEx CLI

[![Build Status](https://github.com/ReCodEx/cli/workflows/CI/badge.svg)](https://github.com/ReCodEx/cli/actions)

Command line interface to the ReCodEx system.

## Requirements
- Python 3.9+
- See `requirements.txt`

## Installation
`pip install recodex-cli`

## Usage
See `recodex --help` after installation.

## Development
1. clone the repository
2. install dependencies using `pip install -r requirements.txt` in the root 
   directory of the repository

The package can be installed locally using `pip install -e` for the development.

### Writing plugins

The CLI is easy to extend with plugins. This way, you can add subcommands to the `recodex` command without touching the 
source of the core, while the CLI takes care of storing access tokens for you.

A minimal plugin must contain package with a [Click](http://click.pocoo.org/) command and a `setup.py` file that looks 
like this:

```python
from setuptools import setup

# ...

setup(# ...
      entry_points={
          'recodex': [
              'my_plugin_name = my_plugin_package.plugin:cli_function'
          ]
      }
      # ...
      )
```

When this is ready, you can install the plugin package (it is recommended to use `pip install -e .` for development). 
The entry point configuration allows the ReCodEx CLI to find your plugins whenever you run it.

Your entry point (the Click command) can use the `@pass_api_client`, `@pass_user_context` and other decorators from the 
`recodex.decorators` module.

For examples of plugins (including decorator usage), check out the `recodex.plugins` package in this repository.

## Testing
Unit tests are using py.test and are located in the `/tests` directory.

### Running tests
- unit tests: `pytest`


