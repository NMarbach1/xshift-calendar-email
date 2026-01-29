#!/usr/bin/env python
"""
One-time OAuth setup for contact@xshift.ai calendar access
Run this once to authorize the application
"""

import os
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from config import Config

def setup_calendar_auth():
    """Run OAuth flow to get calendar access"""

    config = Config()

    print("=" * 60)
    print("Google Calendar OAuth Setup")
    print("=" * 60)
    print(f"\nCalendar ID: {config.CALENDAR_ID}")
    print(f"Credentials file: {config.GOOGLE_CREDENTIALS}")
    print(f"Token will be saved to: {config.GOOGLE_TOKEN}")
    print("\n** IMPORTANT: When the browser opens, sign in as contact@xshift.ai")
    print("=" * 60)

    if not config.GOOGLE_CREDENTIALS.exists():
        print(f"\n** ERROR: Credentials file not found at {config.GOOGLE_CREDENTIALS}")
        print("Please copy your credentials.json file to the credentials/ folder")
        return False

    # Check if token already exists
    if config.GOOGLE_TOKEN.exists():
        response = input(f"\n** Token already exists at {config.GOOGLE_TOKEN}. Recreate? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return False

    try:
        # Run OAuth flow
        print("\n** Starting OAuth flow...")
        flow = InstalledAppFlow.from_client_secrets_file(
            str(config.GOOGLE_CREDENTIALS),
            config.SCOPES
        )

        creds = flow.run_local_server(port=0)

        # Save credentials
        with open(config.GOOGLE_TOKEN, 'w') as token:
            token.write(creds.to_json())

        print(f"\n** Success! Token saved to {config.GOOGLE_TOKEN}")
        print("You can now run send_daily_email.py")
        return True

    except Exception as e:
        print(f"\n** Error during OAuth: {e}")
        return False

if __name__ == "__main__":
    setup_calendar_auth()
