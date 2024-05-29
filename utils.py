import requests

def download_file(owner, repo, file_path):
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
            return f"Failed to download file: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    


if __name__ == '__main__':
    print(download_file('flutter', 'flutter', 'CONTRIBUTING.md'))
