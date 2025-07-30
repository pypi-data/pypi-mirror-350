"""Test base Configuration functionality"""

from pathlib import Path

import pytest

from configaroo import Configuration, configuration


@pytest.fixture
def file_path():
    """The path to the current file"""
    return Path(__file__).resolve()


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


def test_parse_dynamic_default(config, file_path):
    """Test parsing of default dynamic variables"""
    parsed_config = (config | {"diameter": "2 x {nested.pie}"}).parse_dynamic()
    print("pyproject.toml dir: ", configuration._find_pyproject_toml(file_path))
    print(f"{parsed_config.paths.dynamic = }")
    assert parsed_config.paths.dynamic == str(file_path)
    assert parsed_config.phrase == "The meaning of life is 42"
    assert parsed_config.diameter == "2 x 3.14"


def test_parse_dynamic_extra(config, file_path):
    """Test parsing of extra dynamic variables"""
    parsed_config = (config | {"animal": "{adjective} kangaroo"}).parse_dynamic(
        extra={"number": 14, "adjective": "bouncy"}
    )
    assert parsed_config.paths.dynamic == str(file_path)
    assert parsed_config.phrase == "The meaning of life is 14"
    assert parsed_config.animal == "bouncy kangaroo"


def test_parse_dynamic_formatted(config):
    """Test that formatting works for dynamic variables"""
    parsed_config = (
        config
        | {
            "string": "Hey {word!r}",
            "three": "->{nested.pie:6.0f}<-",
            "centered": "|{word:^12}|",
        }
    ).parse_dynamic()
    assert parsed_config.centered == "|  platypus  |"
    assert parsed_config.three == "->     3<-"
    assert parsed_config.string == "Hey 'platypus'"


def test_parse_dynamic_ignore(config):
    """Test that parsing of dynamic variables ignores unknown replacements"""
    parsed_config = (
        config
        | {
            "animal": "{adjective} kangaroo",
            "phrase": "one {nested.non_existent} dollar",
        }
    ).parse_dynamic()
    assert parsed_config.animal == "{adjective} kangaroo"
    assert parsed_config.phrase == "one {nested.non_existent} dollar"


def test_find_pyproject_toml():
    """Test that the pyproject.toml file can be located"""
    assert configuration._find_pyproject_toml() == Path(__file__).parent.parent


def test_find_foreign_caller():
    """Test that a foreign caller (outside of configaroo) can be identified"""
    assert configuration._get_foreign_path() == Path(__file__)


def test_incomplete_formatter():
    """Test that the incomplete formatter can handle fields that aren't replaced"""
    formatted = configuration._incomplete_format(
        "{number:5.1f} {non_existent} {string!r} {name}",
        {"number": 3.14, "string": "platypus", "name": "Geir Arne"},
    )
    assert formatted == "  3.1 {non_existent} 'platypus' Geir Arne"
