import os, sys
from job_db import save_jobs
from fetch_serp import get_serp_results
from fetch_gmail import get_gmail_results
from job_class import JobListing

# get the search profile from config
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config'))
from search_config import *


if __name__=="__main__":
    # use flags -g for gmail, -s for serp, etc.
    # saves unecessary api calls because im poor lol

    job_listings = []
    
    flags = sys.argv[1:]
    for flag in flags:
        flag = flag.replace("-", "")
        print(GMAIL_SCRAPE_PKT)
        if flag == "s":
            job_listings += get_serp_results(SERP_QUERY_PKT)
        elif flag == "g":
            job_listings += get_gmail_results(GMAIL_SCRAPE_PKT)