import unittest
import rollerResolver

seed = 123


class TestLexer(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(rollerResolver.run(''), 0)

    def test_int(self):
        self.assertEqual(rollerResolver.run('5'), 5)
        self.assertEqual(rollerResolver.run('345'), 345)
        self.assertEqual(rollerResolver.run('-5'), -5)
        self.assertEqual(rollerResolver.run('-345'), -345)

    def test_binop(self):
        self.assertEqual(rollerResolver.run('2 + 3'), 5)
        self.assertEqual(rollerResolver.run('2 - 3'), -1)
        self.assertEqual(rollerResolver.run('-45 * 4'), -180)
        self.assertEqual(rollerResolver.run('5 / 2'), 2)
        self.assertEqual(rollerResolver.run('6 / -2'), -3)
        self.assertEqual(rollerResolver.run('2 ^ 3'), 8)

    def test_precedence(self):
        self.assertEqual(rollerResolver.run('5 + 6 * 3'), 23)
        self.assertEqual(rollerResolver.run('5 * 6 + 3'), 33)
        self.assertEqual(rollerResolver.run('3 * 4 ^ 2'), 48)
        self.assertEqual(rollerResolver.run('3 + 2d1'), 5)
        self.assertEqual(rollerResolver.run('4d1k2 ^ 3'), 8)

    def test_paren(self):
        self.assertEqual(rollerResolver.run('-(3 * 4)'), -12)
        self.assertEqual(rollerResolver.run('(3 + 4) * 2'), 14)
        self.assertEqual(rollerResolver.run('(3 + 1) ^ (5 - 3)'), 16)

    # TODO
    def test_roll(self):
        self.assertEqual(rollerResolver.run('3d6', seed=seed), 5)

    # TODO
    def test_roll_failure(self):
        return


if __name__ == '__main__':
    unittest.main()
