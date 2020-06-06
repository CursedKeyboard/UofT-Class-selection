import requests
from bs4 import BeautifulSoup, element
from source.course import Course, Program
from typing import Optional, Union, Tuple, List
from source import utils
from source.gui import gui_popups

SPECIAL_MESSAGES = {'ERSPE1038': ['Two of (CSC422H5, CSC423H5, CSC427H5, CSC490H5)'],
                    'ERSPE1688': ['Five half courses from any 300/400 level U of T Mississauga '
                                  'CSC courses (including at least 1.0 credit from 400-level courses).'],
                    'ERMAJ1540': ['1.0 credit from (STA310H5, STA312H5, STA313H5, STA314H5, STA315H5, '
                                  'STA348H5, STA413H5, STA431H5, STA437H5, STA441H5, STA457H5, CSC322H5, '
                                  'CSC411H5; MAT302H5, MAT311H5, MAT332H5, MAT334H5, MAT344H5, MAT337H5/MAT378H5.'],
                    'ERSPE1868': ["At least 1.0 credit from the following list of recommended courses, "
                                  "of which at least 0.5 must be at the 400-level: BIO315H5, BIO341H5, "
                                  "BIO370Y5, BIO371H5, BIO380H5, BIO443H5, BIO481Y5; CBJ481Y5; CHM361H5; "
                                  "CSC310H5, CSC338H5, CSC363H5; JCP410H5; STA302H5/STA331H5,STA348H5, STA442H5"],
                    'ERMAJ1688': ["two of (CSC209H5, CSC258H5, CSC263H5)",
                                  "Four half courses from any 300/400 level U of T Mississauga CSC "
                                  "courses (including at least 0.5 credit from a 400-level course)."]}


def create_subject_to_department_number_dict() -> dict:
    """ Create a dictionary which maps subjects to department numbers """
    final_dict = {}
    with open('../Data/subject_to_dep_num.txt', 'r') as file:
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


def create_program(program_code: str, applet) -> Program:
    """ Returns a Program object containing all courses which are available on <program_code>'s program on the UTM
    programs website

    Args:
        program_code: The official code for a user inputted program
        user: The user which will have courses from program and eventually program added to
        applet: The applet which will be updated

    Returns:
        Program object corresponding to program_code and optional classes which user chooses
    """
    user = applet.user
    program = Program(code=program_code, description='Test')
    table_courses = find_table_course(program_code)

    for line in table_courses:
        line_text_neat = line.text.replace(';', ',').replace(' ', '')
        line_text_neat = utils.replace_in_parenthesis(line_text_neat, ',', '^')
        line_text_neat = line_text_neat.split(',')

        num_errors = 0
        for potential_course in line_text_neat:
            update = True
            check_potential_course = sdf(potential_course)
            if isinstance(check_potential_course, str):
                course = create_course(check_potential_course)

                program.add_course(course=course)
                user.add_course(course)

                applet.update_middle_segment(course=course)
                applet.mid.update()
                applet.bottom.update()
            elif isinstance(check_potential_course, int):
                update = False
                pass_special_message(program_code, num_errors)
            else:
                # take_user_input(check_potential_course)
                courses_added = add_user_input(program=program, potential_courses=check_potential_course,
                                               course_list=[])
                for course in courses_added:
                    user.add_course(course)
                    applet.update_middle_segment(course=course)

            if update:
                applet.update_active_courses_footer()
    return program


def sdf(potential_course: str) -> Union[str, int, List[Tuple[int, str]]]:
    if len(potential_course) == 8:
        return potential_course
    elif not potential_course[1].isupper():
        return -1
    else:
        return list(enumerate(potential_course.split('/')))


def pass_special_message(program_code: str, num: int):
    gui_popups.special_message(message=SPECIAL_MESSAGES[program_code][num])


def get_user_input(potential_courses: List[Tuple[int, str]]):
    courses = gui_popups.take_user_input(choices=potential_courses)
    return courses


def add_user_input(program: Program, potential_courses: List[Tuple[int, str]], course_list=[]) -> List[Course]:
    courses = get_user_input(potential_courses)
    chosen_course_multiple = courses[0].split('^')
    for course in chosen_course_multiple:
        course = course.replace('(', '').replace(')', '')
        add_course = True
        for courses_had in program.get_courses():
            if courses_had.get_course_code() == course:
                gui_popups.popup_duplicate_course(course)
                add_course = False
        if add_course:
            course_obj = create_course(course)
            try:
                program.add_course(course_obj)
                course_list.append(course_obj)
            # This error checks to make sure that the course exists because sometimes it doesn't but is left in
            except TypeError:
                gui_popups.course_not_found_popup(course_name=course)
                add_user_input(program, potential_courses, course_list)

    return course_list


def add_custom_course(course: str, applet) -> None:
    user = applet.user
    for course_added in user.get_courses():
        if course_added.get_course_code() == course:
            gui_popups.popup_duplicate_course(course)
            return

    course = create_course(course)
    user.add_course(course)
    applet.update_middle_segment(course=course)
    applet.update_active_courses_footer()


if __name__ == '__main__':
    # c = create_course('CSC148H5')
    # print(c.get_desc())
    create_program('ERSPE1038')