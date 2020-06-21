"""Tests for user class"""

import unittest

from source.course import User


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        self.u = User()

    def test_programs_type(self):
        assert(isinstance(self.u.get_programs(), list))

    def test_active_courses_type(self):
        assert(isinstance(self.u.get_active_courses(), list))

    def test_courses_type(self):
        assert(isinstance(self.u.get_courses(), set))

    def test_credits_type(self):
        assert(isinstance(self.u.get_credits(), float))


if __name__ == '__main__':
    unittest.main()
