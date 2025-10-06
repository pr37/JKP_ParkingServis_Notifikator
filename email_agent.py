import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os.path
import pickle
import csv

# To make any of this work, you need to know how to set up a project
# on Google Cloud and enable Gmail API for sending emails. You will also need credentials.json
# from the Google OAuth to be able to use the API.
# Don't even try to set up your own SMTP server, unless you are willing to beg
# your ISP to unblock port 25.

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email(service, user_id, message):
    sent_message = service.users().messages().send(userId=user_id, body=message).execute()
    print(f"Message ID: {sent_message['id']}")
    return sent_message

def send_emails_from_csv(service, sender_email, csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipient = row['email']
            subject = "Parking ticket status for: " + row['plate_num']
            
            message = create_message(sender_email, recipient, subject, row['message'])
            send_email(service, 'me', message)

if __name__ == '__main__':
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    
    sender = "email-from-which-you-send-notifications-from@gmail.com"  
    csv_path = 'scraped_results.csv'      

    send_emails_from_csv(service, sender, csv_path)
    
    #message = create_message(sender, to, subject, body)
    #send_email(service, 'me', message)
