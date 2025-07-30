import unittest

from cooltypes.core.CoolInt import CoolInt


class TestCoolInt(unittest.TestCase):

    def setUp(self):
        self.a = CoolInt(10)
        self.b = CoolInt(3)
        self.negative = CoolInt(-5)

    def test_instance_type(self):
        self.assertIsInstance(self.a, CoolInt)
        self.assertIsInstance(self.b + self.a, CoolInt)

    def test_unary_operations(self):
        self.assertEqual(+self.negative, CoolInt(-5))
        self.assertEqual(-self.negative, CoolInt(5))
        self.assertEqual(abs(self.negative), CoolInt(5))
        self.assertEqual(~self.b, CoolInt(~3))

    def test_binary_operations(self):
        self.assertEqual(self.a + self.b, CoolInt(13))
        self.assertEqual(self.a - self.b, CoolInt(7))
        self.assertEqual(self.a * self.b, CoolInt(30))
        self.assertEqual(self.a // self.b, CoolInt(3))
        self.assertEqual(self.a % self.b, CoolInt(1))
        self.assertEqual(divmod(self.a, self.b), (CoolInt(3), CoolInt(1)))
        self.assertEqual(self.a**self.b, CoolInt(1000))
        self.assertEqual(self.a & self.b, CoolInt(10 & 3))
        self.assertEqual(self.a | self.b, CoolInt(10 | 3))
        self.assertEqual(self.a ^ self.b, CoolInt(10 ^ 3))
        self.assertEqual(self.a << 1, CoolInt(20))
        self.assertEqual(self.a >> 1, CoolInt(5))

    def test_reverse_binary_operations(self):
        self.assertEqual(3 + self.a, CoolInt(13))
        self.assertEqual(13 - self.a, CoolInt(3))
        self.assertEqual(2 * self.a, CoolInt(20))
        self.assertEqual(13 // self.a, CoolInt(1))
        self.assertEqual(13 % self.a, CoolInt(3))
        self.assertEqual(divmod(13, self.a), (CoolInt(1), CoolInt(3)))
        self.assertEqual(2**self.b, CoolInt(8))
        self.assertEqual(10 & self.b, CoolInt(10 & 3))
        self.assertEqual(10 | self.b, CoolInt(10 | 3))
        self.assertEqual(10 ^ self.b, CoolInt(10 ^ 3))
        self.assertEqual(2 << self.b, CoolInt(2 << 3))
        self.assertEqual(32 >> self.b, CoolInt(32 >> 3))

    def test_incompatible_types(self):
        with self.assertRaises(TypeError):
            self.a + "string"
        with self.assertRaises(TypeError):
            "string" + self.a
        self.assertEqual(self.a * [1, 2], int(self.a) * [1, 2])
        self.assertEqual([1, 2] * self.a, int(self.a) * [1, 2])

    def test_divmod_with_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divmod(self.a, CoolInt(0))
        with self.assertRaises(ZeroDivisionError):
            divmod(10, CoolInt(0))

    def test_operation_with_plain_ints(self):
        self.assertEqual(self.a + 5, CoolInt(15))
        self.assertEqual(5 + self.a, CoolInt(15))
        self.assertEqual(self.a - 3, CoolInt(7))
        self.assertEqual(20 - self.a, CoolInt(10))
        self.assertEqual(self.a * 2, CoolInt(20))
        self.assertEqual(2 * self.a, CoolInt(20))
        self.assertEqual(self.a**2, CoolInt(100))
        self.assertEqual(2**self.a, CoolInt(2**10))

    def test_repr_and_str(self):
        self.assertEqual(str(self.a), "10")
        self.assertEqual(repr(self.a), "10")  # inherits int's behavior


if __name__ == "__main__":
    unittest.main()
