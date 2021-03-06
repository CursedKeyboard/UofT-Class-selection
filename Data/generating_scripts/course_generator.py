import requests
from bs4 import BeautifulSoup, element
import json


def generate_course_department_id(department_numbers: int = 60) -> dict:
    """
    Generates a dictionary which maps first 3 letters of course codes to department numbers and is written into a
    file for use elsewhere. Assumes there are a maximum of <department_numbers>
    """
    base_url = "http://student.utm.utoronto.ca/calendar/newdep_detail.pl"
    subject_to_department = dict()

    for i in range(1, department_numbers + 1):
        query = {"Depart": str(i)}
        department_page_source = requests.get(base_url, params=query).text
        soup = BeautifulSoup(department_page_source, 'lxml')
        courses_table = soup.find('table')

        # Handle Non existent departments like department 35
        # If it does exist set values up
        try:
            courses_table['style']
        except KeyError:
            courses = courses_table.find_all('tr')
            set_course_to_value(courses, subject_to_department)

    return subject_to_department


def set_course_to_value(courses: element, d: dict) -> None:
    """ Set up course code to department number by parsing through the department number courses """
    for course in courses:
        subject_code = course.td.a.text[:3]
        depart_num = course.td.a['href'].split('&')[0]
        depart_num = depart_num[depart_num.rfind('=') + 1:]

        if subject_code not in d:
            d[subject_code] = [depart_num]
        elif depart_num in d[subject_code]:
            pass
        else:
            d[subject_code].append(depart_num)


def write_subject_to_department():
    subject_to_department = generate_course_department_id()
    with open('../subject_to_dep_num.txt', 'w') as file:
        file.write(json.dumps(subject_to_department))


if __name__ == '__main__':
    write_subject_to_department()
