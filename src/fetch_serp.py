import os
from dotenv import load_dotenv
import serpapi

def construct_queries(positions, exclusions):
    exclusion_str = ' '.join(f'-{e}' for e in exclusions)
    return [
        f'{term} {exclusion_str}'.strip()
        for group in positions
        for term in group
    ]

def fetch_serp(queries, max_pages=2):
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
                "location": LOCATION,
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

def get_serp_results(positions, exclusions):
    queries = construct_queries(positions, exclusions)
    # TODO reduce the dict, idk if iwe need all the iinfo provided
    return fetch_serp(queries)