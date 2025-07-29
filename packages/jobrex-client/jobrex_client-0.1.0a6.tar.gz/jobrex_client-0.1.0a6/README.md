# Jobrex Client

Jobrex Client is a Python package that provides a simple interface to interact with the Jobrex API, which offers AI-powered recruitment services including resume parsing, job matching, and more.

## Features

* Resume parsing and analysis
* Job description extraction and analysis
* Resume and job matching
* Zoom meeting creation for interviews
* Indexing and searching of resumes and jobs
* Resume rewriting and tailoring for job applications

## Installation

You can install Jobrex Client using pip:
```
pip install jobrex-client
```
## Usage

### Parsing a Resume

```python
from jobrex import ResumesClient, LayoutMode

# Initialize the client with your API key
client = ResumesClient(api_key="your_api_key_here")

# Basic resume parsing
resume_response = client.extract_resume("path/to/your/resume.pdf")

# Parse resume with layout engine enabled (using default TXT mode)
resume_response = client.extract_resume(
    "path/to/your/resume.pdf",
    enable_layout=True
)

# Parse resume with layout engine and specific mode
resume_response = client.extract_resume(
    "path/to/your/resume.pdf",
    enable_layout=True,
    layout_mode=LayoutMode.OCR  # Options: LayoutMode.AUTO, LayoutMode.TXT, LayoutMode.OCR
)
print(resume_response)
```


### Tailoring a Resume

```python
from jobrex import ResumesClient

# Initialize the client with your API key
client = ResumesClient(api_key="your_api_key_here")

# User data and job details
resume_details = {
    "basics": {
        "name": "John Doe",
        "headline": "Senior Software Engineer",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "location": "San Francisco, CA",
        "url": {
            "label": "Portfolio",
            "href": "https://johndoe.com"
        }
    },
    "sections": {
        "experience": {
            "items": [
                {
                    "company": "Tech Solutions Inc",
                    "position": "Senior Software Engineer",
                    "location": "San Francisco, CA",
                    "date": "2020-Present",
                    "summary": "Led development of machine learning pipelines and APIs serving millions of users",
                    "url": {
                        "label": "Tech Solutions Inc",
                        "href": "https://techsolutions.com"
                    }
                },
                {
                    "company": "Data Analytics Co",
                    "position": "Software Engineer",
                    "location": "Seattle, WA", 
                    "date": "2018-2020",
                    "summary": "Developed Python microservices and data processing workflows",
                    "url": {
                        "label": "TData Analytics Co",
                        "href": "https://datago.com"
                    }
                }
            ]
        },
        "certifications": {
            "items": [
                {
                    "name": "AWS Certified Solutions Architect",
                    "issuer": "Amazon Web Services",
                    "date": "2022",
                    "summary": "Professional level cloud architecture certification",
                    "url": {
                        "label": "Verify",
                        "href": "https://aws.amazon.com/verification"
                    }
                },
                {
                    "name": "Professional Scrum Master I",
                    "issuer": "Scrum.org", 
                    "date": "2021",
                    "summary": "Certification in Agile project management and Scrum framework",
                    "url": {
                        "label": "Certificate",
                        "href": "https://www.scrum.org/certificates"
                    }
                }
            ]
        },
        "education": {
            "items":[
            {
                "institution": "University of Technology",
                "studyType": "Bachelor's Degree",
                "area": "Computer Science",
                "score": "3.8",
                "date": "2014-2018",
                "summary": "Focused on software development and machine learning.",
                "url": {
                    "label": "University Website",
                    "href": "https://www.universityoftechnology.edu"
                }
            },
            {
                "institution": "Online Learning Platform",
                "studyType": "Certification",
                "area": "Data Science",
                "score": "Completed",
                "date": "2020",
                "summary": "Completed a comprehensive course on data analysis and machine learning.",
                "url": {
                    "label": "Course Certificate",
                    "href": "https://www.onlinelearningplatform.com/certificate"
                }
            }
            ]
        },
        "profiles": {
            "items": [
            {
                "id": "linkedin_profile",
                "network": "LinkedIn",
                "icon": "https://example.com/linkedin-icon.png",
                "url": {
                    "label": "View Profile",
                    "href": "https://www.linkedin.com/in/yourprofile"
                }
            },
            {
                "id": "github_profile",
                "network": "GitHub",
                "icon": "https://example.com/github-icon.png",
                "url": {
                    "label": "View Profile",
                    "href": "https://github.com/yourusername"
                }
            },
            {
                "id": "personal_website",
                "network": "Personal Website",
                "icon": "https://example.com/website-icon.png",
                "url": {
                    "label": "Visit Website",
                    "href": "https://www.yourwebsite.com"
                }
            }
            ]
        },
        "summary": {
            "content": "Experienced software engineer with 5+ years in Python development."
        },
        "skills": {
            "items": [
                {
                    "name": "Python",
                    "description": "Advanced proficiency",
                    "keywords": ["Django", "Flask", "FastAPI"]
                },
                {
                    "name": "Machine Learning",
                    "description": "Intermediate level",
                    "keywords": ["TensorFlow", "scikit-learn"]
                }
            ]
        }
    }
}

job_details = {
    "title": "Senior Software Engineer",
    "company": "XYZ Corp",
    "description": "Looking for an experienced Python developer with machine learning expertise...",
    "requirements": [
        "5+ years of Python development",
        "Experience with machine learning frameworks",
        "Strong problem-solving skills"
    ]
}

# Tailor the resume
tailored_response = client.tailor_resume(resume_details, job_details, ["summary", "certifications", "experience", "education", "skills"])
print(tailored_response)
```

