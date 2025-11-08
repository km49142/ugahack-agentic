import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ProfileManager:
    """Manages user profile data for internship applications."""

    def __init__(self, profile_path: str = "data/user_profile.json"):
        self.profile_path = Path(profile_path)
        self.profile_path.parent.mkdir(parents=True, exist_ok=True)
        self.profile = self._load_profile()

    def _load_profile(self) -> Dict[str, Any]:
        """Load user profile from JSON file."""
        if self.profile_path.exists():
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        return self._create_default_profile()

    def _create_default_profile(self) -> Dict[str, Any]:
        """Create a default profile structure."""
        return {
            "personal_info": {
                "first_name": "",
                "last_name": "",
                "email": "",
                "phone": "",
                "linkedin": "",
                "github": "",
                "portfolio": "",
                "address": {
                    "street": "",
                    "city": "",
                    "state": "",
                    "zip": "",
                    "country": ""
                }
            },
            "education": [],
            "experience": [],
            "skills": {
                "technical": [],
                "languages": [],
                "soft_skills": []
            },
            "projects": [],
            "certifications": [],
            "documents": {
                "resume_path": "",
                "cover_letter_template": "",
                "transcript_path": ""
            },
            "credentials": {}
        }

    def save_profile(self):
        """Save profile to JSON file."""
        with open(self.profile_path, 'w') as f:
            json.dump(self.profile, f, indent=2)

    def update_personal_info(self, **kwargs):
        """Update personal information."""
        self.profile["personal_info"].update(kwargs)
        self.save_profile()

    def add_education(self, school: str, degree: str, major: str,
                     gpa: float, start_date: str, end_date: str, **kwargs):
        """Add education entry."""
        education_entry = {
            "school": school,
            "degree": degree,
            "major": major,
            "gpa": gpa,
            "start_date": start_date,
            "end_date": end_date,
            **kwargs
        }
        self.profile["education"].append(education_entry)
        self.save_profile()

    def add_experience(self, company: str, title: str, start_date: str,
                      end_date: str, description: str, **kwargs):
        """Add work experience entry."""
        experience_entry = {
            "company": company,
            "title": title,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            **kwargs
        }
        self.profile["experience"].append(experience_entry)
        self.save_profile()

    def add_project(self, name: str, description: str, technologies: list,
                   url: Optional[str] = None, **kwargs):
        """Add project entry."""
        project_entry = {
            "name": name,
            "description": description,
            "technologies": technologies,
            "url": url,
            **kwargs
        }
        self.profile["projects"].append(project_entry)
        self.save_profile()

    def get_profile_summary(self) -> str:
        """Get a formatted summary of the profile."""
        summary = f"""
Profile Summary:
----------------
Name: {self.profile['personal_info']['first_name']} {self.profile['personal_info']['last_name']}
Email: {self.profile['personal_info']['email']}
Phone: {self.profile['personal_info']['phone']}

Education: {len(self.profile['education'])} entries
Experience: {len(self.profile['experience'])} entries
Projects: {len(self.profile['projects'])} entries
Skills: {', '.join(self.profile['skills']['technical'][:5])}{'...' if len(self.profile['skills']['technical']) > 5 else ''}
"""
        return summary.strip()

    def export_to_dataframe(self, section: str) -> pd.DataFrame:
        """Export a section of the profile to pandas DataFrame."""
        if section not in self.profile:
            raise ValueError(f"Section '{section}' not found in profile")

        data = self.profile[section]
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            return pd.DataFrame([data])
        else:
            raise ValueError(f"Cannot convert section '{section}' to DataFrame")
