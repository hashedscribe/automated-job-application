import hashlib

class JobListing:
    def __init__(self, title, company, link):
        self.title = title.strip().lower()
        self.comapny = company.strip().lower()
        
        unique_str = title+company
        # used for hash AND db, required (i think)
        self.id = hashlib.md5(unique_str.encode()).hexdigest()
        
        self.salary = ""
        self.location = "" 
        self.delivery = "On Site"
        self.list_date = ""
        self.link = link
        self.notes = []
    
    def update(self,
            salary = "",
            location = "" ,
            delivery = "On Site",
            list_date = "",
            notes = []
            ):
        
        self.salary = salary
        self.location = location
        if delivery in ["On Site", "Remote", "Hybrid"]:
            self.delivery = delivery
        self.list_date = list_date
        self.notes += notes
        
    # comparison via job id
    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)