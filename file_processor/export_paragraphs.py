#imported from Igor's paper
#https://github.com/fronchetti/FSE-2023/blob/master/scripts/scraper/export.py#L103


import re
import os
import csv
# import xlsxwriter
import subprocess
import markdown # pip install markdown
from bs4 import BeautifulSoup # pip install beautifulsoup4


def create_analysis_file(worksheet_name, raw_filepath, spreadsheet_filepath):
    """Exports documentation files as spreadsheet for qualitative analysis.

    This method receives as input filepaths of documentation files written
    in Markdown and transforms the content of these files into a spreadsheet
    for qualitative analysis. Each file will be represented by a worksheet of
    the spreadsheet, and its' content will be divided paragraphs, in such a way
    that a spreadsheet cell will represent a paragraph, and vice-versa.

    Notice that this method uses cmark-gfm, the official Markdown parser of
    GitHub, to transform the content of the documentation files into plaintext.
    If you don't have cmark-gfm installed, please, follow the official tutorial:
    github.com/github/cmark-gfm/blob/master/README.md

    Args:
        raw_filepaths: A dictionary of strings representing the filepaths of the
        documentation files to be used in the spreadsheet.
        spreadsheet_filepath: A string representing the filepath where the 
        spreadsheet will be saved. 
    """
 
    # workbook = xlsxwriter.Workbook(spreadsheet_filepath)
    workbook = ''
    absolute_path = os.path.abspath(raw_filepath)

    # Redefine this variable with your own filepath to cmark-gfm.exe
    cmark_gfm_exe_path = 'C:\\Users\\fronchettl\\Documents\\cmark-gfm-master\\cmark-gfm-master\\build\\src\\cmark-gfm.exe'

    if os.path.isfile(cmark_gfm_exe_path):
        plaintext = subprocess.run([cmark_gfm_exe_path, absolute_path, '--to', 'plaintext'], stdout=subprocess.PIPE)
    else:
        print('Please, update the filepath to the `cmark-gfm.exe` file inside the scripts/scraper/export.py file')
        print('If you do not have cmark-gfm installed, please visit their repository and install it: github.com/github/cmark-gfm')
        raise ValueError('The cmark-gfm.exe variable was not defined in scripts/scraper/export.py (Line 38)')

    paragraphs = split_into_paragraphs(plaintext.stdout.decode('utf-8'))

    # Creating the worksheet 

    worksheet = workbook.add_worksheet(worksheet_name)

    # In each worksheet we have eight columns. The first column will be
    # used to store the documentation paragraphs in cells. The second
    # to the eigth column will be used during qualitative analysis to 
    # identify the categories of relevant documentation for newcomers.

    # Set up the width of the worksheet columns

    worksheet.set_column(0, 0, 60)
    worksheet.set_column(1, 7, 25)

    # Set up colors and text properties for each column

    default_format = workbook.add_format({'text_wrap': True})
    CF_format = workbook.add_format({'text_wrap': True, 'bg_color': '#ffd966'})
    CT_format = workbook.add_format({'text_wrap': True, 'bg_color': '#b6d7a8'})
    TC_format = workbook.add_format({'text_wrap': True, 'bg_color': '#d9d2e9'})
    BW_format = workbook.add_format({'text_wrap': True, 'bg_color': '#ea9999'})
    DC_format = workbook.add_format({'text_wrap': True, 'bg_color': '#a2c4c9'})
    SC_format = workbook.add_format({'text_wrap': True, 'bg_color': '#f9cb9c'})

    # Write the categories of relevant information for new contributors in
    # the first line of the spreadsheet, from the second to the eight column.

    worksheet.write(0, 1, 'CF   Contribution flow', CF_format)
    worksheet.write(0, 2, 'CT   Choose a task', CT_format)
    worksheet.write(0, 3, 'TC   Talk to the community', TC_format)
    worksheet.write(0, 4, 'BW   Build local workspace', BW_format)
    worksheet.write(0, 5, 'DC   Deal with the code', DC_format)
    worksheet.write(0, 6, 'SC   Submit the changes', SC_format)

    # Write paragraphs in the first column of the worksheet

    for index, paragraph in enumerate(paragraphs):
        worksheet.write(index + 1, 0, paragraph, default_format)

    workbook.close()

