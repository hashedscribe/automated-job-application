from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')

flow = InstalledAppFlow.from_client_secrets_file(
    os.path.join(CONFIG_DIR, 'credentials.json'), SCOPES
)

creds = flow.run_local_server(port=0)

with open(os.path.join(CONFIG_DIR, 'gmail_token.json'), 'w') as f:
    f.write(creds.to_json())

print("Token saved")