### Rewriting a Resume Section

```python
from jobrex import ResumesClient

# Initialize the client with your API key
client = ResumesClient(api_key="your_api_key_here")

# Text to rewrite and optional prompt
text = "I have experience in software development and data analysis."
section = "summary"

# Rewrite the resume section
rewritten_response = client.rewrite_resume(text, section)
print(rewritten_response)
```

### Listing Resume Indexes

```python
from jobrex import ResumesClient

# Initialize the client with your API key
client = ResumesClient(api_key="your_api_key_here")

# List resume indexes
indexes_response = client.list_resume_indexes()
print(indexes_response)
```

### Searching Resumes

```python
from jobrex import ResumesClient

# Initialize the client with your API key
client = ResumesClient(api_key="your_api_key_here")

# Search for resumes
query = "Data Scientist"
index_name = "my_resume_index"
top_k = 10

search_response = client.search_resumes(query, index_name, top_k=10)
print(search_response)
```
### Indexing Resumes

```python
from jobrex import ResumesClient

# Initialize the client with your API key
client = ResumesClient(api_key="your_api_key_here")

# Documents to index
documents = [
    {"resume_id": "r123", "resume_data": """{"basics": {"name": "John Doe", "headline": "Senior Software Engineer", "email": "john.doe@example.com", "phone": "123-456-7890", "location": "San Francisco, CA", "url": {"label": "Portfolio", "href": "https://johndoe.com"}}, "sections": {"experience": {"items": [{"company": "Tech Solutions Inc", "position": "Senior Software Engineer", "location": "San Francisco, CA", "date": "2020-Present", "summary": "Led development of machine learning pipelines and APIs serving millions of users", "url": {"label": "Tech Solutions Inc", "href": "https://techsolutions.com"}}, {"company": "Data Analytics Co", "position": "Software Engineer", "location": "Seattle, WA", "date": "2018-2020", "summary": "Developed Python microservices and data processing workflows", "url": {"label": "TData Analytics Co", "href": "https://datago.com"}}]}, "certifications": {"items": [{"name": "AWS Certified Solutions Architect", "issuer": "Amazon Web Services", "date": "2022", "summary": "Professional level cloud architecture certification", "url": {"label": "Verify", "href": "https://aws.amazon.com/verification"}}, {"name": "Professional Scrum Master I", "issuer": "Scrum.org", "date": "2021", "summary": "Certification in Agile project management and Scrum framework", "url": {"label": "Certificate", "href": "https://www.scrum.org/certificates"}}]}, "education": {"items": [{"institution": "University of Technology", "studyType": "Bachelor\'s Degree", "area": "Computer Science", "score": "3.8", "date": "2014-2018", "summary": "Focused on software development and machine learning.", "url": {"label": "University Website", "href": "https://www.universityoftechnology.edu"}}, {"institution": "Online Learning Platform", "studyType": "Certification", "area": "Data Science", "score": "Completed", "date": "2020", "summary": "Completed a comprehensive course on data analysis and machine learning.", "url": {"label": "Course Certificate", "href": "https://www.onlinelearningplatform.com/certificate"}}]}, "profiles": {"items": [{"id": "linkedin_profile", "network": "LinkedIn", "icon": "https://example.com/linkedin-icon.png", "url": {"label": "View Profile", "href": "https://www.linkedin.com/in/yourprofile"}}, {"id": "github_profile", "network": "GitHub", "icon": "https://example.com/github-icon.png", "url": {"label": "View Profile", "href": "https://github.com/yourusername"}}, {"id": "personal_website", "network": "Personal Website", "icon": "https://example.com/website-icon.png", "url": {"label": "Visit Website", "href": "https://www.yourwebsite.com"}}]}, "summary": {"content": "Experienced software engineer with 5+ years in Python development."}, "skills": {"items": [{"name": "Python", "description": "Advanced proficiency", "keywords": ["Django", "Flask", "FastAPI"]}, {"name": "Machine Learning", "description": "Intermediate level", "keywords": ["TensorFlow", "scikit-learn"]}]}}}"""},
]
index_name = "my_resume_index"
id_field = "resume_id"
search_fields = ["resume_data"]
# Index the resumes
index_response = client.index_resume(documents, index_name, id_field, search_fields, department_name=None)
print(index_response)
```

