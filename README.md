# Daily Calendar Email

Automated daily email system that sends a list of upcoming appointments from contact@xshift.ai calendar to nmarbach@gmail.com.

## Features

- Fetches events from Google Calendar for the next 48 hours
- Sends beautifully formatted HTML email at 9:00 AM daily
- Runs automatically via Windows Task Scheduler
- Full error handling and logging
- OAuth 2.0 authentication with automatic token refresh

## Setup

### 1. Install Dependencies

```bash
cd C:\Users\nmarb\daily-calendar-email
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Copy Google Credentials

Copy your `credentials.json` file to the `credentials/` folder:

```bash
copy C:\Users\nmarb\credentials.json credentials\
```

### 3. Configure Environment

The `.env` file is already configured with:
- SMTP_USER: contact@xshift.ai
- SMTP_PASSWORD: (your app password)
- RECIPIENT_EMAIL: nmarbach@gmail.com

### 4. Authorize Calendar Access (ONE-TIME)

Run the OAuth setup script:

```bash
python setup_auth.py
```

**IMPORTANT:** When the browser opens, sign in as **contact@xshift.ai** (not your personal Gmail).

This will create `credentials/token_contact_xshift.json` which allows unattended access.

### 5. Test Manually

Run the script manually to verify it works:

```bash
python send_daily_email.py
```

Check:
- Email arrives at nmarbach@gmail.com
- Log file created in `logs/daily_calendar_email.log`

### 6. Schedule Daily Execution

**Windows Task Scheduler Setup:**

1. Open Task Scheduler (Win + R → `taskschd.msc`)
2. Create Task (not Basic Task)
3. Configure:

**General Tab:**
- Name: `Daily Calendar Email`
- Run whether user is logged on or not: ✓
- Run with highest privileges: ✓

**Triggers Tab:**
- New Trigger → Daily at 9:00 AM
- Synchronize across time zones: ✓

**Actions Tab:**
- Program: `C:\Users\nmarb\daily-calendar-email\venv\Scripts\python.exe`
- Arguments: `send_daily_email.py`
- Start in: `C:\Users\nmarb\daily-calendar-email`

**Conditions Tab:**
- Wake computer to run: ✓
- Start only if on AC power: ✗

**Settings Tab:**
- Allow run on demand: ✓
- If fails, restart every 15 minutes (3 attempts)

4. Test: Right-click task → Run

## Usage

Once scheduled, the system runs automatically every day at 9:00 AM.

### Manual Execution

```bash
cd C:\Users\nmarb\daily-calendar-email
venv\Scripts\activate
python send_daily_email.py
```

### View Logs

```bash
type logs\daily_calendar_email.log
```

### Re-authorize Calendar

If you need to re-authorize (e.g., token revoked):

```bash
python setup_auth.py
```

## Troubleshooting

### Email not received

1. Check Task Scheduler ran successfully
2. Review logs: `logs\daily_calendar_email.log`
3. Test manually: `python send_daily_email.py`

### Authentication failed

```bash
python setup_auth.py
```

Make sure to sign in as **contact@xshift.ai** when the browser opens.

### Wrong calendar

Verify you signed in as contact@xshift.ai during setup. Delete `credentials/token_contact_xshift.json` and re-run `setup_auth.py`.

## File Structure

```
daily-calendar-email/
├── send_daily_email.py          # Main entry point
├── calendar_client.py           # Google Calendar API client
├── email_sender.py              # SMTP email sender
├── email_template.py            # HTML email generator
├── config.py                    # Configuration management
├── setup_auth.py                # One-time OAuth setup
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── README.md                    # This file
├── logs/                        # Log files
│   └── daily_calendar_email.log
└── credentials/                 # OAuth credentials
    ├── credentials.json         # Google OAuth client
    └── token_contact_xshift.json # Access token
```

## Security

- `.env` contains sensitive credentials (gitignored)
- OAuth tokens are encrypted by Google libraries
- Calendar access is read-only
- SMTP uses app password (not account password)
- Logs never contain passwords or tokens

## Maintenance

**Daily:** Email arrives at 9:00 AM automatically

**Weekly:** Check logs for any errors

**Monthly:** Update dependencies:
```bash
pip install --upgrade -r requirements.txt
```
