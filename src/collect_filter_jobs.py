import os, sys
from job_db import save_jobs
from fetch_serp import *
from job_class import JobListing

# get the search profile from config
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config'))
from search_config import *


if __name__=="__main__":
    get_serp_results()