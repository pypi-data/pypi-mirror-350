"""Test base Configuration functionality"""

import pytest

from configaroo import Configuration


def test_read_simple_values_as_attributes(config):
    """Test attribute access for simple values."""
    assert config.number == 42
    assert config.word == "platypus"
    assert config.things == ["house", "car", "kayak"]


def test_read_simple_values_as_items(config):
    """Test dictionary access for simple values."""
    assert config["number"] == 42
    assert config["word"] == "platypus"
    assert config["things"] == ["house", "car", "kayak"]


def test_missing_attributes_raise_attribute_error(config):
    """Test that accessing missing attributes raise the appropriate error"""
    with pytest.raises(AttributeError):
        config.non_existent


def test_nested_values_are_configurations(config):
    """Test that a nested configuration has type Configuration"""
    assert isinstance(config["nested"], Configuration)


def test_read_nested_values_as_attributes(config):
    """Test attribute access for nested values."""
    assert config.nested.pie == 3.14
    assert config.nested.seven == 7


def test_read_nested_values_as_items(config):
    """Test dictionary access for nested values."""
    assert config["nested"]["pie"] == 3.14
    assert config["nested"]["seven"] == 7
    assert config["with_dot"]["org.num"] == 1234


def test_read_nested_values_as_attributes_and_items(config):
    """Test mixed access for nested values."""
    assert config["nested"].pie == 3.14
    assert config.nested["seven"] == 7


def test_get_nested_values(config):
    """Test that .get() can use dotted keys"""
    assert config.get("nested.seven") == 7
    assert config.get("with_dot.org.num") == 1234


def test_update_preserves_type(config):
    """Test that an update operation gives a Configuration"""
    assert isinstance(config | {"new": 1}, Configuration)

    config.update(new=1)
    assert isinstance(config, Configuration)


def test_dump_to_dict(config):
    """Test that dumping to a dictionary unwraps nested sections"""
    config_dict = config.to_dict()
    assert isinstance(config_dict, dict)
    assert isinstance(config_dict["paths"], dict)


def test_dump_to_flat_dict(config):
    """Test that a configuration can be converted to a flat dictionary"""
    flat_config_dict = config.to_flat_dict()
    assert isinstance(flat_config_dict, dict)
    assert flat_config_dict["number"] == 42
    assert flat_config_dict["nested.seven"] == 7
    assert flat_config_dict["nested.deep.sea"] == "Marianer"
    assert flat_config_dict["with_dot.org.num"] == 1234


def test_contains_with_simple_key(config):
    """Test that "key" in config works for simple keys"""
    assert "number" in config
    assert "not_there" not in config


def test_contains_with_dotted_key(config):
    """Test that "key" in config works for dotted keys"""
    assert "nested.seven" in config
    assert "with_dot.org.num" in config
    assert "nested.number" not in config


def test_parse_dynamic_default(config):
    """Test parsing of default dynamic variables"""
    parsed_config = config.parse_dynamic()
    assert parsed_config.paths.dynamic == __file__
    assert parsed_config.phrase == "The meaning of life is 42"


def test_parse_dynamic_extra(config):
    """Test parsing of extra dynamic variables"""
    parsed_config = (config | {"animal": "{adjective} platypus"}).parse_dynamic(
        extra={"number": 14, "adjective": "tall"}
    )
    assert parsed_config.paths.dynamic == __file__
    assert parsed_config.phrase == "The meaning of life is 14"
    assert parsed_config.animal == "tall platypus"
