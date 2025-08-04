import os
import sys

# Set base path for project
base_path = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(os.path.join(base_path, "src"))

import base64
from email import message_from_bytes, utils
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from agents.draft_agent.draft_agent import generate_response

# Gmail scopes
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
]

def get_gmail_service():
    creds = None
    creds_path = os.path.expanduser('credentials.json')
    token_path = os.path.join(os.path.dirname(__file__), 'token.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_unread_emails():
    service = get_gmail_service()
    result = service.users().messages().list(
        userId='me',
        labelIds=['INBOX'],
        q="is:unread category:primary"
    ).execute()

    messages = result.get('messages', [])
    if not messages:
        print("No unread emails found.")
        return

    for msg in messages:
        msg_id = msg['id']
        msg_data = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
        raw_msg = base64.urlsafe_b64decode(msg_data['raw'].encode("ASCII"))
        email_msg = message_from_bytes(raw_msg)

        subject = email_msg.get('Subject', '(No Subject)')
        sender = email_msg.get('From')
        thread_id = msg_data.get('threadId')

        # Extract plain text part of email body
        body = None
        for part in email_msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                break

        if not body:
            print(f"Skipping email from {sender} — no plain text body.")
            continue

        email_data = {
            "subject": subject,
            "body": body,
            "sender": sender,
        }

        # Generate a reply using the draft agent
        reply_text = generate_response(email_data)

        # Create draft reply in Gmail
        create_draft_reply(service, thread_id, sender, subject, reply_text)
        print(f"✅ Draft created for: {subject}")

def create_draft_reply(service, thread_id, to_email, subject, reply_text):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart()
    msg['To'] = to_email
    msg['Subject'] = f"Re: {subject}"
    msg['In-Reply-To'] = thread_id
    msg['References'] = thread_id
    msg['Date'] = utils.formatdate(localtime=True)

    msg.attach(MIMEText(reply_text, 'plain'))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    draft_body = {
        'message': {
            'raw': raw,
            'threadId': thread_id
        }
    }

    service.users().drafts().create(userId='me', body=draft_body).execute()

if __name__ == '__main__':
    get_unread_emails()