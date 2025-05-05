#Creates the plans for all the code, including creating the weeks of food and workouts, also measures body progress and history of weeks are logged here
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
    
    #Creates a super simple testing calendar
    def showCalendar(self):
        if self.workout.length >= 7 and self.diet.length >= 7:
            for i in range(7):
                self.map.append([self.workouts[i],self.diet[i]])
                return self.map
        if self.workouts and self.diet:
            self.map.append([self.workouts[0],self.diet[0]])
            return self.map
        else:
            self.generic_map()
            return self.map


    def generic_map(self):
        self.map.append(["Burpees","Salmon"])
        self.map.append(["Push-ups","Steak"])
        self.map.append(["Weights","Chicken Alfredo"])
        self.map.append(["Jumping Jacks","Shrimp"])
        self.map.append(["Crunches","Calamari"])
        self.map.append(["Break day","Mystery Meat"])
        self.map.append(["Climbing Wall","Lamb"])
        

#Logs the state of the week, current body height and weight, and resets the weeks food and workouts
    def log_state(self):
       this_week=[self.user.get_height(),self.user.get_weight()]
       self.body_history.append(this_week)
       self.workouts=[]
       self.food=[]

#WIP to make the map of the body, will be finnished soon
    def make_map(self):
        
        pass

    def get_history(self):
        return self.history
