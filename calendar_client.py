"""
Google Calendar client for fetching events
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

class CalendarClient:
    """Client for accessing Google Calendar"""

    def __init__(self, credentials_path: Path, token_path: Path, calendar_id: str = 'primary', timezone: str = 'America/New_York'):
        """Initialize calendar client with OAuth credentials"""
        self.timezone = pytz.timezone(timezone)
        self.calendar_id = calendar_id
        self.service = self._authenticate(credentials_path, token_path)

    def _authenticate(self, credentials_path: Path, token_path: Path):
        """Authenticate and return calendar service"""

        if not token_path.exists():
            raise FileNotFoundError(
                f"Token not found at {token_path}. Run setup_auth.py first."
            )

        # Load credentials from token
        creds = Credentials.from_authorized_user_file(str(token_path))

        # Refresh if expired
        if creds.expired and creds.refresh_token:
            logger.info("Refreshing expired credentials")
            creds.refresh(Request())

            # Save refreshed token
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        # Build calendar service
        service = build('calendar', 'v3', credentials=creds)
        logger.info("Calendar service authenticated successfully")

        return service

    def get_events_next_48h(self) -> List[Dict]:
        """
        Fetch all events from now until 48 hours from now.
        Returns list of formatted events ready for email display.
        """

        # Calculate time range
        now = datetime.now(self.timezone)
        end_time = now + timedelta(hours=48)

        logger.info(f"Fetching events from {now} to {end_time}")

        try:
            # Call Google Calendar API
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=now.isoformat(),
                timeMax=end_time.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])
            logger.info(f"Found {len(events)} events")

            # Format events for email
            formatted_events = [self._format_event(event) for event in events]

            return formatted_events

        except Exception as e:
            logger.error(f"Error fetching calendar events: {e}")
            raise

    def _format_event(self, event: Dict) -> Dict:
        """Convert Google Calendar event to email-friendly format"""

        # Get event title
        title = event.get('summary', '(No title)')

        # Parse start/end times
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))

        # Check if all-day event
        is_all_day = 'date' in event['start']

        if is_all_day:
            # All-day event
            start_dt = datetime.fromisoformat(start)
            date_str = self._format_date(start_dt)
            time_str = "All day"
        else:
            # Timed event
            start_dt = datetime.fromisoformat(start).astimezone(self.timezone)
            end_dt = datetime.fromisoformat(end).astimezone(self.timezone)

            date_str = self._format_date(start_dt)
            time_str = f"{start_dt.strftime('%I:%M %p').lstrip('0')} - {end_dt.strftime('%I:%M %p').lstrip('0')}"

        # Get location
        location = event.get('location', '')

        # Get attendees
        attendees = event.get('attendees', [])
        attendee_names = [a.get('email', '') for a in attendees if not a.get('self', False)]

        # Get meeting link (Google Meet, Zoom, etc.)
        meeting_link = ''
        if 'conferenceData' in event:
            entry_points = event['conferenceData'].get('entryPoints', [])
            for entry in entry_points:
                if entry.get('entryPointType') == 'video':
                    meeting_link = entry.get('uri', '')
                    break

        # If no conference data, check description for links
        if not meeting_link and 'description' in event:
            description = event['description']
            if 'meet.google.com' in description or 'zoom.us' in description:
                # Extract first URL
                import re
                urls = re.findall(r'https?://[^\s<>"]+', description)
                if urls:
                    meeting_link = urls[0]

        return {
            'title': title,
            'date': date_str,
            'time': time_str,
            'location': location,
            'attendees': attendee_names,
            'meeting_link': meeting_link,
            'is_all_day': is_all_day,
            'start_datetime': start_dt if not is_all_day else datetime.fromisoformat(start)
        }

    def _format_date(self, dt: datetime) -> str:
        """Format date as 'Today', 'Tomorrow', or 'Day, Month Date'"""

        now = datetime.now(self.timezone)
        today = now.date()
        tomorrow = (now + timedelta(days=1)).date()

        event_date = dt.date()

        if event_date == today:
            return "Today"
        elif event_date == tomorrow:
            day = dt.day
            return f"Tomorrow, {dt.strftime('%B')} {day}"
        else:
            day = dt.day
            return f"{dt.strftime('%A, %B')} {day}"
