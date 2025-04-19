class Planner:
    def __init__(self, user, map, workouts, diet, current_week, history):
        self.user=user #creates the user to be planned for
        self.map=map #int[] map for measurements in graph
        self.workouts=workouts #list of possibel workouts for this person
        self.diet=diet #list of possible foods for this person
        self.current_week=current_week #The created list using the two last variables
        self.history=history #History list for each past week
        self.body_history=[]

    def getFoods(self):
        return self.diet
    
    def getWK(self):
        return self.workouts
    
    def showCalendar(self):
        if self.workouts and self.diet:
            self.map.append([self.workouts[0],self.diet[0]])
            return self.map
        else:
            self.map.append(["Salmon","Burpees"])
            return self.map

    def log_state(self):
       this_week=[self.user.get_height(),self.user.get_weight()]
       self.body_history.append(this_week)
       self.workouts=[]
       self.food=[]


    def make_map(self):
        
        pass

    def get_history(self):
        return self.history
