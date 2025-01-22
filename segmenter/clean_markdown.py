import re
import os
import csv
# import xlsxwriter
import subprocess
from cmarkgfm import github_flavored_markdown_to_html
from bs4 import BeautifulSoup
import sys

def markdn2text_gfm(md_file = '/Users/tandanp/Documents/doc_scraper/contributing.md', repo=''):
    print("Parsing markdown as plain text file...")
    absolute_path = md_file

    # Redefine this variable with your own filepath to cmark-gfm.exe
    # cmark_gfm_exe_path = 'C:\\Users\\fronchettl\\Documents\\cmark-gfm-master\\cmark-gfm-master\\build\\src\\cmark-gfm.exe'
    cmark_gfm_exe_path = '/Users/tandanp/Documents/cmark-gfm/build/src/cmark-gfm'
    if os.path.isfile(cmark_gfm_exe_path):
        plaintext = subprocess.run(['cmark-gfm', absolute_path, '--to', 'plaintext'], stdout=subprocess.PIPE)
    else:
        print('Please, update the filepath to the `cmark-gfm.exe` file inside the scripts/scraper/export.py file')
        print('If you do not have cmark-gfm installed, please visit their repository and install it: github.com/github/cmark-gfm')
        raise ValueError('The cmark-gfm.exe variable was not defined in scripts/scraper/export.py (Line 38)')

    plain_parsed_file = '/Users/tandanp/Documents/doc_scraper/segmenter/outputs/parsed_file_'+repo+'.txt'
    with open(plain_parsed_file, 'w') as f:
        f.write(plaintext.stdout.decode('utf-8'))

    return plain_parsed_file

def markdn2text_with_links(md_file = '/Users/tandanp/Documents/doc_scraper/contributing.md', repo='', filename=''):
    # Read the Markdown file
    with open(md_file, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Convert to plain text while preserving links
    plain_text_with_links = markdown_to_plain_text_with_links(markdown_content)
    plain_parsed_file = '/Users/tandanp/Documents/doc_scraper/segmenter/outputs/parsed_file_'+repo+'_'+filename+'.txt'
    # Optionally, save the plain text to a file
    with open(plain_parsed_file, "w", encoding="utf-8") as f:
        f.write(plain_text_with_links)

    return plain_parsed_file


# Function to convert Markdown to plain text with links preserved
def markdown_to_plain_text_with_links(markdown_text):
    # Convert Markdown to HTML using cmark-gfm
    html = github_flavored_markdown_to_html(markdown_text)
    
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    
    # Function to traverse HTML and rebuild plain text
    def traverse(element):
        plain_text = ""
        for child in element.children:
            if child.name == "a":  # Links
                link_text = child.get_text()
                href = child.get("href", "")
                # Exclude links with href starting with '#'
                if not href.startswith("#"):
                    plain_text += f"[{link_text}]({href})"
            elif child.name in {"strong", "em"}:  # Bold/Italic
                plain_text += traverse(child)  # Handle nested text
            elif child.name == "li":  # List items
                plain_text += f"- {traverse(child)}\n"
            elif child.name == "code":  # Inline code
                plain_text += f"`{child.get_text()}`"
            elif child.name == "pre":  # Code blocks
                plain_text += f"\n```\n{child.get_text()}\n```\n"
            elif child.name:  # Other elements (e.g., paragraphs, headings)
                plain_text += traverse(child)
            else:  # Plain text
                plain_text += child.string or ""
        return plain_text.strip()

    # Traverse the root element to rebuild plain text
    plain_text = traverse(soup)
    print(plain_text.strip())
    return plain_text.strip()



def split_into_paragraphs(content):
    """Splits the content of a documentation file into paragraphs.

    To organize the content of a documentation file into a spreadsheet, first we
    divide it in paragraphs. We consider as paragraphs "one or more consecutive
    lines of text, separated by one or more blank lines (A blank line is any line
    that looks like a blank line—a line containing nothing but spaces or tabs is
    considered blank)". 

    The only exception are the un/ordered lists, which we consider separately as
    paragraphs. We did it because we noticed that some lists contained a significant
    amount of relevant information per item, and dividing it could help us to 
    increase the number of instances for analysis.

    Args:
        content: A string containing the content of a documentation file, including
            empty spaces, line breaks, etc.
    Returns:
        A list of strings, where each string represents a paragraph of the 
        documentation file.
    References:
        Markdown Syntax, by Jhon Gruber:
            daringfireball.net/projects/markdown/syntax
        GitHub Flavored Markdown Spec:
            github.github.com/gfm
    """

    lines = content.splitlines()
    text = []
    paragraph = []

    for line in lines:
        line = line.strip()

        # If line is empty, create a new paragraph
        if not line:
            if len(paragraph) > 0:
                text.append('\n'.join(paragraph))
                paragraph = []
        # If line is a list item, create a new paragraph:
        elif starts_with_list_marker(line):
            if len(paragraph) > 0:
                text.append('\n'.join(paragraph))
                paragraph = []                
            paragraph.append(line)
        # Else, append line to paragraph
        else:
            paragraph.append(line)
    
    if len(paragraph) > 0:
        text.append('\n'.join(paragraph))
        paragraph = []

    return text

def starts_with_list_marker(line):

    # An ordered list marker is a sequence of 1–9 arabic digits (0-9),
    # followed by either a . character or a ) character. 
    # (The reason for the length limit is that with 10 digits GitHub 
    # start seeing integer overflows in some browsers.)

    if line.startswith(('-','+','*')) or re.match(r"\d{1,9}\..*", line) or re.match(r"\d{1,9}\).*", line):
        return True
    else:
        return False


def main():
    file_path  = '/Users/tandanp/Documents/doc_scraper/downloaded_files/test.md'
    markdn2text_gfm(file_path)

if __name__=='__main__':
    main()