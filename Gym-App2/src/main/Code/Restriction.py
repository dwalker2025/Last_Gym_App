#details things like food allergies and edits them (as food allergie can change over time!)

class Restriction:
    def __init__(self, is_vegan, is_vegetarian, allergies):
        self.is_vegan = is_vegan
        self.is_vegetarian = is_vegetarian
        self.allergies = allergies

    def get_vegan(self):
        return self.is_vegan

    def get_vegetarian(self):
        return self.is_vegetarian

    def get_allergies(self):
        return self.allergies

    def change_vegan(self, is_vegan):
        self.is_vegan = is_vegan

    def change_vegetarian(self, is_vegetarian):
        self.is_vegetarian = is_vegetarian

    def add_allergy(self, allergy):
        self.allergies.append(allergy)