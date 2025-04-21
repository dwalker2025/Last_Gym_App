import unittest

class test(unittest.TestCase):
   
   def tester(self):
      self.assertEqual(9,9, "what the heck")
      self.assertEqual(3,4,"nope")


if __name__=="__main__":
   unittest.main()