import json
import gspread
from dataclasses import dataclass
import requests



def ipynb_to_md(ipynb_content):
    data = json.loads(ipynb_content)
    md = ""

    for cell in data["cells"]:
        if cell["cell_type"] == "markdown":
            md += "".join(cell["source"]) + "\n\n"

        elif cell["cell_type"] == "code":
            md += "```python\n"
            md += "".join(cell["source"])
            md += "\n```\n\n"

    return md



@dataclass
class Student:
    id: str
    repo: str
    group_name: str

    _all_solutions = []

    @classmethod
    def from_sheet_dict(cls, d):
        return cls(
            id=d['Telegram ID'],
            repo=d['Github Repo'],
            group_name=d['Group Name']
        )
    
    def _get_solutions(self, contents):
        for item in contents:
            item_name = item['name']
            item_type = item['type']

            if item_type == 'dir' and item_name != '.idea':
                res = requests.get(item['url'])
                res.raise_for_status()
                inner_contents = res.json()
                self._get_solutions(inner_contents)
            elif item_type == 'file' and item_name.endswith(('.py', '.ipynb')):
                res1 = requests.get(item['download_url'])
                res1.raise_for_status()
                txt = res1.text
                if item_name.endswith('.ipynb'):
                    txt = ipynb_to_md(txt)
                
                txt = f"#{item['path']}\n\n" + txt

                self._all_solutions.append(txt)


    def get_solution(self, lesson_number, subject):
        self._all_solutions.clear()

        base_path = f'{subject}/lesson-{lesson_number}'
        url = f"https://api.github.com/repos/{self.repo}/contents/{base_path}?ref=main"

        res = requests.get(url)
        res.raise_for_status()
        contents = res.json()


        self._get_solutions(contents)
        return '\n'.join(self._all_solutions)



class SpreadSheet:
    def __init__(self, sheet_url):
        self.gc = gspread.service_account(filename="gs-keys.json")
        self.sheet = self.gc.open_by_url(sheet_url)
        self.master_ws = self.sheet.worksheet("Master Table")


    def get_student_by_id(self, telegram_id):
        students = self.master_ws.get_all_records()
        student = [student for student in students if str(student['Telegram ID']) == telegram_id]
        if len(student) == 1:
            student = student[0]
        else:
            raise Exception

        student = Student.from_sheet_dict(student)
        return student


    def get_students(self):
        students = self.master_ws.get_all_records()
        return [Student.from_sheet_dict(student) for student in students]


    def mark_student(self, student, lesson_number, subject, mark):
        pass


if __name__ == '__main__':
    # Assuming that Telegram bot provided this
    user_id = '1'
    lesson_number = 3
    subject = 'ml'


    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1SV34tnSlfh-2iu3X_OOewG_7T839jhwiqNxhSr4SAbI/edit?gid=872752510#gid=872752510"
    sheet = SpreadSheet(spreadsheet_url)

    student = sheet.get_student_by_id(user_id)
    solution = student.get_solution(lesson_number=lesson_number, subject=subject)

    # NOTE: This is hardcoded
    mark = 80

    # TODO: implement this method. For not this does not work
    sheet.mark_student(student=student, lesson_number=lesson_number, subject=subject, mark=mark)
    
