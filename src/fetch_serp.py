import os
from dotenv import load_dotenv
import serpapi
from job_class import JobListing
import dateparser

def construct_queries(positions, exclusions):
    # exclusion_str = ' '.join(f'-{e}' for e in exclusions)
    return positions

def fetch_serp(queries, location="", max_pages=2):
    load_dotenv()
    client = serpapi.Client(api_key=os.getenv("SERP_API_KEY"))
    job_results = []

    for query in queries:
        page = 0
        next_page_token = None

        while page < max_pages:
            params = {
                "engine": "google_jobs",
                "q": query,
                "location": location,
                "google_domain": "google.com",
                "hl": "en",
                "gl": "us",
            }

            if next_page_token:
                params["next_page_token"] = next_page_token

            results = client.search(params)
            job_results += results.get("jobs_results", [])

            next_page_token = results.get("serpapi_pagination", {}).get("next_page_token")
            if not next_page_token:
                break

            page += 1

    return job_results

def get_serp_results(query_pkt):
    queries = construct_queries(query_pkt["positions"], query_pkt["exclusions"])

    listings = set()
    results = fetch_serp(queries, location=query_pkt["location"] )
    for result in results:
        listing = JobListing(result["title"], result["company_name"], result["source_link"])
        

    for key, value in result["detected_extensions"].items():
        if key == "salary":
            listing.update(salary=value)
        elif key == "posted_at":
            listing.update(list_date=dateparser.parse(value).isoformat())
        elif key == "schedule_type":
            listing.update(schedule=value)
        elif key == "work_from_home":
            listing.update(delivery=("Remote" if value else "On Site" ))

        listing.update(notes=[result["description"].replace('\n', '').replace('\r', '')], 
                        location=result["location"])
        # will fail if this job has been seen already
        # one listing should not have more information than
        # the other if both are listed ?
        listings.add(listing)
    
    for listing in listings:
        print(listing)