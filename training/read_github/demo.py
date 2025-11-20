import requests
import json
from pprint import pprint

def get_files_in_folder(repo, folder_path, token=None, branch="main"):
   
    base_url = f"https://api.github.com/repos/{repo}/contents/{folder_path}?ref={branch}"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(base_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch folder contents: {response.status_code}, {response.json().get('message')}")
        return {}

    files_content = {}

    for item in response.json():
        isPy =  item["name"].endswith(".py")
        isIpynb = item["name"].endswith(".ipynb")
        if item["type"] == "file" and (isPy or isIpynb):
            raw_url = item["download_url"]
            file_response = requests.get(raw_url)

            if file_response.status_code == 200:
                content = file_response.text

                # Handle .ipynb files
                if item["name"].endswith(".ipynb"):
                    try:
                        ipynb_data = json.loads(content)
                        # Extract text from the notebook cells
                        ipynb_text = ''.join(
                            ''.join(cell.get('source', [])) for cell in ipynb_data.get('cells', [])
                        )
                        files_content[item["name"]] = ipynb_text
                    except json.JSONDecodeError as e:
                        print(f"Failed to decode JSON for {item['name']}: {e}")
                        files_content[item["name"]] = content
                else:
                    # Store .py file content
                    files_content[item["name"]] = content
            else:
                print(f"Failed to fetch file {item['name']}: {file_response.status_code}")

    return files_content

# Example usage
repo = "S-H-A-K-H-Z-O-D/PythonHomeworks"
folder_path = "lesson-12/homework"
token = None  # Add your GitHub token here if needed
branch = "main"

files = get_files_in_folder(repo, folder_path, token, branch)
pprint(files)
# Display the results
for file_name, content in files.items():
    print(f"\n--- {file_name} ---")
    print(content)
