import os.path
import os


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build

from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from openai import OpenAI

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

receiver_email = os.environ.get("RECEIVER_EMAIL")
sender_email = os.environ.get("SENDER_EMAIL")

# I don't need to add the other environment variables because I already defined them... ?

llm = ChatOpenAI(
    model="gpt-4o-mini-search-preview",
    max_tokens=None,
    timeout=None,
    max_retries=2
)

query_strings = {'Additive Manufacturing': """Find all open positions for additive manufacturing internships in the USA.
                    List up to ten internships, no duplicate postings.""",
                    
                'Vehicle Dynamics': """Find all open positions for vehicle dynamics internships in the USA.
                    List up to ten internships, no duplicate postings.""",
                    
                'Mountain Biking': """Find all open positions for engineering internships in the mountain bike industry in the USA.
                    List up to fifteen internships, no duplicate postings.""",
                    
                'Motorsport': """Find all open positions for race car or motorsport engineering internships in the USA.
                    List up to fifteen internships, no duplicate postings.""",
                    
                'Pittsburgh': """Find all open positions for engineering internships near Pittsburgh, PA.
                    List up to fifteen internships, no duplicate postings."""}

def get_llm_results():
    total_result = ""
    for subject, query_string in query_strings.items():
        messages = [
            (
                "system",
                "You are a helpful assistant that finds job and internship opportunities. Retrieve job and internship listings.",
            ),
            ("human", query_string),
        ]

        ai_msg = llm.invoke(messages)

        total_result = total_result + "\n" + ai_msg.content

    return total_result



def send_email(string_to_send):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message.set_content(string_to_send)

        message["To"] = os.environ.get("RECEIVER_EMAIL")
        message["From"] = os.environ.get("SENDER_EMAIL")
        message["Subject"] = "Daily Internship Listings from Job Alert Agent"
 
        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None

    return send_message

if __name__ == "__main__":
    string_to_send = get_llm_results()
    send_email(string_to_send)