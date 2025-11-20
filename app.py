import os
from dotenv import load_dotenv

from sheet import SpreadSheet
from content import Content
from checker import HomeworkChecker
from telegram import Telegram
from utils import logger

load_dotenv()

SHEET_URL = os.getenv("SHEET_URL")
GIT_TOKEN = os.getenv("GIT_TOKEN")


def main():
    while True:
        N = input("Which lesson? ")
        try:
            content = Content()
            lesson_num = int(N)
            lesson = content.get_lesson(lesson_num=lesson_num)
            hw = lesson.homework
            checker = HomeworkChecker(homework=hw)
            break

        except ValueError:
            print("Invalid input. Please enter a number.")

    sheet = SpreadSheet(
        gs_keys_path='gs-keys.json',
        sheet_url=SHEET_URL,
        lesson_num=N
    )

    logger.info(f'Checking for lesson {N} started:')
    print()
    for student in sheet.students:
        sl = student.get_solution(lesson_num=N, token=GIT_TOKEN)
        
        if sl:
            result = checker.check(solution=sl)
            sheet.mark(student=student, score=int(result["score"]))
            message = f"Lesson-{N}\n\nYour score: {result["score"]}\n\n{result["Feedback"]}"
            st_profile = Telegram(chat_id=student.chat_id, message=message)
            st_profile.send_feedback()

    sheet.write_data_to_sheet(f"SCORE{N}")
    print()
    logger.info(f'Checking for lesson {N} end')


if __name__ == "__main__":
    main()

