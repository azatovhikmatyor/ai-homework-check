import requests

class LoadGithub:
    def __init__(self, repo: str, folder_path: str):
        self.repo = repo
        self.folder_path = folder_path
        self.base_url = f"https://api.github.com/repos/{repo}/contents/{folder_path}"

    def get_files_in_folder(self):
        """
        Fetches Python files from the specified folder in the GitHub repository.
        """
        base_url_with_branch = f"{self.base_url}?ref=main"  # Branch is always 'main'
        headers = {}  # No token needed
        response = requests.get(base_url_with_branch, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch folder contents: {response.status_code}, {response.json().get('message')}")
            return {}

        files_content = {}
        for item in response.json():
            if item["type"] == "file" and item["name"].endswith(".py"):
                raw_url = item["download_url"]
                file_response = requests.get(raw_url)
                if file_response.status_code == 200:
                    files_content[item["name"]] = file_response.text
                else:
                    print(f"Failed to fetch file {item['name']}: {file_response.status_code}")

        return files_content

    def load(self):
        """
        Loads and prints the Python files' content from the GitHub repo and folder.
        """
        files = self.get_files_in_folder()
        for file_name, content in files.items():
            print(f"--- {file_name} ---")
            print(content)
            print("\n")

lc = LoadGithub()
for i in df['github_repo']:
    a = lc.load(repo=i)
    with open(f'{ddf['st_name']}') as f:
        f.write(a)



