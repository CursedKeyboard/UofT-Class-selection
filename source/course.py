from typing import List


class Course:
    """ An object representation of a UofT course

    === Representation Invariants ===
    _code:
        Follows UofT course code standard
    """
    # === Private Attributes ===
    # code:
    #     Course code
    # description:
    #     Description for this course
    # name:
    #     Name for this course

    def __init__(self, code: str, description: str, name: str, class_type: str) -> None:
        """
        Precondition: <code> follows UofT standard
        """
        self._code = code
        self._description = str(description)
        self._name = name
        self._type = class_type

    def __str__(self):
        return "{0}|{1}".format(self._code, self._name)

    def get_credit_count(self) -> float:
        """ Returns number of credits gained upon successful completion of this course """
        if self._code[-2].lower() == 'h':
            return 0.5
        else:
            return 1.0

    def get_course_code(self) -> str:
        """ Returns course code for this course """
        return self._code

    def get_desc(self) -> str:
        """ Returns description for this course """
        return self._description

    def set_desc(self, new_description: str) -> None:
        """ Modifies description to <new_description> """
        self._description = new_description

    def get_course_subject(self) -> str:
        """ Returns the subject type based on UofT code """
        return self._code[:3]

    def get_course_name(self) -> str:
        """ Returns the course name """
        return self._name

    def get_course_type(self):
        """ Returns the course type """
        return self._type


class Program:

    def __init__(self, code: str, description: str) -> None:
        self._code = str(code)
        self._description = str(description)
        self._courses = list()

    def get_name(self) -> str:
        """ Returns program code """
        return self._code

    def add_course(self, course: Course) -> bool:
        """ Adds a course to the program """
        if isinstance(course, Course):
            self._courses.append(course)
        else:
            raise TypeError("Argument <course> must be a Course object!")

    def get_courses(self) -> List[Course]:
        """ Returns a list of courses added to this program """
        return self._courses

    def get_credit_count(self) -> float:
        """ Returns the credit count for this program """
        # Fix this, currently only counting number of courses
        return sum(course for course in self._courses)

    def change_description(self, new_description: str) -> None:
        """ Changes the description of the program object """
        self._description = str(new_description)


class User:

    def __init__(self):
        self._total_credits = 0.0
        self._programs = list()
        self._courses = set()
        self._active_courses = list()

    def add_program(self, program: Program):
        """ Adds a program to the user object """
        if len(self._programs) == 3:
            raise ValueError("Cannot add more than 3 programs")
        self._programs.append(program)

    def get_programs(self):
        """ Returns a list of the programs """
        return self._programs

    def _update_credits(self, course: Course):
        """ Updates user credit count by adding credits from <course> upon successful completion"""
        if course.get_course_code()[-2] == 'Y':
            self._total_credits += 1.0
        else:
            self._total_credits += 0.5

    def get_credits(self) -> float:
        """ Returns user credit count """
        return self._total_credits

    def get_courses(self):
        """ Returns a set of user courses"""
        return self._courses

    def get_active_courses(self):
        """ Returns a list of user's active courses """
        return self._active_courses

    def add_course(self, course: Course):
        """ Adds course to user and updates active courses effectively """
        self._courses.add(course)
        if len(self._active_courses) == 4:
            self._active_courses.pop(0)
        self._active_courses.append(course)
        self._update_credits(course)
