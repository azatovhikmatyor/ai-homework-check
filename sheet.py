import gspread
from dataclasses import dataclass
import pandas as pd
import requests


@dataclass
class Student:
    id: str
    repo: str
    group_name: str

    @classmethod
    def from_sheet_dict(cls, d):
        return cls(
            id=d['Telegram ID'],
            repo=d['Github Repo'],
            group_name=d['Group Name']
        )
    
    def get_solution(self, lesson_num, subject):
        pass



# class Student:
#     def __init__(self, id: int, fname: str, lname: str, repo: str, chat_id: int) -> None:
#         self.id = id
#         self.fname = fname
#         self.lname = lname
#         self.repo = repo
#         self.chat_id = chat_id

#     def _make_request(self, url: str, token=None) -> dict:
#         headers = {"Authorization": f"token {token}"} if token else {}
#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             print(f"Failed to fetch from {url}: {response.status_code}, {response.json().get('message')}")
#             return {}
#         return response.json()

#     def _get_branches(self, token):
#         repo = "/".join(self.repo.split('/')[-2:])
#         url = f"https://api.github.com/repos/{repo}/branches"

#         try:
#             branches_response = self._make_request(url, token)

#             if isinstance(branches_response, list) and branches_response:
#                 return [branch.get('name', 'main') for branch in branches_response]
#         except Exception as e:
#             print(f"Error fetching branches for {repo}: {e}")

#         return ['main']

#     def get_solution(self, lesson_num: int, token=None, base_path=None) -> Solution:
#         branch = self._get_branches(token=token)[0] or "main"

#         repo = "/".join(self.repo.split('/')[-2:])
#         base_path = base_path or f"lesson-{lesson_num}/homework"
#         base_url = f"https://api.github.com/repos/{repo}/contents/{base_path}?ref={branch}"

#         contents = self._make_request(base_url, token)

#         if not contents:
#             return PythonSolution()

#         files_content = []

#         if isinstance(contents, dict):
#             contents = [contents]

#         for item in contents:
#             item_name = item["name"]
#             item_type = item["type"]

#             if item_type == "dir" and item_name != ".idea":
#                 subdir_files = self.get_solution(lesson_num, token, base_path=f"{base_path}/{item_name}")
#                 files_content.extend(subdir_files.files)

#             elif item_type == "file" and (
#                 item_name.endswith(".py") or item_name.endswith(".ipynb") or
#                 item_name.endswith(".sql") or item_name.endswith(".dbo")
#             ):
#                 raw_url = item["download_url"]
#                 file_response = requests.get(raw_url)
#                 if file_response.status_code == 200:
#                     content = file_response.text
#                     files_content.append({"name": item_name, "content": content})
#                 else:
#                     print(f"Failed to fetch file {item_name}: {file_response.status_code}")

#         # Determine solution type based on file extensions
#         if any(file["name"].endswith((".sql", ".dbo")) for file in files_content):
#             return SqlSolution(files=files_content)
#         else:
#             return PythonSolution(files=files_content)

#     def __str__(self) -> str:
#         return f"ID: {self.id} | {self.fname} {self.lname}"

#     def __repr__(self) -> str:
#         return f"Student(fname={self.fname!r}, lname={self.lname!r}, repo={self.repo!r}, chat_id={self.chat_id!r})"



class SpreadSheet:
    def __init__(self, sheet_url):
        self.gc = gspread.service_account(filename="gs-keys.json")
        self.sheet = self.gc.open_by_url(sheet_url)
        self.master_ws = self.sheet.worksheet("Master Table")


    def get_student_by_id(self, telegram_id):
        students = self.master_ws.get_all_records()
        student = [student for student in students if str(student['Telegram ID']) == user_id]
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

    solution = student.get_solution(lesson_num=lesson_number, subject=subject)

