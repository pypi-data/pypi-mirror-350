import unittest

from cooltypes.CoolInt import CoolInt


class TestCoolInt(unittest.TestCase):

    def setUp(self):
        self.a = CoolInt(10)
        self.b = CoolInt(3)

    def test_unary_operations(self):
        self.assertEqual(abs(self.a), CoolInt(10))
        self.assertEqual(-self.b, CoolInt(-3))
        self.assertEqual(+self.b, CoolInt(3))
        self.assertEqual(~self.a, CoolInt(~10))

    def test_binary_operations(self):
        self.assertEqual(self.a + self.b, CoolInt(13))
        self.assertEqual(self.a - self.b, CoolInt(7))
        self.assertEqual(self.a * self.b, CoolInt(30))
        self.assertEqual(self.a // self.b, CoolInt(3))
        self.assertEqual(self.a % self.b, CoolInt(1))
        self.assertEqual(self.a**self.b, CoolInt(1000))
        self.assertEqual(self.a & self.b, CoolInt(10 & 3))
        self.assertEqual(self.a | self.b, CoolInt(10 | 3))
        self.assertEqual(self.a ^ self.b, CoolInt(10 ^ 3))
        self.assertEqual(self.a << self.b, CoolInt(10 << 3))
        self.assertEqual(self.a >> self.b, CoolInt(10 >> 3))

    def test_reverse_binary_operations(self):
        self.assertEqual(3 + self.a, CoolInt(13))
        self.assertEqual(13 - self.a, CoolInt(3))
        self.assertEqual(3 * self.a, CoolInt(30))
        self.assertEqual(30 // self.a, CoolInt(3))
        self.assertEqual(13 % self.a, CoolInt(3))
        self.assertEqual(2**self.b, CoolInt(8))
        self.assertEqual(10 & self.b, CoolInt(10 & 3))
        self.assertEqual(10 | self.b, CoolInt(10 | 3))
        self.assertEqual(10 ^ self.b, CoolInt(10 ^ 3))
        self.assertEqual(3 << self.b, CoolInt(3 << 3))
        self.assertEqual(128 >> self.b, CoolInt(128 >> 3))

    def test_return_type(self):
        self.assertIsInstance(self.a + self.b, CoolInt)
        self.assertIsInstance(-self.b, CoolInt)
        self.assertIsInstance(3 * self.a, CoolInt)
        self.assertIsInstance(~self.a, CoolInt)


if __name__ == "__main__":
    unittest.main()
