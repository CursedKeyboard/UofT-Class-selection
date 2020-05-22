import requests
from bs4 import BeautifulSoup, element
from course import Course
from typing import Optional


def create_subject_to_department_number_dict() -> dict:
    """ Create a dictionary which maps subjects to department numbers """
    final_dict = {}
    with open('Data/subject_to_dep_num.txt', 'r') as file:
        for line in file:
            line = line.split(',')
            subject = line[0]
            final_dict[subject] = [num.strip() for num in line[1:]]

    return final_dict


SUBJECT_TO_DEPARTMENT_NUMBER = create_subject_to_department_number_dict()


def find_table_course(program_code: str) -> element.ResultSet:
    """ Return the bs4 tag which holds all html info about courses """
    default_gateway = 'http://student.utm.utoronto.ca/calendar/program_detail.pl'
    program_query = {'Program': program_code}
    program_page_source = requests.get(default_gateway, params=program_query).text
    soup = BeautifulSoup(program_page_source, 'lxml')

    table = soup.find('table', class_='tab_adm')
    return table.find_all(width='80%')


def get_program_description(program_code: str) -> str:
    """ Returns the official program description """
    with open("data/program_to_description.csv", 'r') as file:
        for line in file:
            if line[:8] == program_code:
                return line[9:]

    raise ValueError("Program Code not found!")


def create_course(course_code: str) -> Optional[Course]:
    base_url = "http://student.utm.utoronto.ca/calendar/course_detail.pl"

    for department_numbers in SUBJECT_TO_DEPARTMENT_NUMBER[course_code[:3]]:
        query = {"Depart": str(department_numbers), 'Course': course_code}

        course_page_source = requests.get(base_url, params=query).text
        soup = BeautifulSoup(course_page_source, 'lxml')

        description = soup.find('span', class_="normaltext")

        if description.b is None:
            data = soup.find('div', class_='centralpos').p.text
            title = data[9:-5]
            class_type = data[-4:-1]
            return Course(course_code, description.text, title, class_type=class_type)


if __name__ == '__main__':
    c = create_course('CSC148H5')
    print(c.get_desc())