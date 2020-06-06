"""Tests for user class"""

import unittest
from source.course import User


class TestUser(unittest.TestCase):

    def test_initializer_types(self):
        u = User()
        assert(isinstance(u.get_programs(), list))
        assert(isinstance(u.get_active_courses(), list))
        assert(isinstance(u.get_courses(), set))
        assert(isinstance(u.get_credits(), float))
