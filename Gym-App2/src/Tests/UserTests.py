import unittest
import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User.User(70, 150)
        self.user.goals = []  # Equivalent to Java's `new ArrayList<>()`

    def test_change_weight(self):
        self.user.change_weight(180)
        self.assertEqual(self.user.weight, 180)

        self.user.change_weight(200)
        self.assertEqual(self.user.weight, 200)

    def test_change_height(self):
        self.user.change_height(75)
        self.assertEqual(self.user.height, 75)

        self.user.change_height(80)
        self.assertEqual(self.user.height, 80)

    def test_update_availability(self):
        self.user.update_availability(5)
        self.assertEqual(self.user.avail, 5)

if __name__ == '__main__':
    unittest.main()
