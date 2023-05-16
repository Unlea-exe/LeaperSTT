import speech_recognition as sr
import keyboard
import time
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

r = sr.Recognizer()

credentials_file = r'C:\Users\Unlea\Documents\V.S.C. Projects\Json files\transfer_file.json'

google_docs_file_id = '1kGpyoMgChhfhgLSsDO7chHni1L0VcCOo69rkVK9XYmY'

scope = ['https://www.googleapis.com/auth/drive']

def speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")

        r.adjust_for_ambient_noise(source)

        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
    except sr.RequestError as e:
        print("Sorry, an error occurred during speech recognition:", str(e))

def save_to_google_docs(text):
    credentials = Credentials.from_service_account_file(credentials_file, scopes=scope)
    service = build('docs', 'v1', credentials=credentials)

    # Retrieve the current content of the Google Docs file
    result = service.documents().get(documentId=google_docs_file_id).execute()
    current_content = result['body']['content']

    # Delete the existing content
    delete_requests = [
        {
            'deleteContentRange': {
                'range': {
                    'startIndex': 1,
                    'endIndex': len(current_content),
                }
            }
        }
    ]

    # Insert the new text at the beginning
    insert_requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': text
            }
        }
    ]

    # Execute the batch update request
    requests = delete_requests + insert_requests
    service.documents().batchUpdate(documentId=google_docs_file_id, body={'requests': requests}).execute()

    print("Recorded speech saved to Google Docs")

recording_duration = 5

keyboard.wait('enter')

result = speech_to_text()
if result:
    print("You said:", result)
    save_to_google_docs(result)
