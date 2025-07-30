"""Test file loader framework"""

import pytest

from configaroo import UnsupportedLoaderError, loaders


def test_unsupported_loader(toml_path):
    """Test that calling an unsupported loader fails"""
    with pytest.raises(UnsupportedLoaderError):
        loaders.from_file(toml_path, loader="non_existent")


def test_unsupported_suffix(toml_path):
    """Test that loading a file with an unsupported suffix fails"""
    with pytest.raises(UnsupportedLoaderError):
        loaders.from_file(toml_path.with_suffix(".non_existent"))


def test_error_lists_supported_loaders(toml_path):
    """Test that the names of supported loaders are listed when failing"""
    try:
        loaders.from_file(toml_path.with_suffix(".non_existent"))
    except UnsupportedLoaderError as err:
        for loader in ["json", "toml"]:
            assert loader in str(err)


def test_toml_returns_dict(toml_path):
    """Test that the TOML loader returns a nonempty dictionary"""
    config_dict = loaders.from_file(toml_path, loader="toml")
    assert config_dict and isinstance(config_dict, dict)


def test_json_returns_dict(json_path):
    """Test that the JSON loader returns a nonempty dictionary"""
    config_dict = loaders.from_file(json_path, loader="json")
    assert config_dict and isinstance(config_dict, dict)
