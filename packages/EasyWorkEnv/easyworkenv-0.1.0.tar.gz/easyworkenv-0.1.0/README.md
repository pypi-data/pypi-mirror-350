# EasyWorkEnv

This is a Python package that simplifies the management of environment variables.

## Compatibility
### Supported environment file formats
- `json`
- `.env`

## Example usage

```python
from EasyWorkEnv import Config

config = Config(".env")

# Variables retrieved from the environment

myEnv = config.ENV
myAPiKey = config.APIKEY

# Nested information

myBddHost = config.BDD.Host
myBddDatabaseName = config.BDD.DATABASENAME
```
