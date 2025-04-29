#holds all the Users in the program
class System:
    def __init__(self, allUsers):
        self.allUsers=allUsers
    
    def get_all_users(self):
        return self.allUsers