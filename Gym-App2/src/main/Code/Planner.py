class Planner:
    def __init__(self, user, map, workouts, diet, current_week, history):
        self.user=user #creates the user to be planned for
        self.map=map #int[] map for measurements in graph
        self.workouts=workouts #list of possibel workouts for this person
        self.diet=diet #list of possible foods for this person
        self.current_week=current_week #The created list using the two last variables
        self.history=history #History list for each past week

    def getFoods(self):
        return self.diet
    
    def getWK(self):
        return self.workouts
    
    def showCalendar(self):
        #For testing, creates calendar from foods and workouts
        pass

    def log_state(self):
        #For testing, adds current height and weight to the map
        pass

    def make_map(self):
        #For testing, Resets the curent map and logs current state in refreshed map
        pass

    def get_history(self):
        return self.history
