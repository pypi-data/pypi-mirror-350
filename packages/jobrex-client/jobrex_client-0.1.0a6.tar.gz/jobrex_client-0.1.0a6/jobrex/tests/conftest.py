"""
Pytest configuration file with fixtures.
"""
import pytest
from unittest.mock import Mock, patch
from jobrex.client import BaseClient, ResumesClient, JobsClient
from jobrex.models import (
    Url, ResumeBasics, Summary, Certifications, Education, Experience,
    Profiles, Skills, Sections, Resume
)


@pytest.fixture
def mock_session():
    """Mock requests.Session for testing."""
    with patch("requests.Session") as mock:
        session_instance = Mock()
        session_instance.headers = {}
        mock.return_value = session_instance
        yield mock


@pytest.fixture
def base_client():
    """Create a BaseClient instance for testing."""
    return BaseClient(api_key="test_api_key")


@pytest.fixture
def resumes_client():
    """Create a ResumesClient instance for testing."""
    return ResumesClient(api_key="test_api_key")


@pytest.fixture
def jobs_client():
    """Create a JobsClient instance for testing."""
    return JobsClient(api_key="test_api_key")


@pytest.fixture
def sample_resume():
    """Create a sample Resume instance for testing."""
    basics = ResumeBasics(
        name="John Doe",
        headline="Software Engineer",
        email="john@example.com",
        phone="123-456-7890",
        location="New York, NY",
        url=Url(label="Portfolio", href="https://johndoe.com")
    )
    
    summary = Summary(content="Experienced software engineer with 5+ years of experience")
    certifications = Certifications(items=[])
    education = Education(items=[])
    experience = Experience(items=[])
    profiles = Profiles(items=[])
    skills = Skills(items=[])
    
    sections = Sections(
        summary=summary,
        certifications=certifications,
        education=education,
        experience=experience,
        profiles=profiles,
        skills=skills
    )
    
    return Resume(basics=basics, sections=sections)


@pytest.fixture
def sample_job_details():
    """Create a sample job details dictionary for testing."""
    return {
        "title": "Senior Software Engineer",
        "company": "Tech Company",
        "location": "Remote",
        "description": "We are looking for a skilled software engineer...",
        "requirements": ["Python", "JavaScript", "AWS"],
        "responsibilities": ["Develop web applications", "Mentor junior developers"]
    }


@pytest.fixture
def mock_response():
    """Create a mock response for testing API calls."""
    mock = Mock()
    mock.json.return_value = {"status": "success"}
    mock.text = '{"status": "success"}'
    return mock 