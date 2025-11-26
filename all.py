from lesson import Lesson
from sheet import SpreadSheet


# Assuming that Telegram bot provided this
user_id = '1'
lesson_number = 3
subject = 'ml'


lesson = Lesson(lesson_number=lesson_number, subject=subject)
homework = lesson.homework

sheet = SpreadSheet(sheet_url="https://docs.google.com/spreadsheets/d/1SV34tnSlfh-2iu3X_OOewG_7T839jhwiqNxhSr4SAbI/edit?gid=872752510#gid=872752510")
student = sheet.get_student_by_id(telegram_id=user_id)
solution = student.get_solution(lesson_number=lesson_number, subject=subject)

# give homework and solution to AI and get mark and suggestions
mark = ...
suggestions = ...


sheet.mark_student(student=student, lesson_number=lesson_number, subject=subject, mark=mark)

# Send suggestion back to the user through telegram bot

