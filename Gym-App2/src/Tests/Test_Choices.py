import unittest
from edu import WK, STWK  # Assuming these classes exist in the `edu` module.

class TestWK(unittest.TestCase):
    def setUp(self):
        # Initialize default instances before each test
        self.workout = WK("Weight Loss", "Running", 300, 30.5)
        self.strengthWorkout = STWK("Gaining Weight", "Bench Press", 150, 45.0, 3, 10, 135)

    # Tests for WK class
    def test_WK_constructor_and_getters(self):
        self.assertEqual(self.workout.getType(), "Weight Loss", "Type should match constructor input")
        self.assertEqual(self.workout.getName(), "Running", "Name should match constructor input")
        self.assertEqual(self.workout.getCalories(), 300, "Calories should match constructor input")
        self.assertAlmostEqual(self.workout.getTimeNeeded(), 30.5, places=3, msg="TimeNeeded should match constructor input")

    def test_WK_setters(self):
        self.workout.setType("Gaining Weight")
        self.workout.setName("Bench Press")
        self.workout.setCalories(150)
        self.workout.setTimeNeeded(45.0)

        self.assertEqual(self.workout.getType(), "Gaining Weight", "Type should update after setType")
        self.assertEqual(self.workout.getName(), "Bench Press", "Name should update after setName")
        self.assertEqual(self.workout.getCalories(), 150, "Calories should update after setCalories")
        self.assertAlmostEqual(self.workout.getTimeNeeded(), 45.0, places=3, msg="TimeNeeded should update after setTimeNeeded")

    def test_WK_to_string(self):
        expected = "Workout{type='Weight Loss', name='Running', calories=300, timeNeeded=30.5 minutes}"
        self.assertEqual(str(self.workout), expected, "toString should match expected format")

    def test_WK_edge_case_calories_zero(self):
        zero_cal_workout = WK("Weight Loss", "Yoga", 0, 20.0)
        self.assertEqual(zero_cal_workout.getCalories(), 0, "Calories should be 0")

    def test_WK_edge_case_time_needed_zero(self):
        zero_time_workout = WK("Gaining Weight", "Stretching", 50, 0.0)
        self.assertAlmostEqual(zero_time_workout.getTimeNeeded(), 0.0, places=3, msg="TimeNeeded should be 0.0")

    # Tests for STWK class
    def test_STWK_constructor_and_getters(self):
        self.assertEqual(self.strengthWorkout.getType(), "Gaining Weight", "Type should match constructor input")
        self.assertEqual(self.strengthWorkout.getName(), "Bench Press", "Name should match constructor input")
        self.assertEqual(self.strengthWorkout.getCalories(), 150, "Calories should match constructor input")
        self.assertAlmostEqual(self.strengthWorkout.getTimeNeeded(), 45.0, places=3, msg="TimeNeeded should match constructor input")
        self.assertEqual(self.strengthWorkout.getSets(), 3, "Sets should match constructor input")
        self.assertEqual(self.strengthWorkout.getReps(), 10, "Reps should match constructor input")
        self.assertEqual(self.strengthWorkout.getWeight(), 135, "Weight should match constructor input")

    def test_STWK_setters(self):
        self.strengthWorkout.setSets(4)
        self.strengthWorkout.setReps(8)
        self.strengthWorkout.setWeight(185)

        self.assertEqual(self.strengthWorkout.getSets(), 4, "Sets should update after setSets")
        self.assertEqual(self.strengthWorkout.getReps(), 8, "Reps should update after setReps")
        self.assertEqual(self.strengthWorkout.getWeight(), 185, "Weight should update after setWeight")

        # Verify inherited setters still work
        self.strengthWorkout.setType("Weight Loss")
        self.assertEqual(self.strengthWorkout.getType(), "Weight Loss", "Inherited setType should work")

    def test_STWK_to_string(self):
        expected = "StrengthWorkout{type='Gaining Weight', name='Bench Press', calories=150, timeNeeded=45.0 minutes, sets=3, reps=10, weight=135 lbs}"
        self.assertEqual(str(self.strengthWorkout), expected, "toString should match expected format")

    def test_STWK_edge_case_zero_sets_reps_weight(self):
        edge_case_workout = STWK("Weight Loss", "Push-ups", 100, 15.0, 0, 0, 0)
        self.assertEqual(edge_case_workout.getSets(), 0, "Sets should be 0")
        self.assertEqual(edge_case_workout.getReps(), 0, "Reps should be 0")
        self.assertEqual(edge_case_workout.getWeight(), 0, "Weight should be 0")

if __name__ == '__main__':
    unittest.main()
