import requests
from bs4 import BeautifulSoup, element
from typing import Tuple, List

#TODO use method to track credits where applicable instead of augmenting
#TODO Add all courses
#TODO look for a more efficient way to store this data
PROGRAM_ADDITIONAL_COURSES = {'ERSPE1038': ['Two of (CSC422H5, CSC423H5, CSC427H5, CSC490H5)'],
                              'ERSPE1688': ['Five half courses from any 300/400 level U of T Mississauga '
                                            'CSC courses (including at least'
                                            '1.0 credit from 400-level courses).'],
                              'ERMAJ1540': ['1.0 credit from (STA310H5, STA312H5, STA313H5, STA314H5, STA315H5,'
                                            'STA348H5, STA413H5, STA431H5, STA437H5, STA441H5, STA457H5, CSC322H5,'
                                            'CSC411H5; MAT302H5, MAT311H5, MAT332H5, MAT334H5, MAT344H5,'
                                            'MAT337H5/MAT378H5.'],
                              'ERSPE1868': ["At least 1.0 credit from the following list of recommended courses,"
                                            " of which at least 0.5 must be at the 400-level: BIO315H5, BIO341H5,"
                                            " BIO370Y5, BIO371H5, BIO380H5, BIO443H5, BIO481Y5; CBJ481Y5; CHM361H5;"
                                            " CSC310H5, CSC338H5, CSC363H5; JCP410H5;"
                                            " STA302H5/STA331H5,STA348H5, STA442H5"],
                              'ERMAJ1688': ["two of (CSC209H5, CSC258H5, CSC263H5)",
                                            "Four half courses from any 300/400 level U of T Mississauga CSC"
                                            " courses (including at least 0.5 credit from a 400-level course)."]}
CREDIT_COURSE_CODE = {'H': 0.5, 'Y': 1.0}


def find_table_course(program_code: str) -> element.ResultSet:
    """ Return the bs4 tag which holds all html info about courses """
    default_gateway = 'http://student.utm.utoronto.ca/calendar/program_detail.pl'
    program_query = {'Program': program_code}
    program_page_source = requests.get(default_gateway, params=program_query).text
    soup = BeautifulSoup(program_page_source, 'lxml')

    table = soup.find('table', class_='tab_adm')
    return table.find_all(width='80%')


def create_set_program(program_code: str) -> set:
    table_courses = find_table_course(program_code)

    courses = set()
    non_parsable_count = 0
    for line in table_courses:
        line_text_neat = line.text.replace(';', ',').replace(' ', '')
        line_text_neat = replace_in_parenthesis(line_text_neat, ',', '^')
        line_text_neat = line_text_neat.split(',')

        for potential_course in line_text_neat:
            if len(potential_course) == 8:
                course_chosen = potential_course
            elif not potential_course[1].isupper():
                additional_requirements(program_code=program_code, course_set=courses, curr_count=non_parsable_count)
                non_parsable_count += 1
                continue
            else:
                print('=' * 20, 'Found choice based classes', sep='\n')
                potential_course_enum = list(enumerate(potential_course.split('/')))
                print(potential_course_enum)

                while True:
                    user_input = input('Which course/courses are you taking? (Enter corresponding number)')
                    try:
                        course_chosen = potential_course_enum[int(user_input)][1]
                        break
                    except TypeError:
                        print('You did not enter a proper value!')
            try:
                add_course(courses, course_chosen)
            except ValueError:
                print('I will ignore that addition')

    return courses


def add_course(course_set: set, course_chosen: str) -> None:
    """ Modifies course_set to include <course_chosen>

    >>> cs = {}
    >>> add_course(cs, 'CSC148H5')
    >>> cs
    {'CSC148H5'}
    """
    chosen_course_multiple = course_chosen.split('^')
    for course_in in chosen_course_multiple:
        course_in = course_in.strip('()')

        if course_in in course_set:
            print('You have already added {0} to your list of courses!'.format(course_in))
            raise ValueError

        course_set.add(course_in)
        

def replace_in_parenthesis(input_str: str, replace: str, replacement: str) -> str:
    """ Return a modified version of <input_str> such that all <replace> within parenthesis are replaced
    with <replacement>

    Precondition: Parenthesis are not nested more than once; len(replace) == 1; replace != '(' or ')'

    >>> replace_commas_in_parenthesis('((,))',",",'a')
    ValueError
    >>> replace_commas_in_parenthesis('(,)', ",", 'a')
    '(a)'
    """
    if len(replace) != 1 or replace == '(' or replace == ')':
        raise ValueError
    open_parenthesis = False
    final_str = str()

    for char in input_str:
        if char == '(' and open_parenthesis:
            raise ValueError
        elif open_parenthesis and char == replace:
            final_str += replacement
        else:
            if char == '(':
                open_parenthesis = True
            elif char == ')':
                open_parenthesis = False
            final_str += char

    return final_str


def add_additional_courses(course_set: set) -> None:
    """ Adds user input courses to <course_set> """
    user_input_course_count = input('How many courses would you like to add?')

    for i in range(int(user_input_course_count)):
        user_input_course_chosen = input('What is the course code for the course you want to add?')
        course_chosen = user_input_course_chosen.upper()
        try:
            add_course(course_set, course_chosen)
            print('You have added {0} and now have {1} credits'.format(course_chosen, count_credits(course_set)))
        except ValueError:
            print('The last addition was cancelled')


def create_program() -> set:
    """ Creates a set with all of a programs required classes and additional ones user has added. Returns that program
    class set and the number of credits in that program
    """
    program_code = input('Enter your program code')

    course_set = create_set_program(program_code=program_code)

    user_input = input('Would you like to add more courses?')

    while user_input.lower() != 'no':
        add_additional_courses(course_set)
        user_input = input('Would you like to add more courses?')

    return course_set


def count_credits(course_list: List[str]) -> int:
    """ Count the number of credits in <course_list>

    Precondition: all items in course list follow UOFT course code

    >>> count_credits(['CSC148H5', 'CSC108H5'])
    1.0
    >>> count_credits(['MAT137Y5'])
    1.0
    """
    try:
        return sum(CREDIT_COURSE_CODE[course[-2]] for course in course_list)
    except KeyError:
        print('Error within, please contact Saiem Irfan')


def additional_requirements(program_code: str, course_set: set, curr_count: int) -> None:
    """ Asks user to add courses based on any non-paresable html """
    print('=' * 20)
    print('Your program has additional requirements\n', PROGRAM_ADDITIONAL_COURSES[program_code][curr_count], sep='')
    add_additional_courses(course_set)

if __name__ == '__main__':
    user_program_choice = input('How many different programs would you like to take at the same time? (2)')

    # if int(user_program_choice) < 2 or int(user_program_choice) >= 5:
    #     print('You must choose between 2 and 4 programs (inclusive)')
    #     raise ValueError

    program_list = list()
    for i in range(int(user_program_choice)):
        print('Program {0}'.format(i + 1))
        program_list.append(create_program())
        print('='*40)

    print('These are the different courses which you will need to take between all programs')
    unique_courses = set()
    for program_stats in program_list:
        for course in program_stats[0]:
            unique_courses.add(course)

    final_credit_count = count_credits(list(unique_courses))
    
    print(unique_courses)
    print('Your final credit total comes out to {0}'.format(final_credit_count))

    print('Thank you for using this program!')
