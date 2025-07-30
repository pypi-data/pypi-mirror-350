# EasyWorkEnv

This is a Python package that simplifies the management of environment variables.

## Compatibility
### Supported environment file formats
- `json`
- `.env`
- `.yaml`

## Example usage

```python
from EasyWorkEnv import Config

# Creation of the object containing all your environment variables

config = Config(".env")

# Variables retrieved from the environment

myEnv = config.ENV
myAPiKey = config.APIKEY

# Nested information

myBddHost = config.BDD.Host
myBddDatabaseName = config.BDD.DATABASENAME
```
