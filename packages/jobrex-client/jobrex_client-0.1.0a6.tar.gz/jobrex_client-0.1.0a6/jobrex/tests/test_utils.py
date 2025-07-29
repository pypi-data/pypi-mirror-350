"""
Tests for the utils module.
"""
import pytest
from jobrex.utils import clean_text, format_experiences, format_skills


def test_clean_text():
    """Test the clean_text function."""
    # Test with special characters
    text = "Hello, World! This is a test."
    result = clean_text(text)
    assert result == ["hello", "world", "this", "is", "a", "test"]
    
    # Test with empty string
    assert clean_text("") == []
    
    # Test with only special characters
    assert clean_text("!@#$%^&*()") == []


def test_format_experiences():
    """Test the format_experiences function."""
    experiences = [
        {
            "position": "Software Engineer",
            "company": "Tech Corp",
            "date": "2020-2022",
            "summary": "Developed web applications"
        },
        {
            "position": "Data Scientist",
            "company": "Data Inc",
            "date": "2018-2020",
            "summary": "Analyzed customer data"
        }
    ]
    
    result = format_experiences(experiences)
    expected = (
        "Software Engineer at Tech Corp (2020-2022): Developed web applications\n"
        "Data Scientist at Data Inc (2018-2020): Analyzed customer data"
    )
    assert result == expected
    
    # Test with empty list
    assert format_experiences([]) == ""


def test_format_skills():
    """Test the format_skills function."""
    skills = [
        {"name": "Python"},
        {"name": "JavaScript"},
        {"name": "Machine Learning"}
    ]
    
    result = format_skills(skills)
    assert result == "Python, JavaScript, Machine Learning"
    
    # Test with empty list
    assert format_skills([]) == ""
    
    # Test with missing name key
    skills_with_missing = [
        {"name": "Python"},
        {},
        {"name": "JavaScript"}
    ]
    assert format_skills(skills_with_missing) == "Python, , JavaScript" 