import unittest
from edu import Planner, WK, STWK  # Assuming these classes exist in the `edu` module.

class TestPlanner(unittest.TestCase):
    def setUp(self):
        self.planner = Planner("John Doe")
        self.workout = WK("Weight Loss", "Running", 300, 30.5)
        self.strength_workout = STWK("Gaining Weight", "Bench Press", 150, 45.0, 3, 10, 135)

    def test_constructor_and_getters(self):
        self.assertIsNotNone(self.planner.getWK(), "Workouts list should be initialized")
        self.assertIsNotNone(self.planner.getFoods(), "Diet list should be initialized")
        self.assertIsNotNone(self.planner.getHistory(), "History list should be initialized")
        self.assertTrue(self.planner.getWK() == [], "Workouts should start empty")
        self.assertTrue(self.planner.getFoods() == [], "Diet should start empty")
        self.assertTrue(self.planner.getHistory() == [], "History should start empty")

    def test_show_calendar(self):
        self.planner.getWK().append(self.workout)
        self.planner.getFoods().append(Planner.Food())  # Assuming Food class exists
        calendar = self.planner.showCalendar()
        self.assertIn("John Doe", calendar, "Calendar should include person name")
        self.assertIn("Workouts: 1", calendar, "Calendar should reflect workout count")
        self.assertIn("Diet: 1", calendar, "Calendar should reflect food count")
        self.assertIn("Current Week", calendar, "Calendar should include current week")

    def test_log_state(self):
        self.planner.getWK().append(self.workout)
        self.planner.logState()
        self.assertEqual(len(self.planner.getHistory()), 1, "History should have 1 week after logging")
        self.assertTrue(len(self.planner.getWK()) == 0, "Workouts should remain empty after logging")
        self.assertTrue(len(self.planner.map) == 0, "Map should be cleared after logging")

    def test_make_map(self):
        self.planner.getWK().append(self.workout)
        self.planner.getWK().append(self.strength_workout)
        self.planner.makeMap()
        self.assertEqual(len(self.planner.map), 2, "Map should have entries for each workout")
        self.assertEqual(self.planner.map.get(0), [0, 0], "Map should map day 0 correctly")
        self.assertEqual(self.planner.map.get(1), [1, 1], "Map should map day 1 correctly")

    def test_empty_map(self):
        self.planner.makeMap()
        self.assertTrue(len(self.planner.map) == 0, "Map should be empty when no workouts are added")

if __name__ == '__main__':
    unittest.main()
