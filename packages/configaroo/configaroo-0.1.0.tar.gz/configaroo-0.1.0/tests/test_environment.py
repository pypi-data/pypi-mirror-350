"""Test handling of environment variables"""

import pytest

from configaroo import MissingEnvironmentVariableError


def test_add_one_env(config, monkeypatch):
    """Test that we can add one environment variable in a new field"""
    monkeypatch.setenv("WORD", "platypus")
    config_w_env = config.add_envs({"WORD": "nested.word"})
    assert config_w_env.nested.word == "platypus"


def test_overwrite_one_env(config, monkeypatch):
    """Test that we can overwrite a value with an environment value"""
    monkeypatch.setenv("NEW_PATH", "files/config.json")
    config_w_env = config.add_envs({"NEW_PATH": "path"})
    assert config_w_env.path == "files/config.json"


def test_several_envs(config, monkeypatch):
    """Test that we can read several environment variables"""
    monkeypatch.setenv("WORD", "platypus")
    monkeypatch.setenv("NEW_PATH", "files/config.json")
    config_w_env = config.add_envs({"WORD": "nested.word", "NEW_PATH": "path"})
    assert config_w_env.nested.word == "platypus"
    assert config_w_env.path == "files/config.json"


def test_error_on_missing_env(config):
    """Test that a missing environment variable raises an error if the value is not set already"""
    with pytest.raises(KeyError):
        config.add_envs({"NON_EXISTENT": "non_existent"})
    with pytest.raises(MissingEnvironmentVariableError):
        config.add_envs({"NON_EXISTENT": "non_existent"})


def test_missing_env_ok_if_optional(config):
    """Test that a missing environment variable is ok if the value is already set"""
    config_w_env = config.add_envs({"NON_EXISTENT": "number"})
    assert config_w_env.number == 42


def test_env_prefix(config, monkeypatch):
    """Test that a common prefix can be used for environment_variables"""
    monkeypatch.setenv("EXAMPLE_NUMBER", "14")
    monkeypatch.setenv("EXAMPLE_WORD", "platypus")
    config_w_env = config.add_envs(
        {"NUMBER": "number", "WORD": "nested.word"}, prefix="EXAMPLE_"
    )
    assert config_w_env.number == "14"
    assert config_w_env.nested.word == "platypus"
