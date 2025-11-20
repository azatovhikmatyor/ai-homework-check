import os
from dotenv import load_dotenv

from sheet import SpreadSheet
from content import Content
from checker import HomeworkChecker
from utils import logger

load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")


def main():
    N = 12  # FIXME: N should be dynamic of configurable
    content = Content()
    hw = content.get_homework(lesson_num=N)
    checker = HomeworkChecker(homework=hw)

    sheet = SpreadSheet(
        id=SPREADSHEET_ID, tab="Python scores"
    )

    logger.info(f'Checking for lesson {N} started:')
    print()
    for student in sheet.students:
        sl = student.get_solution(lesson_num=N)
        if sl:
            result = checker.check(solution=sl)
            sheet.mark(student=student, score=result["score"])
        else:
            sheet.mark(student=student, score=0)
    print()
    logger.info(f'Checking for lesson {N} end')


if __name__ == "__main__":
    main()
