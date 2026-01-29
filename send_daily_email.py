#!/usr/bin/env python
"""
Daily Calendar Email Script

Sends list of appointments from contact@xshift.ai calendar
for the next 48 hours to nmarbach@gmail.com

Designed to run daily at 9:00 AM via Windows Task Scheduler
"""

import logging
import sys
from datetime import datetime

def setup_logging():
    """Configure logging to file and console"""
    from pathlib import Path
    from config import Config

    config = Config()
    config.LOG_DIR.mkdir(exist_ok=True)

    # Configure logging
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)

def main():
    """Main execution flow"""

    logger = setup_logging()

    try:
        logger.info("=" * 60)
        logger.info("Starting daily calendar email job")
        logger.info(f"Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)

        # 1. Load and validate configuration
        from config import Config
        config = Config()
        config.validate()
        logger.info(f"Configuration loaded - Recipient: {config.RECIPIENT_EMAIL}")

        # 2. Initialize calendar client
        from calendar_client import CalendarClient
        logger.info(f"Initializing calendar client for calendar: {config.CALENDAR_ID}")
        calendar = CalendarClient(
            credentials_path=config.GOOGLE_CREDENTIALS,
            token_path=config.GOOGLE_TOKEN,
            calendar_id=config.CALENDAR_ID,
            timezone=config.TIMEZONE
        )

        # 3. Fetch events for next 48 hours
        logger.info("Fetching calendar events for next 48 hours...")
        events = calendar.get_events_next_48h()
        logger.info(f"Found {len(events)} event(s)")

        # Log event details
        for i, event in enumerate(events, 1):
            logger.info(f"  {i}. {event['title']} - {event['date']} at {event['time']}")

        # 4. Generate email HTML
        from email_template import generate_calendar_email
        logger.info("Generating email content...")
        email_content = generate_calendar_email(
            events=events,
            recipient_name="Noah"
        )
        logger.info(f"Email subject: {email_content['subject']}")

        # 5. Send email
        from email_sender import EmailSender
        logger.info("Sending email...")
        sender = EmailSender(
            smtp_user=config.SMTP_USER,
            smtp_password=config.SMTP_PASSWORD
        )

        success = sender.send_email(
            to_email=config.RECIPIENT_EMAIL,
            subject=email_content['subject'],
            html_body=email_content['html'],
            text_body=email_content['text']
        )

        if success:
            logger.info("=" * 60)
            logger.info("Daily calendar email job completed successfully")
            logger.info("=" * 60)
            sys.exit(0)
        else:
            logger.error("=" * 60)
            logger.error("Failed to send email")
            logger.error("=" * 60)
            sys.exit(1)

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        logger.error("Have you run setup_auth.py yet?")
        sys.exit(2)

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Check your .env file")
        sys.exit(3)

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(4)

if __name__ == "__main__":
    main()
