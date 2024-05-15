import re

def extract_headings_and_text(md_file):
    with open(md_file, 'r') as file:
        content = file.read()
    #need to add \nEnd\n--- to content to make the later code succint. Last title we find don't need to be accounted.
    content += "\\nEnd\\n----"
    # print(content)
    underline_indices = []
    newline_character_indices = []
    looked_upto_index = 0

    while content.find("\\n---", looked_upto_index) != -1:
        #Find the first underline
        first_underline_index = content.find("\\n---", looked_upto_index)
        underline_indices.append(first_underline_index)
        # print(first_underline_index)
        #Find the newline before the underline.
        newline_character_index = content.rfind('\\n', 0, first_underline_index)
        newline_character_indices.append(newline_character_index)

        #need to ignore the content upto the found \n--- character so that we don't get into an infinite loop
        looked_upto_index = first_underline_index+3
        # print(content[looked_upto_index:])

    # print(len(newline_character_indices))
    # print(len(underline_indices))

    headings = []
    texts = []
    for i in range(len(underline_indices)-1):
        #Get the heading
        heading_start = newline_character_indices[i]
        heading_end = underline_indices[i]
        headings.append(content[heading_start:heading_end])
        # print(content[heading_start:heading_end])
        #Get the text under that heading
        text_start = underline_indices[i]
        text_end = newline_character_indices[i+1]
        texts.append(content[text_start:text_end])
        # print(content[text_start:text_end])
    
    #return two lists of headings and texts. Can be matched by indices. 
    #e.g. headings[0] is the heading of texts[0].
    return headings, texts


def extract_links(text):
    # Example string
    # text = "We communicate primarily over [Discord](https://github.com/flutter/flutter/wiki/Chat) and [GitHub](https://github.com/flutter/flutter/wiki/Contributor-access)."
    looked_upto_index = 0
    link_titles = [] 
    links = []
    while text.find("https://", looked_upto_index) != -1:
        ######Finding the link
        #Find the https
        https_index = text.find("https://", looked_upto_index)
        #Find the first closing bracket from https://
        closing_bracket_index = text.find(")", https_index)
        #The link will be in between the above two indices
        link = text[https_index:closing_bracket_index]
        links.append(link)
        # print(link)

        #######Finding the link title
        #Finding the opening square bracket index
        open_square_brkt_index = text.rfind("[", 0, https_index)
        #Finding the closing square bracket index
        close_square_brkt_index = text.find("]", open_square_brkt_index)
        #The link title will be in between these above two indices
        link_title = text[open_square_brkt_index+1:close_square_brkt_index]
        link_titles.append(link_title)
        # print(link_title)

        #update the looked upto index to the closing ')' bracket.
        looked_upto_index = closing_bracket_index
    
    return link_titles, links


md_file = 'contrib.md'
# extract_links("[Values](https://github.com/flutter/flutter/wiki/Values),\n   which talks about what we care most about.\n\nHelping out in the issue database\n---------------------------------\n\nTriage is the process of going through bug reports and determining if they are valid, finding out\nhow to reproduce them, catching duplicate reports, and generally making our issues list\nuseful for our engineers.\n\nIf you want to help us triage, you are very welcome to do so!\n\n1. Join the #hackers-triage [Discord channel](https://github.com/flutter/flutter/wiki/Chat).\n\n2. Read [our code of conduct](CODE_OF_CONDUCT.md)")
headings, text = extract_headings_and_text(md_file)

for h, t in zip(headings, text):
    print(h)
    # print('----------')
    print(t)