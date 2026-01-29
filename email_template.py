"""
HTML email template generator for calendar events
"""

from datetime import datetime
from typing import List, Dict

def generate_calendar_email(events: List[Dict], recipient_name: str = "Noah") -> Dict[str, str]:
    """
    Generate HTML email with appointment list.

    Args:
        events: List of formatted event dictionaries
        recipient_name: Name to use in greeting

    Returns:
        Dictionary with 'subject', 'html', and 'text' keys
    """

    # Generate subject
    event_count = len(events)
    if event_count == 0:
        subject = "Your Schedule - All Clear for the Next 48 Hours! ✨"
    elif event_count == 1:
        subject = "Your Schedule - 1 Appointment in the Next 48 Hours"
    else:
        subject = f"Your Schedule - {event_count} Appointments in the Next 48 Hours"

    # Generate HTML body
    html = _generate_html(events, recipient_name)

    # Generate plain text fallback
    text = _generate_text(events, recipient_name)

    return {
        'subject': subject,
        'html': html,
        'text': text
    }

def _generate_html(events: List[Dict], recipient_name: str) -> str:
    """Generate HTML email body"""

    # Generate event cards HTML
    if events:
        events_html = '\n'.join([_event_card_html(event) for event in events])
    else:
        events_html = '''
        <div style="background-color: #F3F4F6; padding: 30px; border-radius: 8px; text-align: center; margin: 20px 0;">
            <p style="font-size: 18px; color: #6B7280; margin: 0;">
                You're all clear for the next 2 days! ✨
            </p>
        </div>
        '''

    html = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #FFFFFF;">

        <!-- Header -->
        <div style="background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%); padding: 30px 20px; text-align: center;">
            <h1 style="color: #FFFFFF; margin: 0; font-size: 24px; font-weight: 600;">
                📅 Your Schedule - Next 48 Hours
            </h1>
        </div>

        <!-- Body -->
        <div style="padding: 30px 20px;">
            <p style="font-size: 16px; color: #374151; margin-bottom: 20px;">
                Hi {recipient_name},
            </p>

            <p style="font-size: 16px; color: #374151; margin-bottom: 30px;">
                Here's your upcoming schedule for the next 48 hours:
            </p>

            <!-- Events -->
            {events_html}
        </div>

        <!-- Footer -->
        <div style="background-color: #F9FAFB; padding: 20px; text-align: center; border-top: 1px solid #E5E7EB;">
            <p style="color: #9CA3AF; font-size: 14px; margin: 0;">
                Generated automatically at {datetime.now().strftime('%I:%M %p').lstrip('0')} on {datetime.now().strftime('%B %d, %Y')}
            </p>
            <p style="color: #9CA3AF; font-size: 14px; margin: 10px 0 0 0;">
                <strong style="color: #4F46E5;">XShift AI</strong> - Calendar Automation
            </p>
        </div>

    </div>
</body>
</html>
    '''

    return html

def _event_card_html(event: Dict) -> str:
    """Generate HTML for a single event card"""

    # Build location/link section
    location_html = ''
    if event.get('meeting_link'):
        location_html = f'''
        <p style="margin: 8px 0; color: #374151; font-size: 14px;">
            <strong style="color: #6B7280;">🔗 Join:</strong>
            <a href="{event['meeting_link']}" style="color: #4F46E5; text-decoration: none;">
                {event.get('location', 'Video call')}
            </a>
        </p>
        '''
    elif event.get('location'):
        location_html = f'''
        <p style="margin: 8px 0; color: #374151; font-size: 14px;">
            <strong style="color: #6B7280;">📍 Location:</strong> {event['location']}
        </p>
        '''

    # Build attendees section
    attendees_html = ''
    if event.get('attendees'):
        attendee_list = ', '.join(event['attendees'][:3])  # Max 3 attendees
        if len(event['attendees']) > 3:
            attendee_list += f" +{len(event['attendees']) - 3} more"

        attendees_html = f'''
        <p style="margin: 8px 0; color: #374151; font-size: 14px;">
            <strong style="color: #6B7280;">👤 With:</strong> {attendee_list}
        </p>
        '''

    card = f'''
    <div style="background-color: #FFFFFF; padding: 20px; border-radius: 8px; margin: 15px 0;
                border-left: 4px solid #4F46E5; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
        <h3 style="margin: 0 0 12px 0; color: #111827; font-size: 18px; font-weight: 600;">
            {event['title']}
        </h3>

        <p style="margin: 8px 0; color: #374151; font-size: 14px;">
            <strong style="color: #6B7280;">📅 Date:</strong> {event['date']}
        </p>

        <p style="margin: 8px 0; color: #374151; font-size: 14px;">
            <strong style="color: #6B7280;">🕐 Time:</strong> {event['time']}
        </p>

        {location_html}
        {attendees_html}
    </div>
    '''

    return card

def _generate_text(events: List[Dict], recipient_name: str) -> str:
    """Generate plain text email fallback"""

    text = f'''Your Schedule - Next 48 Hours
{'=' * 50}

Hi {recipient_name},

Here's your upcoming schedule for the next 48 hours:

'''

    if events:
        for event in events:
            text += f'''
{event['date']}
[{event['time']}] {event['title']}
'''
            if event.get('location'):
                text += f"Location: {event['location']}\n"
            if event.get('meeting_link'):
                text += f"Join: {event['meeting_link']}\n"
            if event.get('attendees'):
                text += f"With: {', '.join(event['attendees'][:3])}\n"

            text += '-' * 50 + '\n'
    else:
        text += "You're all clear for the next 2 days! ✨\n"

    text += f'''
{'=' * 50}
Generated at {datetime.now().strftime('%I:%M %p').lstrip('0')} on {datetime.now().strftime('%B %d, %Y')}
XShift AI - Calendar Automation
'''

    return text
