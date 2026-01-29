import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration from environment variables"""

    # Paths
    BASE_DIR = Path(__file__).parent
    CREDENTIALS_DIR = BASE_DIR / 'credentials'
    LOG_DIR = BASE_DIR / 'logs'

    # Google OAuth
    GOOGLE_CREDENTIALS = CREDENTIALS_DIR / 'credentials.json'
    GOOGLE_TOKEN = CREDENTIALS_DIR / 'token_contact_xshift.json'
    CALENDAR_ID = os.getenv('CALENDAR_ID', 'primary')
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    # Email settings
    SMTP_USER = os.getenv('SMTP_USER', 'contact@xshift.ai')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'nmarbach@gmail.com')

    # Logging
    LOG_FILE = LOG_DIR / 'daily_calendar_email.log'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Timezone
    TIMEZONE = os.getenv('TIMEZONE', 'America/New_York')

    def validate(self):
        """Ensure required settings present"""
        if not self.SMTP_PASSWORD:
            raise ValueError("SMTP_PASSWORD not set in .env")
        if not self.GOOGLE_CREDENTIALS.exists():
            raise ValueError(f"Credentials missing: {self.GOOGLE_CREDENTIALS}")

        # Create directories if needed
        self.CREDENTIALS_DIR.mkdir(exist_ok=True)
        self.LOG_DIR.mkdir(exist_ok=True)
