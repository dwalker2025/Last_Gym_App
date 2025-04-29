from Food import Food

#Class mostly made for testing, this is the fallback for if our API doesn't cooperate, categorized based on the ways we'll categorize food
class FoodsList:
    def __init__(self):
        self.foods = [
            # Bulking foods
            Food("Chicken Breast", 165, isVegan=False, isVegatarian=False, isBulking=True),
            Food("Brown Rice", 215, isVegan=True, isBulking=True, isWheat=False),
            Food("Peanut Butter", 190, isVegan=True, isNut=True, isBulking=True),
            Food("Whole Milk", 150, isVegan=False, isVegatarian=True, isDairy=True, isBulking=True),
            Food("Oats", 150, isVegan=True, isWheat=True, isBulking=True),
            Food("Avocado", 240, isVegan=True, isBulking=True),

            # Cutting foods
            Food("Broccoli", 55, isVegan=True, isBulking=False),
            Food("Egg Whites", 17, isVegan=False, isVegatarian=True, isDairy=False, isBulking=False),
            Food("Grilled Salmon", 232, isVegan=False, isVegatarian=False, isShellfish=False, isBulking=False),
            Food("Tofu", 94, isVegan=True, isSoy=True, isBulking=False),
            Food("Almonds", 170, isVegan=True, isNut=True, isBulking=False),
            Food("Greek Yogurt", 100, isVegan=False, isVegatarian=True, isDairy=True, isBulking=False),

            # Neutral (can be used for both)
            Food("Sweet Potato", 112, isVegan=True),
            Food("Banana", 105, isVegan=True),
            Food("Quinoa", 120, isVegan=True, isWheat=False),
            Food("Lentils", 230, isVegan=True, isSoy=False),
            Food("Eggs", 78, isVegan=False, isVegatarian=True),
            Food("Shrimp", 99, isVegan=False, isVegatarian=False, isShellfish=True)
        ]

    def get_all_foods(self):
        return self.foods

    def get_bulking_foods(self):
        return [food for food in self.foods if food.is_bulking()]

    def get_cutting_foods(self):
        return [food for food in self.foods if not food.is_bulking() and food.get_calories() < 150]

    def get_vegan_foods(self):
        return [food for food in self.foods if food.is_vegan()]

    def get_vegetarian_foods(self):
        return [food for food in self.foods if food.is_vegatarian()]

    def get_allergen_free(self, nut=False, shellfish=False, soy=False, dairy=False, wheat=False):
        return [
            food for food in self.foods
            if (not nut or not food.is_nut()) and
               (not shellfish or not food.is_shellfish()) and
               (not soy or not food.is_soy()) and
               (not dairy or not food.is_dairy()) and
               (not wheat or not food.is_wheat())
        ]
