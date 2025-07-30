"""Test validation and type conversion with Pydantic"""

from pathlib import Path

import pydantic
import pytest

from configaroo import Configuration


def test_can_validate(config, model):
    """Test that a configuration can be validated"""
    assert config.validate_model(model)


def test_wrong_key_raises(model):
    """Test that a wrong key raises an error"""
    config = Configuration(
        digit=4, nested={"pie": 3.14, "seven": 7}, path="files/config.toml"
    )
    with pytest.raises(pydantic.ValidationError):
        config.validate_model(model)


def test_missing_key_raises(model):
    """Test that a missing key raises an error"""
    config = Configuration(nested={"pie": 3.14, "seven": 7}, path="files/config.toml")
    with pytest.raises(pydantic.ValidationError):
        config.validate_model(model)


def test_extra_key_ok(config, model):
    """Test that an extra key raises when the model is strict"""
    updated_config = config | {"new_word": "cuckoo-bird"}
    with pytest.raises(pydantic.ValidationError):
        updated_config.validate_model(model)


def test_type_conversion(config, model):
    """Test that types can be converted based on the model"""
    config_w_types = config.convert_model(model)
    assert isinstance(config.paths.relative, str)
    assert isinstance(config_w_types.paths.relative, Path)


def test_converted_model_is_pydantic(config, model):
    """Test that the converted model is a BaseModel which helps with auto-complete"""
    config_w_types = config.convert_model(model=model)
    assert isinstance(config_w_types, pydantic.BaseModel)


def test_validate_and_convert(config, model):
    config_w_model = config.with_model(model)
    assert isinstance(config_w_model, pydantic.BaseModel)
    assert isinstance(config_w_model.paths.relative, Path)
