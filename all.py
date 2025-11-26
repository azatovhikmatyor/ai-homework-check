import os
from dotenv import load_dotenv
load_dotenv()

from lesson import Lesson
from sheet import SpreadSheet
from checker import HomeworkChecker


# Assuming that Telegram bot provided this
user_id = '1'
lesson_number = 3
subject = 'ml'

SHEET_URL = os.getenv('SHEET_URL')

lesson = Lesson(lesson_number=lesson_number, subject=subject)
homework: str = lesson.homework # Markdown format

sheet = SpreadSheet(sheet_url=SHEET_URL)
student = sheet.get_student_by_id(telegram_id=user_id)
solution: str = student.get_solution(lesson_number=lesson_number, subject=subject) # Markdown format

checker = HomeworkChecker(homework=homework)

res = checker.check(solution=solution)

print(res['score'])
print(res['feedback'])

score = res['score']
feedback = res['feedback']

# FIXME: this method is not implemented yet
sheet.mark_student(student=student, lesson_number=lesson_number, subject=subject, score=score)

# Send suggestion back to the user through telegram bot

