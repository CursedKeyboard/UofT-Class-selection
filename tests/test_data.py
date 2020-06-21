""" Test for modules in data and some functions outside of it """

import unittest

import source.web_scraping as web
import Data.generating_scripts.course_generator as subject_generator


class TestWebScraping(unittest.TestCase):

    def test_subject_to_dep_num(self):
        attempted = subject_generator.generate_course_department_id()
        actual = web.create_subject_to_department_number_dict()
        print(attempted)
        print(actual)
        assert(attempted == actual)


if __name__ == '__main__':
    unittest.main()
