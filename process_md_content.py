def extract_headings_and_text(md_file):
    with open(md_file, 'r') as file:
        content = file.read()
    #need to add \nEnd\n--- to content to make the later code succint. Last title we find don't need to be accounted.
    content += "\\nEnd\\n----"
    print(content)
    underline_indices = []
    newline_character_indices = []
    looked_upto_index = 0

    while content.find("\\n---", looked_upto_index) != -1:
        #Find the first underline
        first_underline_index = content.find("\\n---", looked_upto_index)
        underline_indices.append(first_underline_index)
        print(first_underline_index)
        #Find the newline before the underline.
        newline_character_index = content.rfind('\\n', 0, first_underline_index)
        newline_character_indices.append(newline_character_index)

        #need to ignore the content upto the found \n--- character so that we don't get into an infinite loop
        looked_upto_index = first_underline_index+3
        # print(content[looked_upto_index:])

    print(len(newline_character_indices))
    print(len(underline_indices))

    headings = []
    texts = []
    for i in range(len(underline_indices)-1):
        #Get the heading
        heading_start = newline_character_indices[i]
        heading_end = underline_indices[i]
        headings.append(content[heading_start:heading_end])
        print(content[heading_start:heading_end])
        #Get the text under that heading
        text_start = underline_indices[i]
        text_end = newline_character_indices[i+1]
        texts.append(content[text_start:text_end])
        print(content[text_start:text_end])
    
    #return two lists of headings and texts. Can be matched by indices. 
    #e.g. headings[0] is the heading of texts[0].
    return headings, texts


md_file = 'contrib.md'
extract_headings_and_text(md_file)
