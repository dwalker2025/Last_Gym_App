import unittest
#uncomment below and copy paste a version of the food class from the main code into the testing folder to run 
# import Food

class FoodTest(unittest.TestCase):
    #creates food with lots of parameters and minimum parameters
    def setUp(self):
        self.food1=Food.Food("Mochi",200,True,True,False,False,True,False,True,True)
        self.food2=Food.Food("Pasta",400,True)

#making sure variables, including implicit autofill ones work
    def test_food_constructor(self):
        self.assertEqual(self.food1.name,"Mochi")
        self.assertEqual(self.food2.name,"Pasta")
        self.assertEqual(self.food1.isNut,False)
        self.assertEqual(self.food2.isSoy,False)

#making sure that you can set explicit and implicit variables for both types of obkects with parameters given
    def test_setter(self):
        self.food1.name="Red Bean"
        self.food2.isVegan=False
        self.food1.isBulking=False
        self.food2.isShellfish=True
        self.assertEqual(self.food1.name,"Red Bean")
        self.assertEqual(self.food1.isBulking,False)
        self.assertEqual(self.food2.isVegan,False)
        self.assertEqual(self.food2.isShellfish,True)



if __name__ == '__main__':
    unittest.main()
