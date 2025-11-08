import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List


class ApplicationTracker:
    """Track internship applications and their status."""

    def __init__(self, db_path: str = "data/applications.csv"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.df = self._load_database()

    def _load_database(self) -> pd.DataFrame:
        """Load application database from CSV."""
        if self.db_path.exists():
            return pd.read_csv(self.db_path)
        else:
            # Create new DataFrame with schema
            return pd.DataFrame(columns=[
                'application_id',
                'company',
                'position',
                'url',
                'status',
                'submitted_date',
                'last_updated',
                'notes',
                'resume_used',
                'cover_letter_used',
                'filled_fields',
                'unfilled_fields',
                'errors'
            ])

    def _save_database(self):
        """Save application database to CSV."""
        self.df.to_csv(self.db_path, index=False)

    def add_application(self, company: str, position: str, url: str,
                       status: str = "pending", **kwargs) -> str:
        """
        Add a new application to tracker.

        Returns:
            application_id
        """
        application_id = f"{company.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        new_row = {
            'application_id': application_id,
            'company': company,
            'position': position,
            'url': url,
            'status': status,
            'submitted_date': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'notes': kwargs.get('notes', ''),
            'resume_used': kwargs.get('resume_used', ''),
            'cover_letter_used': kwargs.get('cover_letter_used', ''),
            'filled_fields': kwargs.get('filled_fields', 0),
            'unfilled_fields': kwargs.get('unfilled_fields', 0),
            'errors': kwargs.get('errors', '')
        }

        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self._save_database()

        return application_id

    def update_application(self, application_id: str, **kwargs):
        """Update an existing application."""
        if application_id not in self.df['application_id'].values:
            raise ValueError(f"Application ID {application_id} not found")

        idx = self.df[self.df['application_id'] == application_id].index[0]

        for key, value in kwargs.items():
            if key in self.df.columns:
                self.df.at[idx, key] = value

        self.df.at[idx, 'last_updated'] = datetime.now().isoformat()
        self._save_database()

    def mark_submitted(self, application_id: str):
        """Mark an application as submitted."""
        self.update_application(application_id, status='submitted')

    def mark_failed(self, application_id: str, error: str):
        """Mark an application as failed."""
        self.update_application(application_id, status='failed', errors=error)

    def get_application(self, application_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific application by ID."""
        result = self.df[self.df['application_id'] == application_id]
        if result.empty:
            return None
        return result.iloc[0].to_dict()

    def get_applications_by_status(self, status: str) -> pd.DataFrame:
        """Get all applications with a specific status."""
        return self.df[self.df['status'] == status]

    def get_applications_by_company(self, company: str) -> pd.DataFrame:
        """Get all applications for a specific company."""
        return self.df[self.df['company'].str.contains(company, case=False, na=False)]

    def get_recent_applications(self, limit: int = 10) -> pd.DataFrame:
        """Get most recent applications."""
        return self.df.sort_values('submitted_date', ascending=False).head(limit)

    def get_statistics(self) -> Dict[str, Any]:
        """Get application statistics."""
        total = len(self.df)
        if total == 0:
            return {
                'total_applications': 0,
                'submitted': 0,
                'pending': 0,
                'failed': 0,
                'success_rate': 0.0
            }

        status_counts = self.df['status'].value_counts().to_dict()

        return {
            'total_applications': total,
            'submitted': status_counts.get('submitted', 0),
            'pending': status_counts.get('pending', 0),
            'failed': status_counts.get('failed', 0),
            'success_rate': (status_counts.get('submitted', 0) / total) * 100 if total > 0 else 0.0,
            'companies_applied': self.df['company'].nunique(),
            'positions_applied': self.df['position'].nunique()
        }

    def export_report(self, output_path: str = "data/application_report.csv"):
        """Export full application report."""
        self.df.to_csv(output_path, index=False)
        return output_path

    def search_applications(self, query: str) -> pd.DataFrame:
        """Search applications by company or position."""
        mask = (
            self.df['company'].str.contains(query, case=False, na=False) |
            self.df['position'].str.contains(query, case=False, na=False)
        )
        return self.df[mask]
