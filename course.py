
class Course:
    """
    Public Variables:

    """
    
    def __init__(self, name: str, description: str) -> None:
        """
        Precondition: Name follows UofT standard
        """
        self.name = name
        self.description = description
        self.credits = self.credit_count()

    def _get_credit_count(self) -> float:
        """ Return credit count of this course """
        if self.name[-2].lower() == 'h':
            return 0.5
        else:
            return 1.0
class Program:

    def __init__(self) -> None:
        self.courses = list()
        self.credits = 0.0

    def add_course(self, course: Course) -> bool: