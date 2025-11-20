import requests
import json
from abc import ABC, abstractmethod


class Solution(ABC):
    @property
    @abstractmethod
    def unified(self) -> str:
        pass


class PythonSolution(Solution):
    def __init__(self, files: list[dict] = None):
        self.files = files or []

    @property
    def unified(self) -> str:
        unified_content = []

        for file in self.files:
            if file["name"].endswith(".py"):
                unified_content.append(f"# {file['name']}\n{file['content']}")
            elif file["name"].endswith(".ipynb"):
                try:
                    notebook = json.loads(file["content"])
                    code_cells = [
                        "".join(cell["source"])
                        for cell in notebook.get("cells", [])
                        if cell.get("cell_type") == "code"
                    ]
                    code = "\n\n".join(code_cells)
                    unified_content.append(f"# {file['name']}\n{code}")
                except json.JSONDecodeError:
                    unified_content.append(f"# {file['name']}\nError parsing .ipynb file")

        return "\n\n".join(unified_content)


class SqlSolution(Solution):
    def __init__(self, files: list[dict] = None):
        self.files = files or []

    @property
    def unified(self) -> str:
        unified_content = []

        for file in self.files:
            if file["name"].endswith(".sql") or file["name"].endswith(".dbo"):
                unified_content.append(f"-- {file['name']}\n{file['content']}")

        return "\n\n".join(unified_content)


class Student:
    def __init__(self, id: int, fname: str, lname: str, repo: str, chat_id: int) -> None:
        self.id = id
        self.fname = fname
        self.lname = lname
        self.repo = repo
        self.chat_id = chat_id

    def _make_request(self, url: str, token=None) -> dict:
        headers = {"Authorization": f"token {token}"} if token else {}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch from {url}: {response.status_code}, {response.json().get('message')}")
            return {}
        return response.json()

    def _get_branches(self, token):
        repo = "/".join(self.repo.split('/')[-2:])
        url = f"https://api.github.com/repos/{repo}/branches"

        try:
            branches_response = self._make_request(url, token)

            if isinstance(branches_response, list) and branches_response:
                return [branch.get('name', 'main') for branch in branches_response]
        except Exception as e:
            print(f"Error fetching branches for {repo}: {e}")

        return ['main']

    def get_solution(self, lesson_num: int, token=None, base_path=None) -> Solution:
        branch = self._get_branches(token=token)[0] or "main"

        repo = "/".join(self.repo.split('/')[-2:])
        base_path = base_path or f"lesson-{lesson_num}/homework"
        base_url = f"https://api.github.com/repos/{repo}/contents/{base_path}?ref={branch}"

        contents = self._make_request(base_url, token)

        if not contents:
            return PythonSolution()

        files_content = []

        if isinstance(contents, dict):
            contents = [contents]

        for item in contents:
            item_name = item["name"]
            item_type = item["type"]

            if item_type == "dir" and item_name != ".idea":
                subdir_files = self.get_solution(lesson_num, token, base_path=f"{base_path}/{item_name}")
                files_content.extend(subdir_files.files)

            elif item_type == "file" and (
                item_name.endswith(".py") or item_name.endswith(".ipynb") or
                item_name.endswith(".sql") or item_name.endswith(".dbo")
            ):
                raw_url = item["download_url"]
                file_response = requests.get(raw_url)
                if file_response.status_code == 200:
                    content = file_response.text
                    files_content.append({"name": item_name, "content": content})
                else:
                    print(f"Failed to fetch file {item_name}: {file_response.status_code}")

        # Determine solution type based on file extensions
        if any(file["name"].endswith((".sql", ".dbo")) for file in files_content):
            return SqlSolution(files=files_content)
        else:
            return PythonSolution(files=files_content)

    def __str__(self) -> str:
        return f"ID: {self.id} | {self.fname} {self.lname}"

    def __repr__(self) -> str:
        return f"Student(fname={self.fname!r}, lname={self.lname!r}, repo={self.repo!r}, chat_id={self.chat_id!r})"


if __name__ == '__main__':
    branch = "main"
    N = 2
    st1 = Student(id=1, fname='H', lname='A', repo='https://github.com/S-H-A-K-H-Z-O-D/st1', chat_id=606689265)
    solution = st1.get_solution(lesson_num=N)
    print(solution.unified)