### Deleting Resumes

```python
from jobrex import ResumesClient

# Initialize the client with your API key
client = ResumesClient(api_key="your_api_key_here")

# List of document IDs to delete
documents_ids = ["r123"]
index_name = "my_resume_index"

# Delete the resumes
delete_response = client.delete_resumes(documents_ids, index_name)
print(delete_response)
```

### Searching Jobrex Resumes

```python
from jobrex import ResumesClient

# Initialize the client with your API key
client = ResumesClient(api_key="your_api_key_here")

# Search for resumes in the Jobrex pool
query = "Data Scientist"
top_k = 10

search_response = client.search_jobrex(query, top_k=10)
print(search_response)
```

### Getting Candidate Score

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Job details and resume details
job_details = {
    "title": "Senior Software Engineer",
    "company": "XYZ Corp",
    "description": "Looking for an experienced Python developer with machine learning expertise...",
    "requirements": [
        "5+ years of Python development",
        "Experience with machine learning frameworks",
        "Strong problem-solving skills"
    ]
}

resume_details = {
    "basics": {
        "name": "John Doe",
        "headline": "Senior Software Engineer",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "location": "San Francisco, CA"
    },
    "skills": ["Python", "Machine Learning"]
}

# Get candidate score
score_response = client.candidate_scoring(job_details, resume_details)
print(score_response)
```

### Writing Job Description

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Job details
job_title = "Senior Software Engineer"
hiring_needs = "Looking for a skilled developer with experience in Python and machine learning."
company_description = "XYZ Corp is a leading tech company."
job_type = "Full-time"
job_location = "San Francisco, CA"
specific_benefits = "Health insurance, 401k, and flexible hours."

# Write job description
job_description_response = client.job_writing(
    job_title, hiring_needs, company_description, job_type, job_location, specific_benefits
)
print(job_description_response)
```

### Parsing Job Description

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Job site content
job_site_content = "We are looking for a Senior Software Engineer with experience in Python and machine learning."

# Parse job description
parsed_job_response = client.extract_job_description(job_site_content)
print(parsed_job_response)
```

### Creating a Zoom Meeting

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Zoom meeting details
client_id = "your_zoom_client_id"
client_secret = "your_zoom_client_secret"
account_id = "your_zoom_account_id"
duration = 60  # Duration in minutes
start_time = "2023-10-01T10:00:00Z"  # ISO format
timezone = "America/Los_Angeles"
topic = "Interview for Senior Software Engineer Position"

# Create Zoom meeting
zoom_meeting_response = client.create_zoom_meeting(
    client_id, client_secret, account_id, duration, start_time, timezone, topic
)
print(zoom_meeting_response)
```

