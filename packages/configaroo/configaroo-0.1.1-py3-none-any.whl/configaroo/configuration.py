"""A dict-like configuration with support for envvars, validation and type conversion"""

import inspect
import os
import re
from collections import UserDict
from pathlib import Path
from typing import Any, Self, Type

import dotenv
from pydantic import BaseModel

from configaroo import loaders
from configaroo.exceptions import MissingEnvironmentVariableError


class Configuration(UserDict):
    """A Configuration is a dict-like structure with some conveniences"""

    @classmethod
    def from_file(
        cls,
        file_path: str | Path,
        loader: str | None = None,
        envs: dict[str, str] | None = None,
        env_prefix: str = "",
        extra_dynamic: dict[str, Any] | None = None,
        model: Type[BaseModel] | None = None,
    ) -> Self:
        """Read a Configuration from a file"""
        config_dict = loaders.from_file(file_path, loader=loader)
        return cls(config_dict).initialize(
            envs=envs, env_prefix=env_prefix, extra_dynamic=extra_dynamic, model=model
        )

    def initialize(
        self,
        envs: dict[str, str] | None = None,
        env_prefix: str = "",
        extra_dynamic: dict[str, Any] | None = None,
        model: Type[BaseModel] | None = None,
    ) -> Self:
        """Initialize a configuration.

        The initialization adds environment variables, parses dynamic values,
        validates against a Pydantic model, and converts value types using the
        same model.
        """
        self = self if envs is None else self.add_envs(envs, prefix=env_prefix)
        self = self.parse_dynamic(extra_dynamic)
        self = self if model is None else self.validate(model).convert(model)
        return self

    def __getitem__(self, key: str) -> Any:
        """Make sure nested sections have type Configuration"""
        value = self.data[key]
        if isinstance(value, dict | UserDict | Configuration):
            return Configuration(value)
        else:
            return value

    def __getattr__(self, key: str) -> Any:
        """Create attribute access for config keys for convenience"""
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                f"'{type(self).__name__}' has no attribute or key '{key}'"
            )

    def __contains__(self, key: str) -> bool:
        """Add support for dotted keys"""
        if key in self.data:
            return True
        prefix, _, rest = key.partition(".")
        try:
            return rest in self[prefix]
        except KeyError:
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Allow dotted keys when using .get()"""
        if key in self.data:
            return self[key]

        prefix, _, rest = key.partition(".")
        try:
            return self[prefix].get(rest, default=default)
        except KeyError:
            return default

    def add(self, key: str, value: Any) -> Self:
        """Add a value, allow dotted keys"""
        prefix, _, rest = key.partition(".")
        if rest:
            cls = type(self)
            return self | {prefix: cls(self.setdefault(prefix, {})).add(rest, value)}
        else:
            return self | {key: value}

    def add_envs(self, envs: dict[str, str], prefix: str = "", use_dotenv=True) -> Self:
        """Add environment variables to configuration"""
        if use_dotenv:
            dotenv.load_dotenv()

        for env, key in envs.items():
            env_key = f"{prefix}{env}"
            env_value = os.getenv(env_key)
            if env_value:
                self = self.add(key, env_value)
            else:
                if key not in self:
                    raise MissingEnvironmentVariableError(
                        f"required environment variable '{env_key}' not found"
                    )
        return self

    def parse_dynamic(self, extra: dict[str, Any] | None = None) -> Self:
        """Parse dynamic values of the form {section.key}"""
        cls = type(self)
        variables = (
            self.to_flat_dict()
            | {"project_path": _find_pyproject_toml()}
            | ({} if extra is None else extra)
        )
        return cls(
            {
                key: (
                    value.parse_dynamic(extra=variables)
                    if isinstance(value, Configuration)
                    else _incomplete_format(value, variables)
                    if isinstance(value, str)
                    else value
                )
                for key, value in self.items()
            }
        )

    def validate(self, model: Type[BaseModel]) -> Self:
        """Validate the configuration against the given model."""
        model.model_validate(self.data)
        return self

    def convert(self, model: Type[BaseModel]) -> Self:
        """Convert data types to match the given model"""
        cls = type(self)
        return cls(model(**self.data).model_dump())

    def to_dict(self) -> dict[str, Any]:
        """Dump the configuration into a Python dictionary"""
        return {
            key: value.to_dict() if isinstance(value, Configuration) else value
            for key, value in self.items()
        }

    def to_flat_dict(self, _prefix: str = "") -> dict[str, Any]:
        """Dump the configuration into a flat dictionary.

        Nested configurations are converted into dotted keys.
        """
        return {
            f"{_prefix}{key}": value
            for key, value in self.items()
            if not isinstance(value, Configuration)
        } | {
            key: value
            for nested_key, nested_value in self.items()
            if isinstance(nested_value, Configuration)
            for key, value in (
                self[nested_key].to_flat_dict(_prefix=f"{_prefix}{nested_key}.").items()
            )
        }


def _find_pyproject_toml(
    path: Path | None = None, _file_name: str = "pyproject.toml"
) -> Path:
    """Find a directory that contains a pyproject.toml file.

    This searches the given directory and all direct parents. If a
    pyproject.toml file isn't found, then the root of the file system is
    returned.
    """
    path = _get_foreign_path() if path is None else path
    if (path / _file_name).exists() or path == path.parent:
        return path.resolve()
    else:
        return _find_pyproject_toml(path.parent, _file_name=_file_name)


def _get_foreign_path() -> Path:
    """Find the path to the library that called this package.

    Search the call stack for the first source code file outside of configaroo.
    """
    self_prefix = Path(__file__).parent.parent
    return next(
        path
        for frame in inspect.stack()
        if not (path := Path(frame.filename)).is_relative_to(self_prefix)
    )


def _incomplete_format(text: str, replacers: dict[str, Any]) -> str:
    """Replace some, but not necessarily all format specifiers in a text string.

    Regular .format() raises an error if not all {replace} parameters are
    supplied. Here, we only replace the given replace arguments and leave the
    rest untouched.
    """
    dot = "__DOT__"  # Escape . in fields as they have special meaning in .format()
    pattern = r"({{{word}(?:![ars])?(?:|:[^}}]*)}})"  # Match {word} or {word:...}

    for word, replacement in replacers.items():
        for match in re.findall(pattern.format(word=word), text):
            # Split expression to only replace . in the field name
            field, colon, fmt = match.partition(":")
            replacer = f"{field.replace('.', dot)}{colon}{fmt}".format(
                **{word.replace(".", dot): replacement}
            )
            text = text.replace(match, replacer)
    return text
