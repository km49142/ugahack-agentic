import PyPDF2
from docx import Document
from pathlib import Path
from typing import Dict, Any


class ResumeParser:
    """Parse resume documents (PDF and DOCX) to extract information."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Resume file not found: {file_path}")

        self.file_type = self.file_path.suffix.lower()
        self.text = self._extract_text()

    def _extract_text(self) -> str:
        """Extract text from resume based on file type."""
        if self.file_type == '.pdf':
            return self._extract_from_pdf()
        elif self.file_type in ['.docx', '.doc']:
            return self._extract_from_docx()
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")

    def _extract_from_pdf(self) -> str:
        """Extract text from PDF file."""
        text = []
        with open(self.file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text.append(page.extract_text())
        return '\n'.join(text)

    def _extract_from_docx(self) -> str:
        """Extract text from DOCX file."""
        doc = Document(self.file_path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)

    def get_text(self) -> str:
        """Get the extracted text."""
        return self.text

    def extract_sections(self) -> Dict[str, str]:
        """
        Extract common resume sections.
        This is a basic implementation - you can enhance with AI later.
        """
        sections = {
            "education": "",
            "experience": "",
            "skills": "",
            "projects": ""
        }

        lines = self.text.split('\n')
        current_section = None

        for line in lines:
            line_lower = line.lower().strip()

            # Detect section headers
            if any(keyword in line_lower for keyword in ['education', 'academic']):
                current_section = 'education'
            elif any(keyword in line_lower for keyword in ['experience', 'employment', 'work history']):
                current_section = 'experience'
            elif any(keyword in line_lower for keyword in ['skills', 'technical skills', 'competencies']):
                current_section = 'skills'
            elif any(keyword in line_lower for keyword in ['projects', 'portfolio']):
                current_section = 'projects'
            elif current_section and line.strip():
                sections[current_section] += line + '\n'

        return sections

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the resume."""
        return {
            "file_path": str(self.file_path),
            "file_type": self.file_type,
            "character_count": len(self.text),
            "word_count": len(self.text.split()),
            "line_count": len(self.text.split('\n'))
        }
