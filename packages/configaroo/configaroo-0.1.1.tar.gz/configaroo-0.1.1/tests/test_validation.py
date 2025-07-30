"""Test validation and type conversion with Pydantic"""

from pathlib import Path

import pydantic
import pytest

from configaroo import Configuration


def test_can_validate(config, model):
    """Test that a configuration can be validated"""
    assert config.validate(model)


def test_wrong_key_raises(model):
    """Test that a wrong key raises an error"""
    config = Configuration(
        digit=4, nested={"pie": 3.14, "seven": 7}, path="files/config.toml"
    )
    with pytest.raises(pydantic.ValidationError):
        config.validate(model)


def test_missing_key_raises(model):
    """Test that a missing key raises an error"""
    config = Configuration(nested={"pie": 3.14, "seven": 7}, path="files/config.toml")
    with pytest.raises(pydantic.ValidationError):
        config.validate(model)


def test_extra_key_ok(config, model):
    """Test that an extra key raises when the model is strict"""
    updated_config = config | {"new_word": "cuckoo-bird"}
    with pytest.raises(pydantic.ValidationError):
        updated_config.validate(model)


def test_type_conversion(config, model):
    config_w_types = config.convert(model)
    assert isinstance(config.paths.relative, str)
    assert isinstance(config_w_types.paths.relative, Path)
