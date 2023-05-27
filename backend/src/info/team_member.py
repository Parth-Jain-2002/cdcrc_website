class UserProfile:
    def __init__(self, fname, lname, email):
        self.first_name = fname
        self.last_name = lname
        self.email = email
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def __repr__(self):
        return self.first_name + ' ' + self.last_name

class TeamMember:
    def __init__(self, fname, lname, email, designation, phone, linkedin):
        self.user = UserProfile(fname, lname, email)
        self.designation = designation
        self.phone = phone
        self.linkedin_profile = linkedin
    
    def __str__(self):
        return self.user.__str__()
    
    def __repr__(self):
        return self.user.__repr__()
    