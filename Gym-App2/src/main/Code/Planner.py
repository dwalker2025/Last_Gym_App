class Planner:
    def __init__(self, user, map, workouts,diet,current_week,history):
        self.user=user #creates the user to be planned for
        self.map=map
        self.workouts=workouts
        self.diet=diet
        self.current_week=current_week
        self.history=history

    def getFoods(self):
        return self.diet
    
    def getWK(self):
        return self.workouts
    
    def showCalendar(self):
        if self.workouts and self.diet:
            self.map[0]=[self.workouts[0],self.diet[0]]
            return self.map
        else:
            self.map[0]=["Salmon","Burpees"]
            return self.map


        

    def log_state(self):
        #For testing, adds current height and weight to the map
        pass

    def make_map(self):
        #For testing, Resets the curent map and logs current state in refreshed map
        pass

    def get_history(self):
        return self.history
