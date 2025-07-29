"""
Tests for the models module.
"""
import pytest
from jobrex.models import (
    Url, ResumeBasics, CertificationItem, EducationItem, ExperienceItem,
    ProfileItem, SkillItem, Summary, Certifications, Education, Experience,
    Profiles, Skills, Sections, Resume, ResumeResponse, JobDetails,
    JobMatchResult, ResumeScoringResult, ZoomMeetingResponse
)


def test_url_model():
    """Test the Url model."""
    url = Url(label="GitHub", href="https://github.com/username")
    assert url.label == "GitHub"
    assert url.href == "https://github.com/username"


def test_resume_basics_model():
    """Test the ResumeBasics model."""
    # Test without optional url
    basics = ResumeBasics(
        name="John Doe",
        headline="Software Engineer",
        email="john@example.com",
        phone="123-456-7890",
        location="New York, NY"
    )
    assert basics.name == "John Doe"
    assert basics.headline == "Software Engineer"
    assert basics.email == "john@example.com"
    assert basics.phone == "123-456-7890"
    assert basics.location == "New York, NY"
    assert basics.url is None
    
    # Test with url
    url = Url(label="Portfolio", href="https://johndoe.com")
    basics_with_url = ResumeBasics(
        name="John Doe",
        headline="Software Engineer",
        email="john@example.com",
        phone="123-456-7890",
        location="New York, NY",
        url=url
    )
    assert basics_with_url.url == url


def test_certification_item_model():
    """Test the CertificationItem model."""
    cert = CertificationItem(
        name="AWS Certified Developer",
        issuer="Amazon Web Services",
        date="2022",
        summary="Cloud development certification"
    )
    assert cert.name == "AWS Certified Developer"
    assert cert.issuer == "Amazon Web Services"
    assert cert.date == "2022"
    assert cert.summary == "Cloud development certification"
    assert cert.url is None
    
    # Test with url
    url = Url(label="Certificate", href="https://aws.amazon.com/certification")
    cert_with_url = CertificationItem(
        name="AWS Certified Developer",
        issuer="Amazon Web Services",
        date="2022",
        summary="Cloud development certification",
        url=url
    )
    assert cert_with_url.url == url


def test_education_item_model():
    """Test the EducationItem model."""
    edu = EducationItem(
        institution="University of Example",
        studyType="Bachelor's",
        area="Computer Science",
        score="3.8 GPA",
        date="2015-2019",
        summary="Focused on software engineering and AI"
    )
    assert edu.institution == "University of Example"
    assert edu.studyType == "Bachelor's"
    assert edu.area == "Computer Science"
    assert edu.score == "3.8 GPA"
    assert edu.date == "2015-2019"
    assert edu.summary == "Focused on software engineering and AI"
    assert edu.url is None


def test_experience_item_model():
    """Test the ExperienceItem model."""
    exp = ExperienceItem(
        company="Tech Company",
        position="Senior Developer",
        location="Remote",
        date="2020-Present",
        summary="Leading development of web applications"
    )
    assert exp.company == "Tech Company"
    assert exp.position == "Senior Developer"
    assert exp.location == "Remote"
    assert exp.date == "2020-Present"
    assert exp.summary == "Leading development of web applications"
    assert exp.url is None


def test_resume_model():
    """Test the Resume model with minimal data."""
    # Create basic components
    basics = ResumeBasics(
        name="Jane Smith",
        headline="Data Scientist",
        email="jane@example.com",
        phone="987-654-3210",
        location="San Francisco, CA"
    )
    
    summary = Summary(content="Experienced data scientist with ML expertise")
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
    
    resume = Resume(basics=basics, sections=sections)
    
    assert resume.basics == basics
    assert resume.sections == sections
    assert resume.sections.summary.content == "Experienced data scientist with ML expertise"
    assert len(resume.sections.skills.items) == 0 