def starts_with_list_marker(line):

    # An ordered list marker is a sequence of 1–9 arabic digits (0-9),
    # followed by either a . character or a ) character. 
    # (The reason for the length limit is that with 10 digits GitHub 
    # start seeing integer overflows in some browsers.)

    if line.startswith(('-','+','*')) or re.match(r"\d{1,9}\..*", line) or re.match(r"\d{1,9}\).*", line):
        return True
    else:
        return False

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

def export_to_repositories_file(information, filepath):
    """Exports information about a repository to a spreadsheet file.

    Args:
        repositories: A dictionary containing information about a repository.
        filepath: A string representing the path where the spreadsheet file will be saved.
    """
    if os.path.isfile(filepath):
        with open(filepath, 'a', errors='replace') as writer:
            print("Exporting {}/{} to `repositories.csv`.".format(information['owner'], information['name']))
            fieldnames = information.keys()
            dict_writer = csv.DictWriter(writer, fieldnames)
            dict_writer.writerow(information)
            writer.close()
    else:
        with open(filepath, 'w', errors='replace') as writer:
            print("Exporting {}/{} to `repositories.csv`.".format(information['owner'], information['name']))
            fieldnames = information.keys()
            dict_writer = csv.DictWriter(writer, fieldnames)
            dict_writer.writeheader()
            dict_writer.writerow(information)
            writer.close()    

def md_to_text(md):
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.get_text()

