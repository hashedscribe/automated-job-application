import os, sys
import base64
import re
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from job_class import JobListing

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

def make_linkedin_listing(url, text):
    # given the text, are we able to get enough information ? not sure
    # visually i see hour if possible , company name, and location
    # also bracket remote but idk if thats a full indicator
    
    # def could try lol
    
    # i think i need to fetch the outer <a>, that's what i was picking up before
    # so i can use regex and have the nested linking !! huge.
    
    # so we go by sender and then just want to handle all the linkedin things
    # per email, we want to match to the following. rn it seems like the regex 
    # looks something like

    # acc gonna do it in another file so it's easily changeable 
    
    print(url, text)
    
    linkedin = r'https?://www\.linkedin\.com[^\s"<>]*/[\d]+/'
    linkedin_match = re.match(linkedin, url)
    
    sanitized_url = ""
    if linkedin_match:
        sanitized_url = linkedin_match.group().replace("/comm", "")
    else:
        return None
        
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
    # pulls all job URLs out of the email body
    # i think this needs to change because linkedin weird
    listings = []
    pattern = r'<a[^>]+href=["\']?(https?://[^\s"<>]*jobs[^\s"<>]*)["\']?[^>]*>(.*?)</a>'
    matches = re.findall(pattern, html, re.DOTALL)
    
    # all the fields we could want to fill
    
    for url, text in matches:
        res = None
        if "linkedin" in url:
            res = make_linkedin_listing(url, text)
        elif "indeed" in url:
            res = handle_indeed(url, text)
        else:
            continue
        
        if res != None:
            (title, company, salary, location, delivery, schedule, list_date,
             link, notes) = res
        else:
            continue
        
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

def get_gmail_results(query_pkt):
    service = get_gmail_service()
    messages = fetch_job_emails(query_pkt["senders"],
                                additional_filters=query_pkt["gmail_additional_filters"])

    listings = set()
    for msg in messages:
        body = get_email_body(service, msg['id'])
        links = extract_job_links(body)