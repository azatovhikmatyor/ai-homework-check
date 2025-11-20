import requests
from abc import ABC, abstractmethod


class Homework(ABC):
    def __init__(self, file: dict):
        self.file = file

    def __repr__(self):
       return f"<Homework name={self.file['name']}, content={self.file['content']}>"


class PythonHomework(Homework):
    def __init__(self, files: list[dict]):
        self.files = files

    @property
    def unified(self) -> str:
        return "\n\n".join([f"# {file['name']}\n{file['content']}" for file in self.files])


class Lesson:
    repo = "https://api.github.com/repos/azatovhikmatyor/bi_and_ai_group"
    branch = "main"

    def __init__(self, lesson_num: int, topic: str = None):
        self.lesson_num = lesson_num
        self.topic = topic
        self.homework_files = []  

    def fetch_homework_files(self):
        folder_path = f"lesson-{self.lesson_num}/homework"
        api_url = f"{self.repo}/contents/{folder_path}?ref={self.branch}"

        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Handle HTTPS ERRORS

            files_info = response.json() 
            self.homework_files = []  

            for file_info in files_info:
                if file_info["name"].endswith(".md"):  
                    file_url = file_info["download_url"]
                    file_response = requests.get(file_url)
                    if file_response.status_code == 200:
                        self.homework_files.append({
                            "name": file_info["name"],
                            "content": file_response.text
                        })

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as e:
            print(f"Error fetching homework files: {e}")

    @property
    def homework(self) -> Homework:
        if not self.homework_files:  
            self.fetch_homework_files()
        return PythonHomework(self.homework_files)


if __name__ == '__main__':
    lesson10 = Lesson(lesson_num=10, topic="Introduction")
    print(lesson10.homework.unified)
