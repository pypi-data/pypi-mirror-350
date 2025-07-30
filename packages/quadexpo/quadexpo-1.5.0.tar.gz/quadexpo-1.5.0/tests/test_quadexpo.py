import unittest
from quadexpo import quadexpo_function

class TestQuadexpoFunction(unittest.TestCase):
    def test_quadexpo_function(self):
        result = quadexpo_function(1, -2, 3, 0.5, 0, 5)
        expected_value = 10.87  # Expected result approximation
        self.assertAlmostEqual(result, expected_value, places=2)

if __name__ == "__main__":
    unittest.main()
