from abc import ABC, abstractmethod


class Solution(ABC):
    @property
    @abstractmethod
    def unified(self) -> str:
        pass

class PythonSolution(Solution):
    @property
    def unified(self) -> str:
        # NOTE: fake implementation
        return "Unified text from all files"
        


class Student:

    def __init__(self, fname: str, lname: str, repo: str) -> None:
        self.fname = fname
        self.lname = lname
        self.repo = repo

    def get_solution(self, lesson_num: int) -> Solution:
        # NOTE: fake implementation
        return PythonSolution()

    def __str__(self) -> str:
        return f"{self.fname} {self.lname}"

    def __repr__(self) -> str:
        return f"Student(fname={self.fname!r}, lname={self.lname!r}, repo={self.repo!r})"