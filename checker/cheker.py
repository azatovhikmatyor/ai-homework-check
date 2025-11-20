from content import Homework
from sheet import Solution
import random

class HomeworkChecker:
    # NOTE: There will be other parameters which are specific for AI model
    def __init__(self, homework: Homework) -> None:
        self.hw = homework

    def check(self, solution: Solution) -> dict:
        # NOTE: fake implementation
        score = random.randint(0, 100)
        return dict(score=score, suggestion=None)  # XXX: What should the result contain?