def example():
    # md = '**A** [B](http://example.com) <!-- C -->'
    md  = '''\n\nContributing to Flutter\n=======================\n\n_tl;dr: join Discord, be courteous, follow the steps below to set up a development environment; if you stick around and contribute, you can join the team and get commit access._\n\nWelcome\n-------\n\nWe invite you to join the Flutter team, which is made up of volunteers and sponsored folk alike!\nThere are many ways to contribute, including writing code, filing issues on GitHub, helping people\non our mailing lists, our chat channels, or on Stack Overflow, helping to triage, reproduce, or\nfix bugs that people have filed, adding to our documentation,\ndoing outreach about Flutter, or helping out in any other way.\n\nWe grant commit access (which includes full rights to the issue\ndatabase, such as being able to edit labels) to people who have gained\nour trust and demonstrated a commitment to Flutter. For more details\nsee the Contributor access\npage on our wiki.\n\nWe communicate primarily over GitHub and Discord.\n\nBefore you get started, we encourage you to read these documents which describe some of our community norms:\n\n1. Our code of conduct, which stipulates explicitly\n   that everyone must be gracious, respectful, and professional. This\n   also documents our conflict resolution policy and encourages people\n   to ask questions.\n\n2. Values,\n   which talks about what we care most about.\n\nHelping out in the issue database\n---------------------------------\n\nTriage is the process of going through bug reports and determining if they are valid, finding out\nhow to reproduce them, catching duplicate reports, and generally making our issues list\nuseful for our engineers.\n\nIf you want to help us triage, you are very welcome to do so!\n\n1. Join the #hackers-triage Discord channel.\n\n2. Read our code of conduct, which stipulates explicitly\n   that everyone must be gracious, respectful, and professional. If you\'re helping out\n   with triage, you are representing the Flutter team, and so you want to make sure to\n   make a good impression!\n\n3. Help out as described in our wiki: https://github.com/flutter/flutter/wiki/Triage\n   You won\'t be able to add labels at first, so instead start by trying to\n   do the other steps, e.g. trying to reproduce the problem and asking for people to\n   provide enough details that you can reproduce the problem, pointing out duplicates,\n   and so on. Chat on the #hackers-triage channel to let us know what you\'re up to!\n\n4. Familiarize yourself with our\n   issue hygiene wiki page,\n   which covers the meanings of some important GitHub labels and\n   milestones.\n\n5. Once you\'ve been doing this for a while, someone will invite you to the flutter-hackers\n   team on GitHub and you\'ll be able to add labels too. See the\n   contributor access wiki\n   page for details.\n\n\nQuality Assurance\n-----------------\n\nOne of the most useful tasks, closely related to triage, is finding and filing bug reports. Testing\nbeta releases, looking for regressions, creating test cases, adding to our test suites, and\nother work along these lines can really drive the quality of the product up. Creating tests\nthat increase our test coverage, writing tests for issues others have filed, all these tasks\nare really valuable contributions to open source projects.\n\nIf this interests you, you can jump in and submit bug reports without needing anyone\'s permission!\nThe #quality-assurance channel on our Discord server\nis a good place to talk about what you\'re doing. We\'re especially eager for QA testing when\nwe announce a beta release. See https://github.com/flutter/flutter/wiki/Quality-Assurance for\nmore details.\n\nIf you want to contribute test cases, you can also submit PRs. See the next section\nfor how to set up your development environment, or ask in #hackers-test on Discord.\n\n> As a personal side note, this is exactly the kind of work that first got me into open\n> source. I was a Quality Assurance volunteer on the Mozilla project, writing test cases for\n> browsers, long before I wrote a line of code for any open source project. \xe2\x80\x94Hixie\n\n\nDeveloping for Flutter\n----------------------\n\nIf you would prefer to write code, you may wish to start with our list of good first issues for Flutter or for Flutter DevTools. See the respective sections below for further instructions.\n\n### Framework and Engine\n\nTo develop for Flutter, you will eventually need to become familiar\nwith our processes and conventions. This section lists the documents\nthat describe these methodologies. The following list is ordered: you\nare strongly recommended to go through these documents in the order\npresented.\n\n1. Setting up your engine development environment,\n   which describes the steps you need to configure your computer to\n   work on Flutter\'s engine. If you only want to write code for the\n   Flutter framework, you can skip this step. Flutter\'s engine mainly\n   uses C++, Java, and Objective-C.\n\n2. Setting up your framework development environment,\n   which describes the steps you need to configure your computer to\n   work on Flutter\'s framework. Flutter\'s framework mainly uses Dart.\n\n3. Tree hygiene,\n   which covers how to land a PR, how to do code review, how to\n   handle breaking changes, how to handle regressions, and how to\n   handle post-commit test failures.\n\n4. Our style guide,\n   which includes advice for designing APIs for Flutter, and how to\n   format code in the framework.\n\n5. Flutter design doc template,\n   which should be used when proposing a new technical design.  This is a good\n   practice to do before coding more intricate changes.\n   See also our guidance for writing design docs.\n\n\n\nIn addition to the documents, there is a video linked above on How to contribute to Flutter\nfrom the Flutter YouTube channel,\nthere are many pages on our Wiki,\nand an article Contributing to Flutter: Getting Started\non Medium that may be of interest. For a curated list of pages see the sidebar\non the wiki\'s home page. They are more or less listed in order of importance.\n\n### DevTools\n\nContributing code to Dart & Flutter DevTools may be a good place to start if you are\nlooking to dip your toes into contributing with a relatively low-cost setup or if you\nare generally excited about improving the Dart & Flutter developer experience.\n\nPlease see the DevTools CONTRIBUTING.md\nguide to get started.\n\nOutreach\n--------\n\nIf your interests lie in the direction of developer relations and developer outreach,\nwhether advocating for Flutter, answering questions in fora like\nStack Overflow\nor Reddit,\nor creating content for our documentation\nor sites like YouTube,\nthe best starting point is to join the #hackers-devrel Discord channel.\nFrom there, you can describe what you\'re interested in doing, and go ahead and do it!\nAs others become familiar with your work, they may have feedback, be interested in\ncollaborating, or want to coordinate their efforts with yours.\n\n\nAPI documentation\n-----------------\n\nAnother great area to contribute in is sample code and API documentation. If this is an area that interests you, join our\nDiscord server and introduce yourself on the #hackers-deverl, #hackers-framework,\nor #hackers-engine channels, describing your area of interest. As our API docs are integrated into our source code, see the\n"developing for Flutter" section above for a guide on how to set up your developer environment.\n\nTo contribute API documentation, an excellent command of the English language is particularly helpful, as is a careful attention to detail.\nWe have a whole section in our style guide\nthat you should read before you write API documentation. It includes notes on the "Flutter Voice", such as our word and grammar conventions.\n\nIn general, a really productive way to improve documentation is to use Flutter and stop any time you have a question: find the answer, then\ndocument the answer where you first looked for it.\n\nWe also keep a list of areas that need better API documentation.\nIn many cases, we have written down what needs to be said in the relevant issue, we just haven\'t gotten around to doing it!\n\nWe\'re especially eager to add sample code and diagrams to our API documentation. Diagrams are generated from Flutter code that\ndraws to a canvas, and stored in a special repository. It can be a lot of fun\nto create new diagrams for the API docs.\n\n\nReleases\n--------\n\nIf you are interested in participating in our release process, which may involve writing release notes and blog posts, coordinating the actual\ngeneration of binaries, updating our release tooling, and other work of that nature, then reach out on the #hackers-releases\nchannel of our Discord server.\n\n\nSocial events in the contributor community\n------------------------------------------\n\nFinally, one area where you could have a lot of impact is in contributing to social interactions among the Flutter contributor community itself.\nThis could take the form of organizing weekly video chats on our Discord, or planning tech talks from contributors, for example.\nIf this is an area that is of interest to you, please join our Discord and ping Hixie on the #hackers\nchannel!\n'''
    print(type(md))
    text = md_to_text(md)
    print(text)
    # Output: A B

