import os.path
import base64
import time
from ast import literal_eval

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SERVICE = None
THRESHOLD = 5
PREV_LIST = set()
NEW_LIST = set()
INTERVAL = 10
RUNNING = False
WINDOW = False
LOCATION = "./"
LISTBOX = None
# NUM_OF_DOWNLOADS= 0

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def reset():
    print("IN reset")
    if os.path.exists("./logs.txt"):
        os.remove("./logs.txt")

def get_message_list():
    print("IN get_message_list")
    return SERVICE.users().messages().list(userId='me', maxResults=THRESHOLD, q='category:primary').execute()

def get_message(mail_id):
    print("IN get_message")
    return SERVICE.users().messages().get(userId='me', id=mail_id).execute()

def start():
    print("IN start")
    global SERVICE, RUNNING, WINDOW

    if(not RUNNING and not WINDOW):

        RUNNING = True
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials
            with open('token.json', 'w') as token:
                token.write(creds.to_json())    

        try:
            if SERVICE == None:
                SERVICE = build('gmail', 'v1', credentials=creds)
            while True:
                if RUNNING:
                    try:
                        exec_service()
                    except Exception:
                        print('Error Occured')
                    time.sleep(INTERVAL)
                else:
                    if not WINDOW:
                        exit()
                    time.sleep(2)
            
        except HttpError as error:
            print(f'An error occurred: {error}')


def set_type_of_user(type):
    global INTERVAL, THRESHOLD

    if(type == 'Very Frequent'):
        INTERVAL=5
        THRESHOLD = 15
    elif(type == 'Less Frequent'):
        INTERVAL=20
        THRESHOLD = 5
    else:
        INTERVAL=10
        THRESHOLD = 5


def exec_service():
    print("IN EXEC")
    global PREV_LIST
    try:
        with open('logs.txt', 'r') as f:
            file_content_str = f.read()
            if(file_content_str.strip() != ""):
                PREV_LIST = literal_eval(file_content_str)
    except Exception:
        if os.path.exists("./logs.txt"):
            os.remove("./logs.txt")
        #CREATE THE LOGS FILE IF NOT EXISTS
        with open('logs.txt', 'w+') as f:
            pass

    msg_list = get_message_list()
    fetch_download(msg_list)


def stop():
    print("IN stop")
    global RUNNING, PREV_LIST, NEW_LIST
    PREV_LIST = set()
    NEW_LIST = set()
    RUNNING = False
    WINDOW = False

def exitout():
    global WINDOW
    WINDOW = False

def update_list_box(item):
    global LISTBOX
    if LISTBOX != None:
        LISTBOX.insert("end",item)

def reset_listbox():
    global LISTBOX
    if LISTBOX != None:
        LISTBOX.delete(0, "end")


def setLocation(l):
    global LOCATION
    LOCATION = l

def fetch_download(msg_list):
    print("IN fetch_download")
    global SERVICE, NEW_LIST, PREV_LIST

    for mail_dict in msg_list['messages']:
        NEW_LIST.add(mail_dict['id'])

    mails_to_process = NEW_LIST - PREV_LIST 


    for each_mail_id in mails_to_process:
        results = get_message(each_mail_id)
        process_payloads(results, each_mail_id)


    to_write = str(PREV_LIST.union(mails_to_process))
    #save new list in a log.txt file
    with open('logs.txt', 'w') as f:
        f.write(to_write)

    NEW_LIST = set()

def process_payloads(results, msg_id):
    print("IN process_payloads")
    payl = results['payload']
    if 'parts' in payl:
        for partPayl in payl['parts']:
            file_name = partPayl['filename']
            body = partPayl['body']
            if 'attachmentId' in body:
                attachment_id = body['attachmentId']
                attachment = get_attachment(msg_id, attachment_id)
                download_file(msg_id, attachment_id, attachment, file_name)

def get_attachment(msg_id, attachment_id):
    print("IN get_attachment")
    return SERVICE.users().messages().attachments().get(userId='me', messageId=msg_id, id=attachment_id).execute()

def download_file(msg_id, attachment_id, attachment, file_name):
    print("IN download_file")

    global LOCATION
    file_data = base64.urlsafe_b64decode(attachment.get('data').encode('UTF-8'))
    if(not os.path.exists(LOCATION)):
        LOCATION = '/Downloads/'
    with open(os.path.join(LOCATION, file_name), 'wb') as f:
        f.write(file_data)
        print(f"Saved : {file_name}")
        update_list_box(file_name)


# if __name__ == '__main__':
    # start()