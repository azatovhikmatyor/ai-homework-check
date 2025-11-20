from base import Homework
import requests


class Content:
    repo = "https://api.github.com/repos/azatovhikmatyor/bi_and_ai_group"
    branch = "main"

    def get_homework(self, lesson_num: int) -> list[Homework]:
        """
        Fetches all .md files in the homework folder of the specified lesson.
        Returns a list of Homework objects.
        """
        folder_url = f"{self.repo}/contents/lesson-{lesson_num}/homework?ref={self.branch}"

        try:
            response = requests.get(folder_url)
            response.raise_for_status()  
            files_info = response.json()

            md_files = []

            for file_info in files_info:
                if file_info["name"].endswith(".md"):  
                    file_url = file_info["download_url"] 
                    file_response = requests.get(file_url)
                    file_response.raise_for_status() 

                    md_files.append(Homework(file={
                        "name": file_info["name"],
                        "content": file_response.text
                    }))

            if not md_files:
                raise FileNotFoundError(f"No .md files found in lesson-{lesson_num}/homework")

            return md_files

        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise FileNotFoundError(
                    f"Lesson {lesson_num} does not exist in the repository or the homework folder is missing"
                ) from e
            else:
                raise Exception(f"Failed to fetch homework files: {e}") from e

        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}") from e

    def get_lesson(self, lesson_num: int) -> list[Homework]:
        try:
            return self.get_homework(lesson_num)
        except FileNotFoundError as e:
            print(e)
            return []
        except Exception as e:
            print(e)
            return []


if __name__ == "__main__":
    content = Content()
    homework_files = content.get_homework(lesson_num=10)
    for homework in homework_files:
            print(homework.file["name"]) 
            print(homework.file["content"])  
            print("-" * 40)  