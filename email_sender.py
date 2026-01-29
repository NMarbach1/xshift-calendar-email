"""
Email sender using Gmail SMTP with retry logic
"""

import logging
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

class EmailSender:
    """Gmail SMTP email sender with retry logic"""

    def __init__(self, smtp_user: str, smtp_password: str):
        """Initialize with Gmail credentials"""
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def send_email(self, to_email: str, subject: str, html_body: str, text_body: str = None) -> bool:
        """
        Send email with retry logic (3 attempts with exponential backoff)

        Args:
            to_email: Recipient email address
            subject: Email subject line
            html_body: HTML email body
            text_body: Plain text fallback (optional)

        Returns:
            True if sent successfully, False otherwise
        """

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f'"XShift Calendar" <{self.smtp_user}>'
        msg['To'] = to_email

        # Add text and HTML parts
        if text_body:
            part1 = MIMEText(text_body, 'plain')
            msg.attach(part1)

        part2 = MIMEText(html_body, 'html')
        msg.attach(part2)

        # Retry logic
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                logger.info(f"Sending email to {to_email} (attempt {attempt + 1}/{max_attempts})")

                # Connect to SMTP server
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()  # Enable TLS encryption
                    server.login(self.smtp_user, self.smtp_password)
                    server.send_message(msg)

                logger.info(f"Email sent successfully to {to_email}")
                return True

            except smtplib.SMTPAuthenticationError as e:
                logger.error(f"Authentication failed: {e}")
                logger.error("Check SMTP_USER and SMTP_PASSWORD in .env")
                return False  # Don't retry auth errors

            except smtplib.SMTPException as e:
                logger.warning(f"SMTP error on attempt {attempt + 1}: {e}")

                if attempt < max_attempts - 1:
                    # Exponential backoff: 1s, 2s, 4s
                    delay = 2 ** attempt
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"Failed to send email after {max_attempts} attempts")
                    return False

            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return False

        return False