def markdn2text_gfm(md_file = '/Users/tandanp/Documents/doc_scraper/contributing.md'):
    absolute_path = md_file

    # Redefine this variable with your own filepath to cmark-gfm.exe
    # cmark_gfm_exe_path = 'C:\\Users\\fronchettl\\Documents\\cmark-gfm-master\\cmark-gfm-master\\build\\src\\cmark-gfm.exe'
    cmark_gfm_exe_path = '/Users/tandanp/Documents/doc_scraper/contributing.md'
    if os.path.isfile(cmark_gfm_exe_path):
        plaintext = subprocess.run(['cmark-gfm', absolute_path, '--to', 'plaintext'], stdout=subprocess.PIPE)
    else:
        print('Please, update the filepath to the `cmark-gfm.exe` file inside the scripts/scraper/export.py file')
        print('If you do not have cmark-gfm installed, please visit their repository and install it: github.com/github/cmark-gfm')
        raise ValueError('The cmark-gfm.exe variable was not defined in scripts/scraper/export.py (Line 38)')

    paragraphs = split_into_paragraphs(plaintext.stdout.decode('utf-8'))

    return paragraphs

def print_paragraphs(paragraphs):
    '''
    Print the paragraph in such format that I can copy/paste them directly in colab.
    '''


def main():
    # md_file = './contrib.md'
    txt_file = 'contrib.txt'
    # with open(md_file,'r') as md_file:
    #     md_content = md_file.read()
    #     # lines = my_file.readlines()
    #     # md_content = ''.join(lines)


    # print(type(md_content))
    # # txt_content = md_to_text(md_content)
    # # txt_content = markdown_to_text(md_content)
    # txt_content = markdown_to_text('''\n\nContributing to Flutter\n=======================\n\n_tl;dr: join Discord''')
    # print(txt_content)
    # paragraphs = split_into_paragraphs(txt_content)
    paragraphs = markdn2text_gfm()
    print("No of paragraphs = ", len(paragraphs))
    para_list = []
    for idx, paragraph in enumerate(paragraphs):
        # print("\n\n----------------------------<NEW PARAGRAPH>---------------------\n\n")
        print(f"para{idx} = '{paragraph}'\n")
        # txt_file.write(f"para_{idx} = '''{paragraph}'''\n\n")
        para_list.append(paragraph)

    txt_file = open(txt_file,'w')
    txt_file.write(str(para_list))
    txt_file.close()

if __name__ == '__main__':
    main()
    # example()