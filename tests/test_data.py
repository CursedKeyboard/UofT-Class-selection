""" Test for modules in data and some functions outside of it """

import unittest

import source.web_scraping as web
import Data.generating_scripts.course_generator as subject_generator


class TestWebScraping(unittest.TestCase):

    def test_subject_to_dep_num(self):
        assert(subject_generator.generate_course_department_id() ==
               web.create_subject_to_department_number_dict())
