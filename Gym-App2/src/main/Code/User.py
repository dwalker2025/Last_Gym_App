class User:
    """This is the main user class for our gym software"""

    def __init__(self, height=0, weight=0):
        self.height = height
        self.weight = weight
        self.avail = 0
        self.limits = None
        self.goals = []

    def change_weight(self, new_weight):
        self.weight = new_weight

    def change_height(self, new_height):
        self.height = new_height

    def update_availability(self, new_avail):
        self.avail = new_avail

    def get_height(self):
        return self.height

    def get_weight(self):
        return self.weight