### Listing Job Indexes

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# List job indexes
indexes_response = client.list_job_indexes()
print(indexes_response)
```

### Searching Jobs

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Search for jobs
query = "Software Engineer"
index_name = "my_job_index"
top_k = 10

search_response = client.search_jobs(query, index_name, top_k=10)
print(search_response)
```

### Deleting a Job

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# List of document IDs to delete
documents_ids = ["job_id_1", "job_id_2"]
index_name = "my_job_index"

# Delete the jobs
delete_response = client.delete_job(documents_ids, index_name)
print(delete_response)
```

### Indexing Jobs

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Documents to index
documents = [
    {"job_id": "job_1", "job_data": """{"title": "Software Engineer", "company": "XYZ Corp"}"""},
    {"job_id": "job_2", "job_data": """{"title": "Data Scientist", "company": "ABC Inc"}"""}
]
index_name = "my_job_index"
id_field = "job_id"
search_fields = ["job_data"]
# Index the jobs
index_response = client.index_job(documents, index_name, id_field, search_fields, department_name=None)
print(index_response)
```

### Generating Screening Questions

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Job and resume details
job_details = {
    "title": "Senior Software Engineer",
    "company": "XYZ Corp",
    "description": "Looking for an experienced Python developer with machine learning expertise...",
    "requirements": [
        "5+ years of Python development",
        "Experience with machine learning frameworks",
        "Strong problem-solving skills"
    ]
}

resume_details = {
    "basics": {
        "name": "John Doe",
        "headline": "Senior Software Engineer",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "location": "San Francisco, CA"
    },
    "skills": ["Python", "Machine Learning"],
    "experience": [
        {
            "title": "Senior Software Engineer",
            "company": "Tech Corp",
            "duration": "3 years",
            "description": "Led development of ML pipelines..."
        }
    ]
}

# Generate screening questions
questions_response = client.generate_screening_questions(resume_details, job_details)
print(questions_response)
```

### Generating Interview Criteria

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Job details
job_details = {
    "title": "Senior Software Engineer",
    "company": "XYZ Corp",
    "description": "Looking for an experienced Python developer with machine learning expertise...",
    "requirements": [
        "5+ years of Python development",
        "Experience with machine learning frameworks",
        "Strong problem-solving skills"
    ]
}

# Generate interview criteria (default type is "technical")
technical_criteria = client.generate_interview_criteria(job_details)
print(technical_criteria)

# Generate behavioral interview criteria
behavioral_criteria = client.generate_interview_criteria(job_details, interview_type="behavioral")
print(behavioral_criteria)
```

### Generating Offer Letter

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Job and candidate details
job_details = {
    "title": "Senior Software Engineer",
    "company": "XYZ Corp",
    "description": "Looking for an experienced Python developer...",
    "requirements": [
        "5+ years of Python development",
        "Experience with machine learning frameworks",
        "Strong problem-solving skills"
    ]
}

resume_details = {
    "basics": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "location": "San Francisco, CA"
    },
    "experience": [
        {
            "title": "Senior Software Engineer",
            "company": "Tech Corp",
            "duration": "3 years",
            "description": "Led development of ML pipelines..."
        }
    ]
}

# Additional offer details
salary = "$150,000 per year with 15% annual bonus"
benefits = "Health insurance, 401k matching, unlimited PTO"
company_policies = "Flexible work hours, remote work options"

