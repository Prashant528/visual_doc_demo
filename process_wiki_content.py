from bs4 import BeautifulSoup

def extract_text_with_heading(html_file, output_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all elements with class 'heading-element' and extract their text and their tags
    headings = [(tag.get_text(separator=' ', strip=True), tag.name) for tag in soup.find_all(class_='heading-element')]

    #It's going to add the headings in the sidebar too. So, we have to remove any heading elements that come after "Flutter Wiki"
    end_index = headings.index(('Flutter Wiki', 'h1'))
    final_headings = headings[:end_index]

    # There can be several headings in different levels like h1, h2, h3.
    # Right now, I am selecting h2 elements as the main headings. We may have to change this later on.
    headings_text = [heading[0] for heading in final_headings if heading[1]=='h2']
    print(headings_text)

    # Write the extracted text to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        text = BeautifulSoup(html_content, features="html.parser").get_text()
        f.write(text)

# Example usage:
html_file = 'webpage_content.html'
output_file = 'output.txt'
extract_text_with_heading(html_file, output_file)
