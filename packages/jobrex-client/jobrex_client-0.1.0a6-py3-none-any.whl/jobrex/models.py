from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union


@dataclass
class Url:
    """URL with label and href."""
    label: str
    href: str


@dataclass
class ResumeBasics:
    """Basic personal and contact information."""
    name: str
    headline: str
    email: str
    phone: str
    location: str
    url: Optional[Url] = None


@dataclass
class CertificationItem:
    """Certification item from a resume."""
    name: str
    issuer: str
    date: str
    summary: str
    url: Optional[Url] = None


@dataclass
class EducationItem:
    """Education item from a resume."""
    institution: str
    studyType: str
    area: str
    score: str
    date: str
    summary: str
    url: Optional[Url] = None


@dataclass
class ExperienceItem:
    """Work experience item from a resume."""
    company: str
    position: str
    location: str
    date: str
    summary: str
    url: Optional[Url] = None


@dataclass
class ProfileItem:
    """Profile item from a resume."""
    id: str
    network: str
    icon: str
    url: Url


@dataclass
class SkillItem:
    """Skill item from a resume."""
    name: str
    description: str
    keywords: List[str]


@dataclass
class Summary:
    """Professional summary section."""
    content: str


@dataclass
class Certifications:
    """Certifications section."""
    items: List[CertificationItem]


@dataclass
class Education:
    """Education section."""
    items: List[EducationItem]


@dataclass
class Experience:
    """Experience section."""
    items: List[ExperienceItem]


@dataclass
class Profiles:
    """Profiles section."""
    items: List[ProfileItem]


@dataclass
class Skills:
    """Skills section."""
    items: List[SkillItem]


@dataclass
class Sections:
    """All resume sections."""
    summary: Summary
    certifications: Certifications
    education: Education
    experience: Experience
    profiles: Profiles
    skills: Skills


@dataclass
class Resume:
    """Complete resume data."""
    basics: ResumeBasics
    sections: Sections


@dataclass
class ResumeResponse:
    """Response for resume extraction."""
    data: Resume


@dataclass
class JobDetails:
    """Details of a job posting."""
    title: str
    company: str
    location: str
    description: str
    requirements: List[str]
    responsibilities: List[str]
    salary_range: Optional[str] = None
    job_type: Optional[str] = None
    work_type: Optional[str] = None


@dataclass
class JobMatchResult:
    """Result of matching a resume to a job."""
    selected: bool
    feedback: str
    matching_skills: List[str]
    missing_skills: List[str]
    experience_level: str


@dataclass
class ResumeScoringResult:
    """Result of scoring a resume against a job."""
    job_match: float
    job_normalized: str
    resume_normalized: str


@dataclass
class ZoomMeetingResponse:
    """Response for creating a Zoom meeting."""
    join_url: str
    password: str
    start_url: str
    id: str


@dataclass
class JobDescriptionResponse:
    """Response for job description extraction."""
    data: Dict[str, Any]


@dataclass
class RecommendationsResponse:
    """Response for resume recommendations."""
    recommendations: List[str]


@dataclass
class ResumeRewriteResponse:
    """Response for resume section rewrite."""
    text: str


@dataclass
class ResumeScoringResponse:
    """Response for resume scoring."""
    job_match: float
    job_normalized: str
    resume_normalized: str


@dataclass
class IndexesListResponse:
    """Response for listing indexes."""
    indexes: List[str]


@dataclass
class IndexResponse:
    """Response for index operation."""
    done: bool


@dataclass
class SearchResponse:
    """Response for search operation."""
    documents: List[Dict[str, Any]]


@dataclass
class JobDetailsResponse:
    """Response for job details."""
    data: JobDetails
    filtered: bool


@dataclass
class JobSelectionRequest:
    """Request for job selection."""
    resume_details: Dict[str, Any]
    job_details: Dict[str, Any] 