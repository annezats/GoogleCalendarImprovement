from __future__ import print_function
import datetime #dont rlly need it
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/calendar.events','https://www.googleapis.com/auth/calendar.addons.execute']

def setup():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_day_info(timezone_offset):
    print('enter the day you want to clear in DDMMYYYY format: ')
    day= raw_input() #returns string
    date=day[4:8]+"-"+day[2:4]+"-"+day[0:2]
    startofday= date+"T00:00:00"+timezone_offset
    endofday=date+"T23:59:59"+timezone_offset
    dayinfo= [startofday, endofday]
    return dayinfo

def get_cal_IDs(cal, allowedcalendars):
    allowedcalIDs=[]
    callist=cal.calendarList().list().execute() #gets list of all calendars
    calendars=callist.get('items', [])
    for calendar in calendars: #compares list of all cals to list of allowed cals
        for ac in allowedcalendars:
            if calendar['summary']== ac:
                allowedcalIDs.append(calendar['id']) #sticks the calID into a list
    return allowedcalIDs

def main():
    creds= setup()
    cal = build('calendar', 'v3', credentials=creds)
    calendarID= "primary";
    timezone_offset="-04:00"#cal.settings.get(timezone).execute()

    allowedcalendars=['anne.zats@macaulay.cuny.edu','Classes']
    allowedcalIDs=get_cal_IDs(cal, allowedcalendars)

    dayinfo=get_day_info(timezone_offset)
    print(dayinfo)

    for calendarID in allowedcalIDs:
        mylist=cal.events().list(calendarId=calendarID,
        timeMax=dayinfo[1], timeMin=dayinfo[0], singleEvents=True,
        orderBy='startTime').execute()
        events = mylist.get('items', [])
        for event in events:
            print(event['summary'])
            cal.events().delete(calendarId=calendarID, eventId=event['id']).execute()


if __name__ == "__main__":
    main()
