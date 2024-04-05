from bs4 import BeautifulSoup

def extract_text_with_heading(html_file, output_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all elements with class 'heading-element' and extract their text
    headings_text = [tag.get_text(separator=' ', strip=True) for tag in soup.find_all(class_='heading-element')]

    # Write the extracted text to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        text = BeautifulSoup(html_content, features="html.parser").get_text()
        f.write(text)

# Example usage:
html_file = 'webpage_content.html'
output_file = 'output.txt'
extract_text_with_heading(html_file, output_file)
