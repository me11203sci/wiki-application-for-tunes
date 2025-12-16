"""Test waft package functionality."""

from waft.__about__ import __version__  # type: ignore
from waft.application import Application  # type: ignore


def test_application_exists():
    """Test that Application class can be imported."""
    assert Application is not None


def test_version_defined():
    """Test that version is defined."""
    assert __version__ is not None
    assert isinstance(__version__, str)


def test_application_instantiation():
    """Test that Application can be instantiated."""
    app = Application()
    assert app is not None
