import os
import serpapi
import json

def get_job_hits(query, location):
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",           # Language
        "api_key": "YOUR_FREE_SERP_API_KEY"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    # Google Jobs returns 'jobs_results' as a list
    jobs = results.get("jobs_results", [])
    
    return jobs

# Example: Finding Security Internships in Toronto
found_jobs = get_job_hits("Cybersecurity Intern", "Toronto, ON")

for job in found_jobs:
    print(f"[{job.get('company_name')}] {job.get('title')}")
    print(f"Link: {job.get('related_links', [{}])[0].get('link')}\n")