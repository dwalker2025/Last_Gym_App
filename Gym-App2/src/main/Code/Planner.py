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
    
    #Creates a super simple testing calendar and returns it
    def showCalendar(self):
            self.generic_map()
            return self.map


    #adds the generic variables to the list
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

    def get_history(self):
        return self.history
