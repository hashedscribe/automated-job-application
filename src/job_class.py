import hashlib

def title(string):
    new_str = ""
    for word in string.split(" "):
        new_str += word.capitalize() + " "
    return new_str.strip()

class JobListing:
    def __init__(self, title, company, link):
        self.title = title.strip().lower()
        self.company = company.strip().lower()
        
        unique_str = title+company
        # used for hash AND db, required (i think)
        self.id = hashlib.md5(unique_str.encode()).hexdigest()
        
        self.salary = ""
        self.location = "" 
        self.delivery = ""
        self.schedule = ""
        self.list_date = ""
        self.link = link
        self.notes = []
    
    def update(self,
            salary = "",
            location = "" ,
            delivery = "",
            schedule = "",
            list_date = "",
            notes = []
            ):
        
        self.salary = salary if salary != None else self.salary
        self.location = location if location != None else self.location
        # protects against None already
        if delivery in ["On Site", "Remote", "Hybrid"]:
            self.delivery = delivery
        self.schedule = schedule if schedule != None else self.schedule
        self.list_date = list_date if list_date != None else self.list_date
        # if no notes, it will be empty
        self.notes += notes
        
    # comparison via job id
    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
    
    def __str__(self):
        notes_str = '\n              '.join(f"{n[:50]}..." if len(n) > 100 else n for n in self.notes)
        return (f'''
        Title:    {title(self.title)}
        Company:  {title(self.company)}
        Location: {title(self.location)}
        Salary:   {self.salary}
        Schedule: {self.schedule}
        Delivery: {self.delivery}
        Listed:   {self.list_date}
        Link:     {self.link[:50] + "..." if len(self.link)>50 else self.link}
        Notes:    {notes_str}
        ''')
        
    def __repr__(self):
        return(f"({title(self.title)}, {title(self.company)})")