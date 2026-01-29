#!/usr/bin/env python
"""
Helper script to list all accessible calendars
Run this to find the calendar ID for contact@xshift.ai
"""

from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def list_calendars():
    """List all calendars accessible to the authenticated user"""

    credentials_path = Path(__file__).parent / 'credentials' / 'credentials.json'
    token_path = Path(__file__).parent / 'credentials' / 'token_nmarbach.json'
    scopes = ['https://www.googleapis.com/auth/calendar.readonly']

    creds = None

    # Load existing token
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), scopes)

    # Get new credentials if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing credentials...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow...")
            print("Sign in as nmarbach@gmail.com when browser opens")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), scopes
            )
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        print(f"Token saved to {token_path}\n")

    # Build calendar service
    service = build('calendar', 'v3', credentials=creds)

    print("=" * 70)
    print("Listing all accessible calendars:")
    print("=" * 70)

    # Get calendar list
    calendar_list = service.calendarList().list().execute()

    for calendar in calendar_list.get('items', []):
        calendar_id = calendar['id']
        summary = calendar.get('summary', '(No name)')
        access_role = calendar.get('accessRole', 'unknown')
        primary = ' [PRIMARY]' if calendar.get('primary', False) else ''

        print(f"\nCalendar: {summary}{primary}")
        print(f"  ID: {calendar_id}")
        print(f"  Access: {access_role}")

        # Highlight if it's the xshift calendar
        if 'xshift' in calendar_id.lower() or 'xshift' in summary.lower():
            print("  >>> THIS IS THE XSHIFT CALENDAR <<<")

    print("\n" + "=" * 70)
    print("Copy the calendar ID for contact@xshift.ai and update .env file")
    print("Add this line to .env:")
    print("CALENDAR_ID=<paste the ID here>")
    print("=" * 70)

if __name__ == "__main__":
    list_calendars()
