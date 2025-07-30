"""Configaroo specific exceptions"""


class ConfigarooException(Exception):
    """Base exception for more specific Configaroo exceptions"""


class MissingEnvironmentVariableError(ConfigarooException, KeyError):
    """A required environment variable is missing"""


class UnsupportedLoaderError(ConfigarooException, ValueError):
    """An unsupported loader is called"""
