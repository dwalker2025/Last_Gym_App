# This function creates the week that can be viewed in planner, typically this is created by planner and holds
# all the choices that have been selected for the week

# I am not 100% sure that is the correct way to convert this so I would double check before using it - Owen
class Week:
    def __init__(self, choices_list):
        self.choices = choices_list

    def get_week(self):
        return self.choices
    
    def add_to_week(self,object):
        self.choice.append(object)