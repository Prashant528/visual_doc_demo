import requests
from bs4 import BeautifulSoup

def extract_webpage_content(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract the text content of the webpage and strip spaces
            # webpage_content = soup.get_text(strip=True)
            webpage_content = soup.find(id='wiki-content')
            # header_element = soup.find(id='header')
            return webpage_content
        else:
            return f"Failed to fetch webpage: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def save_to_md(content, filename):
    file_dir = 'downloaded_files/'
    file_path = file_dir + filename
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Content saved to {file_path} successfully.")
    except Exception as e:
        print(f"An error occurred while saving to {filename}: {str(e)}")
    
    return file_path

# # Example usage:
if __name__=='__main__':
    url = 'https://github.com/flutter/flutter/wiki/Issue-hygiene'  # Replace with the URL of the webpage you want to extract content from
    webpage_content = extract_webpage_content(url)
    save_to_txt(webpage_content, 'webpage_content.txt')

