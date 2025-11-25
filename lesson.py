import requests
from urllib.parse import quote


class Lesson:
    repo = "https://api.github.com/repos/azatovhikmatyor/ai-homeworks/contents"
    branch = "main"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    def __init__(self, lesson_num: int, subject: str, topic: str = None):
        self.lesson_num = lesson_num
        self.subject = subject
        self.topic = topic
        self.homework_files = []

    def _fetch_homework_files(self):
        response = requests.get(f"{self.repo}/{self.subject}?ref={self.branch}", headers=self.headers)
        response.raise_for_status()

        folder_name = [info['name'] for info in response.json() if info['name'].startswith("lesson " + str(self.lesson_num).rjust(2, "0"))]

        if len(folder_name) == 1:
            folder_name = folder_name[0]
        else:
            raise Exception(f"Lesson number with {self.lesson_num} could not be found.")

        encoded_folder_name = quote(folder_name)

        try:
            response = requests.get(f"{self.repo}/{self.subject}/{encoded_folder_name}?ref={self.branch}", headers=self.headers)
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
    def homework(self):
        if not self.homework_files:  
            self._fetch_homework_files()
        
        return "\n\n".join([f"# {file['name']}\n{file['content']}" for file in self.homework_files])

if __name__ == '__main__':
    l = Lesson(3, 'ml')

    print(l.homework)