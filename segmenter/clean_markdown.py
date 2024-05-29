import re
import os
import csv
# import xlsxwriter
import subprocess

def markdn2text_gfm(md_file = '/Users/tandanp/Documents/doc_scraper/contributing.md'):
    absolute_path = md_file

    # Redefine this variable with your own filepath to cmark-gfm.exe
    # cmark_gfm_exe_path = 'C:\\Users\\fronchettl\\Documents\\cmark-gfm-master\\cmark-gfm-master\\build\\src\\cmark-gfm.exe'
    cmark_gfm_exe_path = '/Users/tandanp/Documents/NLP_test_projects/cmark-gfm/build/src/cmark-gfm'
    if os.path.isfile(cmark_gfm_exe_path):
        plaintext = subprocess.run(['cmark-gfm', absolute_path, '--to', 'plaintext'], stdout=subprocess.PIPE)
    else:
        print('Please, update the filepath to the `cmark-gfm.exe` file inside the scripts/scraper/export.py file')
        print('If you do not have cmark-gfm installed, please visit their repository and install it: github.com/github/cmark-gfm')
        raise ValueError('The cmark-gfm.exe variable was not defined in scripts/scraper/export.py (Line 38)')

    paragraphs = split_into_paragraphs(plaintext.stdout.decode('utf-8'))

    return paragraphs


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