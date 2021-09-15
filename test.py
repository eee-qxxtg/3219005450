import unittest
from main import test


class MyTestCase(unittest.TestCase):
    def test_something1(self):
        self.assertEqual(test(), 0.70)

    def test_something2(self):
        self.assertEqual(test(), 0.71)

    def test_something3(self):
        self.assertEqual(test(), 0.79)

    def test_something4(self):
        self.assertEqual(test(), 0.65)

    def test_something5(self):
        self.assertEqual(test(), 0.55)


if __name__ == '__main__':
    unittest.main()
