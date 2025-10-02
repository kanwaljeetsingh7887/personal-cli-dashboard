import os, pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_creds(credentials_path='credentials.json', token_path='token.json'):
    creds = None
    if os.path.exists(token_path):
        with open(token_path, 'rb') as t:
            creds = pickle.load(t)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as t:
            pickle.dump(creds, t)
    return creds

def get_next_event(creds, max_results=1):
    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=max_results, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            return None
        e = events[0]
        start = e['start'].get('dateTime', e['start'].get('date'))
        return {
            'summary': e.get('summary', 'No title'),
            'start': start,
            'link': e.get('htmlLink')
        }
    except Exception:
        return None
