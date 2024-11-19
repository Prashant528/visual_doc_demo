import requests
import re
from urllib.parse import urljoin

class GitHubService:
    def __init__(self, token):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_file_content_from_api(self, owner, repo, path):
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        print("Downloading file: ", url)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            content = response.json()
            if content['type'] == 'file':
                return requests.get(content['download_url']).text
        else:
            print(f"Couldn't download file {path}. Check link again or your Github API key.")
        return None
    
    def get_file_content_from_raw_url(self, owner, repo, file_path):
        # GitHub repository information. Example:
        # owner = 'flutter'
        # repo = 'flutter'
        # file_path = 'CONTRIBUTING.md'

        # Construct the URL to download the raw file
        raw_url = f'https://raw.githubusercontent.com/{owner}/{repo}/main/{file_path}'

        try:
            # Send a GET request to download the file
            response = requests.get(raw_url)
            if response.status_code == 200:
                print("Response code 200")
                response.encoding = 'UTF-8'
                # If the request is successful, return the file as a response
                return(response.content)
            else:
                return f"Failed to download file: {file_path}. Code: {response.status_code}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def extract_links(self, content):
        # Regular expression to match markdown links: [text](link)
        link_pattern = r'\[.*?\]\((.*?)\)'

        # Find all links in the markdown content
        raw_links = re.findall(link_pattern, content)

        # Normalize the links
        abs_links = set()
        relative_links = set()
        for link in raw_links:
            if link.startswith(('http://', 'https://')):
                # If the link is an absolute URL, add it directly
                abs_links.add(link)
            else:
                # Otherwise, add it to relative links
                relative_links.add(link)

        return abs_links, relative_links

    def download_recursive(self, owner, repo, file_path, depth=0):
        
        if depth > 1:  # To avoid infinite recursion
            return
        
        content = self.get_file_content_from_raw_url(owner, repo, file_path)
        # print(content)
        if not content:
            print("File not downloaded.")
            return
        
        # PTANDAN UNComment below section to go deeper on links
        #------------------------------
        # abs_links, relative_links = self.extract_links(content)
        # print("Absolute links found:")
        # # for link in abs_links:
        # #     print(link)
        
        # print("Relative links found: ")
        # for link in relative_links:
        #     print(link)
        #     #TODO: Currently looking at the relative links only. Need to do for absolute links if needs arise.
        #     if link.endswith('.md') or 'wiki' in link:
        #         #create a new file path based on the relative directory.
        #         new_file_path = self.create_new_filepath(file_path, link)
        #         print("New file paths: ", new_file_path)
        #         self.download_recursive(owner, repo, new_file_path, depth + 1)
        #------------------------------


        return [[file_path, content]]

    def create_new_filepath(self, old_file_path, relative_link):
        new_file_path = urljoin(old_file_path, relative_link)
        return new_file_path
    
