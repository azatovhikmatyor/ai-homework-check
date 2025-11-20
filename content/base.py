from abc import ABC, abstractmethod

class Homework(ABC):
    @property
    @abstractmethod
    def unified(self) -> str:
        pass

class PythonHomework(Homework):
    @property
    def unified(self) -> str:
        # NOTE: fake implementation
        return "Unified homework text"
    

class Lesson:
    def __init__(self, topic: str):
        self.topic = topic

    @property
    def homework(self) -> Homework:
        # NOTE: fake implementation
        return PythonHomework()
    
    