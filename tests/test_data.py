""" Test for modules in data and some functions outside of it """

import unittest

import source.web_scraping as web
import Data.generating_scripts.course_generator as subject_generator


class TestWebScraping(unittest.TestCase):

    def test_subject_to_dep_num(self):
        attempted = subject_generator.generate_course_department_id()
        actual = web.create_subject_to_department_number_dict()
        both = [attempted, actual]
        both_names = ["attempted", "actual"]
        for i in range(len(both)):
            for course_letters in both[i]:
                if course_letters not in both[i-1]:
                    print("The following 3 letter designation was in {0} but not {1} {2}".format(both_names[i],
                                                                                                 both_names[i-1],
                                                                                                 course_letters))
                elif both[i][course_letters] != both[i-1][course_letters]:
                    print("The following 3 letter designation is not equal: {0}, {1} for {2}, {3} for {4}".
                          format(course_letters,
                                 both[i][course_letters], both_names[i],
                                 both[i-1][course_letters], both_names[i-1]))

        assert(attempted == actual)


if __name__ == '__main__':
    unittest.main()
