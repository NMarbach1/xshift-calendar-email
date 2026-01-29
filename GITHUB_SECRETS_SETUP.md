# GitHub Secrets Setup

After pushing this repository to GitHub, you need to add the following secrets for GitHub Actions to work.

## How to Add Secrets

1. Go to your GitHub repository
2. Click "Settings" tab
3. In the left sidebar, click "Secrets and variables" → "Actions"
4. Click "New repository secret" for each secret below

## Required Secrets

### 1. SMTP_USER
- **Value:** `contact@xshift.ai`
- **Description:** Email address to send from

### 2. SMTP_PASSWORD
- **Value:** Your Gmail app password (format: `kjqz alle kowv yzku`)
- **Description:** Gmail app password for contact@xshift.ai

### 3. RECIPIENT_EMAIL
- **Value:** `nmarbach@gmail.com`
- **Description:** Email address to receive the daily calendar digest

### 4. CALENDAR_ID
- **Value:** `primary`
- **Description:** Google Calendar ID to fetch events from

### 5. GOOGLE_CREDENTIALS
- **Value:** Contents of `credentials/credentials.json` file
- **Description:** Google OAuth client credentials
- **How to get:** Copy the entire contents of your local `credentials/credentials.json` file

### 6. GOOGLE_TOKEN
- **Value:** Contents of `credentials/token_contact_xshift.json` file
- **Description:** OAuth access token for contact@xshift.ai calendar
- **How to get:** Copy the entire contents of your local `credentials/token_contact_xshift.json` file

## Testing the Workflow

After adding all secrets:

1. Go to "Actions" tab in your repository
2. Click "Daily Calendar Email" workflow
3. Click "Run workflow" → "Run workflow" button
4. Check the logs to verify it works
5. Check your email at nmarbach@gmail.com

## Scheduled Execution

The workflow is scheduled to run automatically every day at:
- **9:00 AM Eastern Time**
- Cron expression: `0 14 * * *` (14:00 UTC = 9:00 AM EST)

## Troubleshooting

If the workflow fails:
1. Check the "Actions" tab for error logs
2. Verify all 6 secrets are set correctly
3. Make sure the JSON secrets (GOOGLE_CREDENTIALS, GOOGLE_TOKEN) are valid JSON format
4. Test locally first with `python send_daily_email.py`
