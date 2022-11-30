# libraries for enabling google calendar
from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Permissions for google api: if modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def gcal():
    """Shows basic usage of the Google Calendar API. Write one schedule"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    #generate event part
    service = build('calendar', 'v3', credentials=creds)
    event = {
    'summary': 'test',
    'location': 'online',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
        'dateTime': '2022-12-15T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': '2022-12-15T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
    },
    'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
    ],
    # 'attendees': [
    #     {'email': 'lpage@example.com'},
    #     {'email': 'sbrin@example.com'},
    # ],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created:'+(event.get('htmlLink')))

#STEP 1: recognized image, and extract all strings from it
from PIL import Image
from pytesseract import pytesseract
import os
from dotenv import load_dotenv
import re

#Access .env file, which contains TESSERACTPATH, IMAGENAME
load_dotenv()

#Define path to tessaract.exe
path_to_tesseract = os.getenv('TESSERACTPATH')
#Define path to image
path_to_image = os.getenv('IMAGENAME')
#Point tessaract_cmd to tessaract.exe
pytesseract.tesseract_cmd = path_to_tesseract
#Open image with PIL
img = Image.open(path_to_image)
#Extract text from image
text = pytesseract.image_to_string(img)
print(text)
textlist = text.split('\n')

#STEP 2: Analyze all extracted strings, and make a time list for QUIZ/ASSIGNMENT/...
for line in textlist:
    x = re.findall(r"(?:January|Febeburay|March|April|May|Jun|July|August|September|October|November|December)\s\d{1,2},\s\d{4}", line)
    print(x)

#STEP 3: make google calendar (ref: https://developers.google.com/calendar/api/guides/create-events#python)
gcal()
