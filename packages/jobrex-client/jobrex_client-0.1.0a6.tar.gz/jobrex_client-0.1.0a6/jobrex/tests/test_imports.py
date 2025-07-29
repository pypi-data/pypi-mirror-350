"""
Tests for package imports.
"""
import pytest


def test_package_imports():
    """Test that the package can be imported."""
    import jobrex
    assert hasattr(jobrex, "ResumesClient")
    assert hasattr(jobrex, "JobsClient")
    
    # Test importing specific classes
    from jobrex import ResumesClient, JobsClient
    assert ResumesClient is not None
    assert JobsClient is not None


def test_module_imports():
    """Test that modules can be imported."""
    import jobrex.client
    import jobrex.models
    import jobrex.utils
    
    # Test client module
    assert hasattr(jobrex.client, "BaseClient")
    assert hasattr(jobrex.client, "ResumesClient")
    assert hasattr(jobrex.client, "JobsClient")
    
    # Test models module
    assert hasattr(jobrex.models, "Resume")
    assert hasattr(jobrex.models, "JobDetails")
    
    # Test utils module
    assert hasattr(jobrex.utils, "clean_text")
    assert hasattr(jobrex.utils, "format_experiences")
    assert hasattr(jobrex.utils, "format_skills") 