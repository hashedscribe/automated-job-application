import sys, os
import sqlite3
from datetime import date

# get the search profile from config
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config'))
from search_config import *

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            description TEXT,
            apply_link TEXT,
            source TEXT,
            date_found TEXT,
            date_posted TEXT,
            status TEXT DEFAULT 'new',
            score INTEGER,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("DB initialized")
    
def delete_db():
    confirm = input("Are you sure you want to clear the database? (y/n): ")
    if confirm.lower() != 'y':
        print("Aborted")
        return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM jobs")
    conn.commit()
    conn.close()
    print("DB cleared")

def is_relevant(job):
    title = job.get("title", "").lower()
    return not any(e.lower() in title for e in exclusions)

def save_jobs(job_results):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = date.today().isoformat()
    total = 0
    skipped = 0

    for job in job_results:
        if not is_relevant(job):
            skipped += 1
            continue
        
        job_id = make_job_id(job)
        c.execute("""
            INSERT OR IGNORE INTO jobs (id, title, company, location, apply_link, source, date_found)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            job_id,
            job.get("title"),
            job.get("company_name"),
            job.get("location"),
            job.get("job_link"),
            "serpapi",
            today
        ))
        total += c.rowcount

    conn.commit()
    conn.close()
    print(f"Added {total} new jobs, skipped {skipped} irrelevant")
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python db.py [init|clear]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "init":
        init_db()
    elif command == "clear":
        delete_db()
    else:
        print(f"Unknown command: {command}. Use init or clear")