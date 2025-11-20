from .base import Student
from utils import logger

class SpreadSheet:
    def __init__(self, id: str, tab: str):
        self.id = id
        self.tab = tab

    @property
    def students(self) -> list[Student]:
        # NOTE: fake implementation
        s1 = Student(fname='Shohjahon', lname='Shonazarov', repo='https://github.com/Shoha-2006/homeworks')
        s2 = Student(fname='Odilbek', lname='Marimov', repo='https://github.com/odilbekmarimov/maab_python/')
        s3 = Student(fname='Murod', lname='Maxmatkulov', repo='https://github.com/Makhmatkulov/for_ml_ai')

        return [s1, s2, s3]

    def mark(self, student: Student, score: int) -> None:
        # NOTE: fake implementation
        logger.info(f"{student} are given {score}")
        pass
