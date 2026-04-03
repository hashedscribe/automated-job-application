import os, sys
import base64
import re
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# get the search profile from config
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config'))
from search_config import *


CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')
TOKEN_PATH = os.path.join(CONFIG_DIR, 'gmail_token.json')

def get_gmail_service():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    return build('gmail', 'v1', credentials=creds)

def fetch_job_emails():
    service = get_gmail_service()
    sender_filter = ' OR '.join(f'from:{s}' for s in SENDERS)
    
    results = service.users().messages().list(
        userId='me',
        q=f'({sender_filter})'.join(GMAIL_ADDITIONAL_FILTERS)
    ).execute()

    messages = results.get('messages', [])
    print(f"Found {len(messages)} unread job alert emails")
    return messages

def get_email_body(service, msg_id):
    msg = service.users().messages().get(
        userId='me', id=msg_id, format='full'
    ).execute()
    
    parts = msg['payload'].get('parts', [])
    for part in parts:
        if part['mimeType'] == 'text/html':
            data = part['body']['data']
            return base64.urlsafe_b64decode(data).decode('utf-8')
    return ''

def make_linkedin_listing(url, text):
    # TODO adjust making the listing ? or we get the info and then make it in 
    # the other function
    linkedin = r'https?://www\.linkedin\.com[^\s"<>]*/[\d]+/'
    linkedin_match = re.match(linkedin, url)
    
    sanitized_url = ""
    if linkedin_match:
        sanitized_url = linkedin_match.group().replace("/comm", "")
        
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    
    return (sanitized_url, clean_text)

def handle_indeed(url, text):
    indeed = r'https?://www\.indeed\.com[^\s"<>]*'
    indeed_match = re.match(indeed, url)
    
    sanitized_url = ""
    if indeed:
        sanitized_url = indeed_match.group()
        
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    
    return (sanitized_url, clean_text)
    

def extract_job_links(html):
    # TODO make this a dict with properties of job
    seen = set()
    
    # pulls all job URLs out of the email body
    pattern = r'<a[^>]+href=["\']?(https?://[^\s"<>]*jobs[^\s"<>]*)["\']?[^>]*>(.*?)</a>'
    matches = re.findall(pattern, html, re.DOTALL)
    
    for url, text in matches:
        if "linkedin" in url:
            sanitized_url, clean_text = handle_linkedin(url, text)
        elif "indeed" in url:
            sanitized_url, clean_text = handle_indeed(url, text)
            
        # TODO build th
        # return list(set(urls)) 
        if sanitized_url in seen:
            continue
        else:
            seen.add(sanitized_url)

if __name__ == "__main__":
    service = get_gmail_service()
    messages = fetch_job_emails(date_range=5)
    
    max_search = 100
    found = 0
    
    all_links = []
    for msg in messages:
        body = get_email_body(service, msg['id'])
        # print(body)
        found += 1
        links = extract_job_links(body)
        if(found == max_search):
            break
        # all_links.extend(links)