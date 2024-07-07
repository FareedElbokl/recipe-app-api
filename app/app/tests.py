"""
Sample Tests
"""
from django.test import SimpleTestCase

from app import calc

# define test case class
class CalcTests(SimpleTestCase):
    """Test the calc module"""

    def test_add_numbers(self):
        """Test adding numbers together"""
        res = calc.add(6,5)

        self.assertEqual(res, 11)

    def test_subtract_numbers(self):
        """Test subtracting"""
        res = calc.subtract(6,4)
        
        self.assertEqual(res, 2)
