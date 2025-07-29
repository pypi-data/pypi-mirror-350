"""
Integration tests for the jobrex client.

These tests verify that the client and models work together correctly.
"""
import pytest
from unittest.mock import patch, Mock, mock_open
from jobrex.client import ResumesClient, JobsClient
from jobrex.models import (
    Resume, ResumeBasics, Summary, Certifications, Education, Experience,
    Profiles, Skills, Sections, JobDetails
)


class TestResumesClientIntegration:
    """Integration tests for the ResumesClient."""
    
    @patch("jobrex.client.BaseClient._make_request")
    def test_parse_and_tailor_resume(self, mock_make_request, sample_resume, sample_job_details):
        """Test parsing a resume and then tailoring it."""
        # Mock the extract_resume response
        mock_make_request.return_value = {
            "data": {
                "basics": {
                    "name": "John Doe",
                    "headline": "Software Engineer",
                    "email": "john@example.com",
                    "phone": "123-456-7890",
                    "location": "New York, NY"
                },
                "sections": {
                    "summary": {"content": "Experienced software engineer"},
                    "certifications": {"items": []},
                    "education": {"items": []},
                    "experience": {"items": []},
                    "profiles": {"items": []},
                    "skills": {"items": []}
                }
            }
        }
        
        # First call to parse resume
        client = ResumesClient(api_key="test_api_key")
        m = mock_open(read_data="fake resume content")
        with patch("builtins.open", m):
            parse_result = client.extract_resume("fake_resume.pdf")
        
        # Mock the tailor_resume response
        mock_make_request.return_value = {
            "basics": {
                "name": "John Doe",
                "headline": "Senior Software Engineer",  # Updated headline
                "email": "john@example.com",
                "phone": "123-456-7890",
                "location": "New York, NY"
            },
            "sections": {
                "summary": {"content": "Tailored summary for Senior Software Engineer position"},
                "certifications": {"items": []},
                "education": {"items": []},
                "experience": {"items": []},
                "profiles": {"items": []},
                "skills": {"items": []}
            }
        }
        
        # Now tailor the resume
        sections_to_tailor = ["summary", "experience"]
        tailor_result = client.tailor_resume(sample_resume, sample_job_details, sections_to_tailor)
        
        # Verify the results
        assert parse_result["data"]["basics"]["name"] == "John Doe"
        assert tailor_result["basics"]["headline"] == "Senior Software Engineer"
        assert "Tailored summary" in tailor_result["sections"]["summary"]["content"]
        
        # Verify the correct API calls were made
        assert mock_make_request.call_count == 2
        # First call should be to parse endpoint
        assert mock_make_request.call_args_list[0][0][1] == "v1/resumes/extract/"
        # Second call should be to tailor endpoint
        assert mock_make_request.call_args_list[1][0][1] == "v1/resumes/tailor/"


class TestJobsClientIntegration:
    """Integration tests for the JobsClient."""
    
    @patch("jobrex.client.BaseClient._make_request")
    def test_write_and_parse_job(self, mock_make_request):
        """Test writing a job description and then parsing it."""
        # Mock the extract_job_description response
        job_response = {
            "data": {
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "location": "Remote",
                "description": "We are looking for a skilled software engineer...",
                "requirements": ["Python", "JavaScript", "AWS"],
                "responsibilities": ["Develop web applications", "Mentor junior developers"],
                "salary_range": "$120,000 - $150,000",
                "job_type": "Full-time",
                "work_type": "Remote"
            },
            "filtered": False
        }
        mock_make_request.return_value = job_response
        
        # First call to write job description
        client = JobsClient(api_key="test_api_key")
        write_result = client.job_writing(
            job_title="Senior Software Engineer",
            hiring_needs="Need a skilled developer with 5+ years of experience",
            company_description="Tech Corp is a leading software company",
            job_type="Full-time",
            job_location="Remote",
            specific_benefits="Health insurance, 401k, unlimited PTO"
        )
        
        # Mock the parse_job_description response (same as write response for simplicity)
        mock_make_request.return_value = job_response
        
        # Now parse the job description
        job_content = write_result["data"]["description"]
        parse_result = client.extract_job_description(job_content)
        
        # Verify the results
        assert write_result["data"]["title"] == "Senior Software Engineer"
        assert parse_result["data"]["title"] == "Senior Software Engineer"
        assert "Python" in parse_result["data"]["requirements"]
        
        # Verify the correct API calls were made
        assert mock_make_request.call_count == 2
        # First call should be to write endpoint
        assert mock_make_request.call_args_list[0][0][1] == "v1/jobs/job-writing/"
        # Second call should be to parse endpoint
        assert mock_make_request.call_args_list[1][0][1] == "v1/jobs/extract-job-description/"
        
        # Verify the correct parameters were passed
        assert "json" in mock_make_request.call_args_list[1][1]
        assert mock_make_request.call_args_list[1][1]["json"]["text"] == job_content
    
    @patch("jobrex.client.BaseClient._make_request")
    def test_job_candidate_matching(self, mock_make_request, sample_resume, sample_job_details):
        """Test matching a candidate to a job."""
        # Mock the candidate_scoring response
        mock_make_request.return_value = {
            "selected": True,
            "feedback": "Great match for the position",
            "matching_skills": ["Python", "JavaScript"],
            "missing_skills": ["AWS"],
            "experience_level": "Senior"
        }
        
        # Convert sample_resume to dict for the API call
        resume_dict = {
            "name": sample_resume.basics.name,
            "headline": sample_resume.basics.headline,
            "summary": sample_resume.sections.summary.content,
            "skills": []
        }
        
        client = JobsClient(api_key="test_api_key")
        result = client.candidate_scoring(sample_job_details, resume_dict)
        
        # Verify the results
        assert result["selected"] is True
        assert "Great match" in result["feedback"]
        assert "Python" in result["matching_skills"]
        assert "AWS" in result["missing_skills"]
        assert result["experience_level"] == "Senior"
        
        # Verify the correct API call was made
        mock_make_request.assert_called_once()
        assert mock_make_request.call_args[0][0] == "POST"
        assert mock_make_request.call_args[0][1] == "v1/jobs/candidate-scoring/" 