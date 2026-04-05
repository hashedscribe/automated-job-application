import re

#TOdo cleean up code for linkedin stuff
# blocks = block_pattern.findall(html)

def parse_details(details_str):
    clean = re.sub(r'<[^>]+>', '', details_str)
    lines = [l.strip() for l in clean.split('\n') if l.strip()]

    company_location = lines[0] if lines else ''
    remote = '(Remote)' in company_location
    company_location = company_location.replace('(Remote)', '').strip()
    parts = company_location.split('·')
    company = parts[0].strip() if len(parts) > 0 else ''
    location = parts[1].strip() if len(parts) > 1 else ''

    salary = ''
    for line in lines[1:]:
        if '$' in line or '/' in line:
            salary = line.strip()
            break

    return company, location, remote, salary

def parse_block(block):
    pattern = re.compile(
        r'<a\s+href="(https://www\.linkedin\.com/comm/jobs/view/(\d+)/[^"]*)"[^>]*>'
        r'.*?'
        r'<a\s+href="https://www\.linkedin\.com/comm/jobs/view/\2/[^"]*"[^>]*>'
        r'(.*?)'
        r'</a>'
        r'(.*?)'
        r'</a>',
        re.DOTALL
    )

    match = pattern.search(block)
    if not match:
        return None

    link = match.group(1)
    title = re.sub(r'<[^>]+>', '', match.group(3)).strip()
    company, location, remote, salary = parse_details(match.group(4))

    return (title, company, salary, location, "Remote" if remote else "Onsite", None, None,
                link, [])

def make_linkedin_listings(html):
    splits = re.split(r'(?=<a\s+href="https://www\.linkedin\.com/comm/jobs/view/\d+/)', html)
    
    listings_info = []
    for split in splits:
        listings_info.append(parse_block(split))
    
    return listings_info
    