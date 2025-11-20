from .base import Lesson

class Content:
    
    def get_lesson(self, lesson_num: int) -> Lesson:
        return Lesson(lesson_num=lesson_num, topic=f'Lesson-{lesson_num}')


if __name__ == "__main__":
    N = 10
    content = Content()
    lesson = content.get_lesson(lesson_num=N)
    homework = lesson.homework
    print(homework.unified)
    