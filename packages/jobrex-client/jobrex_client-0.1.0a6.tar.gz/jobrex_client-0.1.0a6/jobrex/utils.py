import re
from typing import Dict, List


def clean_text(text: str) -> List[str]:
    """
    Clean text by removing special characters and splitting into words.
    
    Args:
        text: Text to clean
        
    Returns:
        List of words in the text
    """
    # Remove special characters and convert to lowercase
    cleaned = re.sub(r'[^\w\s]', '', text.lower())
    # Split into words
    return cleaned.split()


def format_experiences(experiences: List[Dict]) -> str:
    """
    Format a list of experience items into a string.
    
    Args:
        experiences: List of experience dictionaries
        
    Returns:
        Formatted string of experiences
    """
    formatted = []
    for exp in experiences:
        formatted.append(
            f"{exp.get('position')} at {exp.get('company')} ({exp.get('date')}): {exp.get('summary')}"
        )
    return "\n".join(formatted)


def format_skills(skills: List[Dict]) -> str:
    """
    Format a list of skill items into a string.
    
    Args:
        skills: List of skill dictionaries
        
    Returns:
        Formatted string of skills
    """
    return ", ".join([skill.get('name', '') for skill in skills]) 