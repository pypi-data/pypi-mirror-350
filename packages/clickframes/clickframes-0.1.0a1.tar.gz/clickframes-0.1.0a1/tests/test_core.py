"""Tests for ClickFrame core functionality."""

# import pytest
from clickframes.core import ClickFrame


class TestClickFrame:
    """Test suite for ClickFrame class."""

    def test_initialization(self):
        """Test ClickFrame can be initialized."""
        frame = ClickFrame()
        assert isinstance(frame, ClickFrame)

    def test_process_basic(self):
        """Test basic data processing."""
        frame = ClickFrame()
        test_data = "test"
        result = frame.process(test_data)
        assert result == test_data

    def test_process_with_dict(self):
        """Test processing with dictionary data."""
        frame = ClickFrame()
        test_data = {"key": "value"}
        result = frame.process(test_data)
        assert result == test_data

    def test_process_with_list(self):
        """Test processing with list data."""
        frame = ClickFrame()
        test_data = [1, 2, 3]
        result = frame.process(test_data)
        assert result == test_data


def test_package_version():
    """Test that package version is accessible."""
    import clickframes

    assert hasattr(clickframes, "__version__")
    assert isinstance(clickframes.__version__, str)
