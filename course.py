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
        return self._code

    def add_course(self, course: Course) -> bool:
        if isinstance(course, Course):
            self._courses.append(course)
        else:
            raise TypeError("Argument <course> must be a Course object!")

    def get_courses(self) -> List[Course]:
        return self._courses

    def get_credit_count(self) -> float:
        return sum(course for course in self._courses)

    def change_description(self, new_description: str) -> None:
        self._description = str(new_description)


class User:

    def __init__(self):
        self._total_credits = 0.0
        self._programs = list()
        self._courses = set()
        self._active_courses = []

    def add_program(self, program: Program):
        self._programs.append(program)

    def get_programs(self):
        return self._programs

    def update_credits(self):
        self._total_credits = sum(course.get_credit_count() for course in self._courses)

    def get_credits(self):
        return self._total_credits

    def get_courses(self):
        return self._courses

    def get_active_courses(self):
        return self._active_courses

    def add_course(self, course: Course):
        self._courses.add(course)
        if len(self._active_courses) == 4:
            self._active_courses.pop(0)
        self._active_courses.append(course)