# Generate offer letter
offer_letter = client.generate_offer_letter(
    job_details, 
    resume_details, 
    salary=salary, 
    benefits=benefits, 
    company_policies=company_policies
)
print(offer_letter)
```

### Generating Screening Email

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Job and resume details
job_details = {
    "title": "Senior Software Engineer",
    "company": "XYZ Corp",
    "description": "Looking for an experienced Python developer...",
    "requirements": [
        "5+ years of Python development",
        "Experience with machine learning frameworks",
        "Strong problem-solving skills"
    ]
}

resume_details = {
    "basics": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "location": "San Francisco, CA"
    },
    "experience": [
        {
            "title": "Senior Software Engineer",
            "company": "Tech Corp",
            "duration": "3 years",
            "description": "Led development of ML pipelines..."
        }
    ]
}

# Questionnaire responses
questionnaire_responses = [
    {
        "question": "How many years of Python experience do you have?",
        "answer": "I have 7 years of professional Python development experience."
    },
    {
        "question": "Describe your experience with machine learning frameworks.",
        "answer": "I have extensive experience with TensorFlow and PyTorch, having built and deployed multiple production ML models."
    }
]

# Generate screening email
screening_email = client.generate_screening_email(resume_details, job_details, questionnaire_responses)
print(screening_email)
```

### Getting Calendar Available Times

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Calendar availability parameters
recruiter_email = "recruiter@company.com"
date = "2024-04-10"  # YYYY-MM-DD format
working_start_hour = 9  # 9 AM
working_end_hour = 17   # 5 PM
time_zone = "America/New_York"
calendar_provider = "google"  # or "outlook"
calendar_credentials = {
    "access_token": "your_calendar_api_access_token",
    "refresh_token": "your_calendar_api_refresh_token",
    # Add other required credentials based on the provider
}

# Get available time slots
available_times = client.get_calendar_available_times(
    recruiter_email=recruiter_email,
    date=date,
    working_start_hour=working_start_hour,
    working_end_hour=working_end_hour,
    time_zone=time_zone,
    calendar_provider=calendar_provider,
    calendar_credentials=calendar_credentials
)
print(available_times)
```

### Getting Zoom Meeting Transcript

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Zoom meeting details
meeting_id = "your_zoom_meeting_id"
access_token = "your_zoom_access_token"

# Get the transcript
transcript = client.retrieve_zoom_transcript(meeting_id, access_token)
print(transcript)
```

### Getting Teams Meeting Transcript

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Teams meeting details
meeting_id = "your_teams_meeting_id"
access_token = "your_teams_access_token"

# Get the transcript
transcript = client.get_teams_transcript(meeting_id, access_token)
print(transcript)
```

### Extracting Interview Responses

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Interview transcript details
transcript = """
WEBVTT

00:00:00.000 --> 00:00:05.000
Interviewer: Tell me about your experience with Python.

00:00:05.000 --> 00:00:15.000
Candidate: I have 5 years of experience using Python for web development...
"""
interviewee_name = "John Doe"
interviewer_name = "Jane Smith"

# Extract responses
responses = client.extract_interview_responses(
    transcript=transcript,
    interviewee_name=interviewee_name,
    interviewer_name=interviewer_name
)
print(responses)
```

### Generating Final Interview Report

```python
from jobrex import JobsClient

# Initialize the client with your API key
client = JobsClient(api_key="your_api_key_here")

# Interview evaluation details
transcript = """
WEBVTT

00:00:00.000 --> 00:00:05.000
Interviewer: Tell me about your experience with Python.

00:00:05.000 --> 00:00:15.000
Candidate: I have 5 years of experience using Python for web development...
"""

evaluation_criteria = [
    {
        "criteria_name": "Technical Skills",
        "weight": 0.4,
        "description": "Evaluate the candidate's technical knowledge and experience"
    },
    {
        "criteria_name": "Communication",
        "weight": 0.3,
        "description": "Assess how well the candidate explains technical concepts"
    },
    {
        "criteria_name": "Problem Solving",
        "weight": 0.3,
        "description": "Evaluate the candidate's approach to solving technical challenges"
    }
]

# Generate the report
report = client.generate_final_report(
    transcript=transcript,
    evaluation_criteria=evaluation_criteria,
    chunk_size=4000,  # Optional: Size of text chunks for processing
    overlap_size=200  # Optional: Overlap between chunks
)
print(report)
```

### Get Subscription Info

```python
from jobrex import SubscriptionClient

# Initialize the client with your API key
client = SubscriptionClient(api_key="your_api_key_here")

subscription_info_response = client.subscriptions_info()
print(subscription_info_response)
```

## License

Jobrex Client is licensed under the MIT License.

