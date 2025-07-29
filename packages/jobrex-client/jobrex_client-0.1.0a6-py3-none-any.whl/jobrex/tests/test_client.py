"""
Tests for the client module.
"""
import pytest
import json
import os
from unittest.mock import patch, Mock, mock_open
from jobrex.client import BaseClient, ResumesClient, JobsClient, SubscriptionClient
from jobrex.models import (
    Resume, ResumeResponse, JobDetailsResponse, ZoomMeetingResponse,
    ResumeRewriteResponse, IndexesListResponse, IndexResponse, SearchResponse,
    JobMatchResult
)


class TestBaseClient:
    """Tests for the BaseClient class."""
    
    def test_init(self):
        """Test initialization of BaseClient."""
        client = BaseClient(api_key="test_api_key")
        assert client.api_key == "test_api_key"
        assert client.base_url == "https://api.jobrex.ai"
        assert "Authorization" in client.session.headers
        assert client.session.headers["Authorization"] == "Api-Key test_api_key"
        
        # Test with custom base URL
        client = BaseClient(api_key="test_api_key", base_url="https://custom.api.com/")
        assert client.base_url == "https://custom.api.com"
    
    @patch("requests.Session.request")
    def test_make_request(self, mock_request):
        """Test the _make_request method."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_response.text = '{"status": "success"}'
        mock_request.return_value = mock_response
        
        client = BaseClient(api_key="test_api_key")
        result = client._make_request("GET", "test/endpoint", params={"key": "value"})
        
        # Verify request was made correctly
        mock_request.assert_called_once_with(
            "GET", 
            "https://api.jobrex.ai/test/endpoint", 
            params={"key": "value"}
        )
        assert result == {"status": "success"}
        
        # Test with error response
        mock_response.raise_for_status.side_effect = Exception("API Error")
        with pytest.raises(Exception, match="API Error"):
            client._make_request("GET", "test/endpoint")


class TestResumesClient:
    """Tests for the ResumesClient class."""
    
    @patch("jobrex.client.BaseClient._make_request")
    def test_extract_resume(self, mock_make_request):
        """Test the parse_resume method."""
        # Setup mock response
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
        
        # Mock open file
        m = mock_open(read_data="fake resume content")
        with patch("builtins.open", m):
            client = ResumesClient(api_key="test_api_key")
            result = client.extract_resume("fake_resume.pdf")
        
        # Verify request was made correctly
        mock_make_request.assert_called_once()
        assert mock_make_request.call_args[0][0] == "POST"
        assert mock_make_request.call_args[0][1] == "v1/resumes/extract/"
        assert "files" in mock_make_request.call_args[1]
        
        # Verify result
        assert "data" in result
        assert "basics" in result["data"]
        assert result["data"]["basics"]["name"] == "John Doe"
    
    @patch("jobrex.client.BaseClient._make_request")
    def test_tailor_resume(self, mock_make_request):
        """Test the tailor_resume method."""
        # Setup mock data
        resume_details = Mock(spec=Resume)
        job_details = {"title": "Software Engineer", "description": "Job description"}
        sections = ["summary", "experience"]
        
        # Setup mock response
        mock_make_request.return_value = {
            "basics": {
                "name": "John Doe",
                "headline": "Software Engineer",
                "email": "john@example.com",
                "phone": "123-456-7890",
                "location": "New York, NY"
            },
            "sections": {
                "summary": {"content": "Tailored summary for Software Engineer"},
                "certifications": {"items": []},
                "education": {"items": []},
                "experience": {"items": []},
                "profiles": {"items": []},
                "skills": {"items": []}
            }
        }
        
        client = ResumesClient(api_key="test_api_key")
        result = client.tailor_resume(resume_details, job_details, sections)
        
        # Verify request was made correctly
        mock_make_request.assert_called_once()
        assert mock_make_request.call_args[0][0] == "POST"
        assert mock_make_request.call_args[0][1] == "v1/resumes/tailor/"
        assert "json" in mock_make_request.call_args[1]
        
        # Verify result
        assert "basics" in result
        assert result["basics"]["name"] == "John Doe"
        assert "sections" in result
        assert result["sections"]["summary"]["content"] == "Tailored summary for Software Engineer"
    
    @patch("jobrex.client.BaseClient._make_request")
    def test_rewrite_resume(self, mock_make_request):
        """Test the rewrite_resume method."""
        # Setup mock response
        mock_make_request.return_value = {
            "text": "Improved resume section content"
        }
        
        client = ResumesClient(api_key="test_api_key")
        result = client.rewrite_resume("Original content", "summary")
        
        # Verify request was made correctly
        mock_make_request.assert_called_once()
        assert mock_make_request.call_args[0][0] == "POST"
        assert mock_make_request.call_args[0][1] == "v1/resumes/rewrite/"
        assert "json" in mock_make_request.call_args[1]
        assert mock_make_request.call_args[1]["json"]["text"] == "Original content"
        assert mock_make_request.call_args[1]["json"]["type"] == "summary"
        
        # Verify result
        assert "text" in result
        assert result["text"] == "Improved resume section content"
    
    @patch("jobrex.client.BaseClient._make_request")
    def test_list_resume_indexes(self, mock_make_request):
        """Test the list_resume_indexes method."""
        # Setup mock response
        mock_make_request.return_value = {
            "indexes": ["index1", "index2", "index3"]
        }
        
        client = ResumesClient(api_key="test_api_key")
        result = client.list_resume_indexes()
        
        # Verify request was made correctly
        mock_make_request.assert_called_once()
        assert mock_make_request.call_args[0][0] == "GET"
        assert mock_make_request.call_args[0][1] == "v1/resumes/list-indexes/"
        
        # Verify result
        assert "indexes" in result
        assert result["indexes"] == ["index1", "index2", "index3"]


class TestJobsClient:
    """Tests for the JobsClient class."""
    
    @patch("jobrex.client.BaseClient._make_request")
    def test_candidate_scoring(self, mock_make_request):
        """Test the candidate_scoring method."""
        # Setup mock data
        job_details = {"title": "Software Engineer", "description": "Job description"}
        resume_details = {"name": "John Doe", "skills": ["Python", "JavaScript"]}
        
        # Setup mock response
        mock_make_request.return_value = {
            "selected": True,
            "feedback": "Good match for the position",
            "matching_skills": ["Python", "JavaScript"],
            "missing_skills": ["React"],
            "experience_level": "Mid-level"
        }
        
        client = JobsClient(api_key="test_api_key")
        result = client.candidate_scoring(job_details, resume_details)
        
        # Verify request was made correctly
        mock_make_request.assert_called_once()
        assert mock_make_request.call_args[0][0] == "POST"
        assert mock_make_request.call_args[0][1] == "v1/jobs/candidate-scoring/"
        assert "json" in mock_make_request.call_args[1]
        
        # Verify result
        assert "selected" in result
        assert result["selected"] is True
        assert "feedback" in result
        assert "matching_skills" in result
        assert "missing_skills" in result
        assert "experience_level" in result
    
    @patch("jobrex.client.BaseClient._make_request")
    def test_job_writing(self, mock_make_request):
        """Test the job_writing method."""
        # Setup mock response
        mock_make_request.return_value = {
            "data": {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "location": "Remote",
                "description": "Job description content",
                "requirements": ["Python", "JavaScript"],
                "responsibilities": ["Develop web applications"]
            },
            "filtered": False
        }
        
        client = JobsClient(api_key="test_api_key")
        result = client.job_writing(
            job_title="Software Engineer",
            hiring_needs="Need a skilled developer",
            company_description="Tech company",
            job_type="Full-time",
            job_location="Remote",
            specific_benefits="Health insurance, 401k"
        )
        
        # Verify request was made correctly
        mock_make_request.assert_called_once()
        assert mock_make_request.call_args[0][0] == "POST"
        assert mock_make_request.call_args[0][1] == "v1/jobs/job-writing/"
        assert "json" in mock_make_request.call_args[1]
        
        # Verify result
        assert "data" in result
        assert result["data"]["title"] == "Software Engineer"
        assert "filtered" in result
        assert result["filtered"] is False
    
    @patch("jobrex.client.BaseClient._make_request")
    def test_extract_job_description(self, mock_make_request):
        """Test the extract_job_description method."""
        # Setup mock response
        mock_make_request.return_value = {
            "data": {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "location": "Remote",
                "description": "Job description content",
                "requirements": ["Python", "JavaScript"],
                "responsibilities": ["Develop web applications"]
            },
            "filtered": False
        }
        
        client = JobsClient(api_key="test_api_key")
        result = client.extract_job_description("Job description content")
        
        # Verify request was made correctly
        mock_make_request.assert_called_once()
        assert mock_make_request.call_args[0][0] == "POST"
        assert mock_make_request.call_args[0][1] == "v1/jobs/extract-job-description/"
        assert "json" in mock_make_request.call_args[1]
        assert mock_make_request.call_args[1]["json"]["text"] == "Job description content"
        
        # Verify result
        assert "data" in result
        assert result["data"]["title"] == "Software Engineer" 
        

class TestSubscriptionClient:
    @patch("jobrex.client.BaseClient._make_request")
    def test_subscriptions_info(self, mock_make_request):
        """Test the subscriptions_info method."""
        mock_make_request.return_value = {
            "subscription_period": "monthly",
            "total_requests_allowed": 10000,
            "requests_used": 500,
            "remaining_requests": 9500,
            "reset_date": "2025-06-01T00:00:00Z",
        }
        
        client = SubscriptionClient(api_key="test_api_key")
        result = client.subscriptions_info()
        
        # Verify request was made correctly
        mock_make_request.assert_called_once()
        assert mock_make_request.call_args[0][0] == "GET"
        assert mock_make_request.call_args[0][1] == "v1/subscriptions/info/"
        
        # Verify result
        assert result["subscription_period"] == "monthly"
        assert result["total_requests_allowed"] == 10000
        assert result["requests_used"] == 500
        assert result["remaining_requests"] == 9500