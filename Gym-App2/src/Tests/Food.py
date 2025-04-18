class Food:
    def __init__(self, name, calories, isVegan, isVegatarian=None, isNut=False, isShellfish=False, isSoy=False, isDairy=False, isWheat=False, isBulking=False):
        self.name = name
        self.calories = calories
        self.isVegan = isVegan
        self.isVegatarian = isVegan if isVegatarian is None else isVegatarian
        self.isNut = isNut
        self.isShellfish = isShellfish
        self.isSoy = isSoy
        self.isDairy = isDairy
        self.isWheat = isWheat
        self.isBulking = isBulking

    def get_name(self):
        return self.name

    def get_calories(self):
        return self.calories

    def is_vegan(self):
        return self.isVegan

    def is_vegatarian(self):
        return self.isVegatarian

    def is_nut(self):
        return self.isNut

    def is_shellfish(self):
        return self.isShellfish

    def is_soy(self):
        return self.isSoy

    def is_dairy(self):
        return self.isDairy

    def is_wheat(self):
        return self.isWheat

    def is_bulking(self):
        return self.isBulking