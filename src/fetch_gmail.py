import os, sys
import base64
import re
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from job_class import JobListing
from gmail_services.linkedin_handler import make_linkedin_listings

# get the search profile from config
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config'))
from search_config import *


CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')
TOKEN_PATH = os.path.join(CONFIG_DIR, 'gmail_token.json')

def get_gmail_service():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    return build('gmail', 'v1', credentials=creds)

def fetch_job_emails(senders, additional_filters=""):
    service = get_gmail_service()
    # get the filter for the senders
    sender_filter = ' OR '.join(f'from:{s}' for s in senders)
    
    # filter for the given senders and any additional filters
    results = service.users().messages().list(
        userId='me',
        q=f'({sender_filter})'.join(additional_filters)
    ).execute()

    messages = results.get('messages', [])
    # TODO do we need the print ? i feel like when bash scripting 
    # I'll care more about it
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


def handle_indeed(url, text):
    indeed = r'https?://www\.indeed\.com[^\s"<>]*'
    indeed_match = re.match(indeed, url)
    
    sanitized_url = ""
    if indeed:
        sanitized_url = indeed_match.group()
        
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    
    return (sanitized_url, clean_text)
    
    
def get_gmail_results(query_pkt):
    service = get_gmail_service()
    messages = fetch_job_emails(query_pkt["senders"],
                                additional_filters=query_pkt["gmail_additional_filters"])

    listings_info = []
    for msg in messages:
        html = get_email_body(service, msg['id'])
        if "linkedin" in html:
            listings_info += make_linkedin_listings(html)
        elif "indeed" in html:
            print("indeed handler not implemented")
            continue
            # listings_info += make_indeed_listings(html)
    
    
    # for all the info found per listing off linkedin/indeed/other places
    listings = []
    for res in listings_info:
        if res != None:
            (title, company, salary, location, delivery, schedule, list_date,
                link, notes) = res
        else:
            return None
        
        listing = JobListing(title, company)
        # if we already seen this listing, update the information
        # otherwise, add the relevant information and then append
        # TODO can we clean this up any more? cheeck logics but its fine if not
        if listing in listings:
            i = listings.getindex(listing)
            listings[i].update(
                salary = salary,
                location = location,
                delivery = delivery,
                schedule = schedule,
                list_date = list_date,
                link = link,
                notes = notes
            )
        else:
            listing.update(
                salary = salary,
                location = location,
                delivery = delivery,
                schedule = schedule,
                list_date = list_date,
                link = link,
                notes = notes
            )
            listings.append(listing)

    for listing in listings:
        print(listing)
    
    return listings