"""Test handling of TOML files"""

import tomllib

import pytest

from configaroo import Configuration


def test_can_load_config_from_toml(toml_path):
    """Test that the TOML file can be loaded"""
    config = Configuration.from_file(toml_path)
    assert config


def test_can_load_config_with_path_as_str(toml_path):
    """Test that the path can be specified in a string"""
    config = Configuration.from_file(str(toml_path))
    assert config


def test_can_specify_loader(other_toml_path):
    """Test that we can specify the "toml" loader"""
    config = Configuration.from_file(other_toml_path, loader="toml")
    assert config


def test_error_on_nonexisting_file():
    """Test that a FileNotFoundError is raised if the file doesn't exist"""
    with pytest.raises(FileNotFoundError):
        Configuration.from_file("non-existent.toml")


def test_error_on_wrong_format(json_path):
    """Test that a TOMLDecodeError is raised if the file is not a valid TOML-file"""
    with pytest.raises(tomllib.TOMLDecodeError):
        Configuration.from_file(json_path, loader="toml")


def test_can_read_toml_values(toml_path):
    """Test that values can be accessed"""
    config = Configuration.from_file(toml_path)
    assert config.word == "platypus"
    assert config.nested.seven == 7
