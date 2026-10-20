import unittest
from inventory import reserve


class ReservationTests(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(reserve(10, 3), 7)

    def test_full_stock(self):
        self.assertEqual(reserve(10, 10), 0)

    def test_zero(self):
        self.assertEqual(reserve(10, 0), 10)

    def test_negative(self):
        with self.assertRaises(ValueError):
            reserve(10, -1)

    def test_oversell(self):
        with self.assertRaises(ValueError):
            reserve(10, 11)


if __name__ == '__main__':
    unittest.main()
