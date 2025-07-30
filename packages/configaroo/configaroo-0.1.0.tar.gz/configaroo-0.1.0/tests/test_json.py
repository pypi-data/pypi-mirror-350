"""Test handling of JSON files"""

import json

import pytest

from configaroo import Configuration


def test_can_load_config_from_toml(json_path):
    """Test that the TOML file can be loaded"""
    config = Configuration.from_file(json_path)
    assert config


def test_can_load_config_with_path_as_str(json_path):
    """Test that the path can be specified in a string"""
    config = Configuration.from_file(str(json_path))
    assert config


def test_can_specify_loader(other_json_path):
    """Test that we can specify the "json" loader"""
    config = Configuration.from_file(other_json_path, loader="json")
    assert config


def test_error_on_nonexisting_file():
    """Test that a FileNotFoundError is raised if the file doesn't exist"""
    with pytest.raises(FileNotFoundError):
        Configuration.from_file("non-existent.json")


def test_error_on_wrong_format(toml_path):
    """Test that a JSONDecodeError is raised if the file is not a valid JSON-file"""
    with pytest.raises(json.JSONDecodeError):
        Configuration.from_file(toml_path, loader="json")


def test_can_read_json_values(json_path):
    """Test that values can be accessed"""
    config = Configuration.from_file(json_path)
    assert config.word == "platypus"
    assert config.nested.seven == 7
