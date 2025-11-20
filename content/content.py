from .base import Lesson, Homework


class Content:
    repo = "https://github.com/azatovhikmatyor/bi_and_ai_group.git"
    branch = "main"

    # XXX: What should __init__() do?

    @property
    def lessons(self) -> list[Lesson]:
        # NOTE: fake implementation
        return [Lesson(topic=f"lesson {i}") for i in range(20)]

    def get_homework(self, lesson_num: int) -> Homework:
        try:
            lesson = self.lessons[lesson_num]
        except IndexError:
            raise Exception(f"There is no lesson for {lesson_num=} yet.")
        else:
            return lesson.homework
