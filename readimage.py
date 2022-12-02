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


def gcal(datedict):
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
    for idx, disd in enumerate(datedict['dis']):
        event = {
        'summary': 'discusstion'+str(idx+1),
            'start': {'dateTime': disd+'T13:00:00','timeZone': 'America/Los_Angeles',},
            'end': {'dateTime': disd+'T14:00:00','timeZone': 'America/Los_Angeles'},
        }
        e = service.events().insert(calendarId='primary', body=event).execute()
    for idx, quizd in enumerate(datedict['quiz']):
        event = {
        'summary': 'quiz'+str(idx+1),
            'start': {'dateTime': quizd+'T13:00:00','timeZone': 'America/Los_Angeles',},
            'end': {'dateTime': quizd+'T14:00:00','timeZone': 'America/Los_Angeles'},
        }
        e = service.events().insert(calendarId='primary', body=event).execute() 
    print ('Here is the link:'+(e.get('htmlLink')))               

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
discussion = []
quiz = []

monthdict = {
    'January'   :'01', 
    'Februay'   :'02', 
    'March'     :'03', 
    'April'     :'04', 
    'May'       :'05',
    'June'      :'06', 
    'July'      :'07', 
    'August'    :'08', 
    'September' :'09', 
    'October'   :'10', 
    'November'  :'11',
    'December'  :'12'}

for line in textlist:
    x = re.findall(r"(?:January|Februay|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}", line)
    if len(x) == 3:
        disdatelist = x[1].split()
        if (len(disdatelist[1].replace(',','')) == 1):
            dated = '0'+disdatelist[1].replace(',','')
        else: dated = disdatelist[1].replace(',','')
        newdisdate = disdatelist[2]+'-'+monthdict[disdatelist[0]]+'-'+dated
        discussion.append(newdisdate)

        quizdatelist = x[2].split()
        if (len(quizdatelist[1].replace(',','')) == 1):
            dated = '0'+quizdatelist[1].replace(',','')
        else: dated = quizdatelist[1].replace(',','')
        newquizdate = quizdatelist[2]+'-'+monthdict[quizdatelist[0]]+'-'+dated
        quiz.append(newquizdate)

dissquizdict = {'dis':discussion, 'quiz':quiz}

#STEP 3: make google calendar - use append (ref: https://developers.google.com/calendar/api/guides/create-events#python)
gcal(dissquizdict)
