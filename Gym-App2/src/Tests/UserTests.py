import unittest
#paste the user class into the test class to test this
from user import format_user_info

class TestUserInfo(unittest.TestCase):

#creating a vegetarian
    def test_format_user_info_vegetarian(self):
        result = format_user_info(
            name="Garen",
            height="195",
            weight="85",
            goal="Bulk",
            vegetarian=True,
            restrictions="None"
        )
        expected = (
            "Name: Garen\nHeight: 195 cm\nWeight: 85 kg\n"
            "Goal: Bulk\nVegetarian: Yes\nRestrictions: None"
        )
        self.assertEqual(result, expected)

    #Creatign a non-vegetarian that can't have milk
    def test_format_user_info_non_vegetarian_with_restrictions(self):
        result = format_user_info(
            name="Renn",
            height="180",
            weight="75",
            goal="Cut",
            vegetarian=False,
            restrictions="Lactose intolerant"
        )
        expected = (
            "Name: Renn\nHeight: 180 cm\nWeight: 75 kg\n"
            "Goal: Cut\nVegetarian: No\nRestrictions: Lactose intolerant"
        )
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
