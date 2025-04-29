import unittest
#copy and paste all the classes listed here from the main into testing to run
import Planner
import WK
import STWK
import Food
import User

class PlannerTest(unittest.TestCase):
    #creating a person, with a simgle workout, planner, and diet made
    def setUp(self):
        john=User.User("John Doe")
        self.planner = Planner.Planner(john,[],[],[],[],[])
        self.workout = WK.WK("Weight Loss", "Running", 300, 30.5)
        self.diet= Food.Food("Biscuts",200,True)
        #self.strength_workout = STWK.STWK("Gaining Weight", "Bench Press", 150, 45.0, 3, 10, 135)
#making sure everything is entered as intended
    def test_constructor_and_getters(self):
        self.assertIsNotNone(self.planner.getWK(), "Workouts list should be initialized")
        self.assertIsNotNone(self.planner.getFoods(), "Diet list should be initialized")
        self.assertIsNotNone(self.planner.get_history(), "History list should be initialized")
        self.assertTrue(self.planner.getWK() == [], "Workouts should start empty")
        self.assertTrue(self.planner.getFoods() == [], "Diet should start empty")
        self.assertTrue(self.planner.get_history() == [], "History should start empty")

#Creating a calendar and making sure it's empty
    def test_show_calendar(self):
        self.planner.getWK().append(self.workout)
        self.planner.getFoods().append(self.diet)  # Assuming Food class exists
        calendar = self.planner.showCalendar()
        self.assertIsNotNone(calendar[0][0], "Calendar should reflect workout count")
        self.assertIsNotNone(calendar[0][1], "Calendar should reflect food count")
        self.assertIsNotNone(calendar, "Calendar should include current week")

#saving the current state in history and map
    def test_log_state(self):
        self.planner.getWK().append(self.workout)
        self.planner.log_state()
        self.assertEqual(len(self.planner.body_history), 1, "History should have 1 week after logging")
        self.assertTrue(len(self.planner.getWK()) == 0, "Workouts should remain empty after logging")
        self.assertTrue(len(self.planner.map) == 0, "Map should be cleared after logging")

#Making a map for the workouts
    def test_make_map(self):
        self.planner.getWK().append(self.workout)
        self.planner.make_map()
        self.assertEqual(len(self.planner.workouts), 1, "Map should have entries for each workout")
        #self.assertEqual(self.planner.map[0], [0, 0], "Map should map day 0 correctly")
        #self.assertEqual(self.planner.map[1], [1, 1], "Map should map day 1 correctly")

#making an empty map
    def test_empty_map(self):
        self.planner.make_map()
        self.assertTrue(len(self.planner.map) == 0, "Map should be empty when no workouts are added")

if __name__ == '__main__':
    unittest.main()
