while content.find("\\n---", first_underline_index+4, -1):
        #Extracting the text after the heading
        next_underline_index = content.find("\\n---", first_underline_index+4, -1)
        #Find the newline before the underline.
        newline_character_index = content.rfind('\\n', first_underline_index, next_underline_index)
        new_heading = content[newline_character_index+2:next_underline_index]
        print(new_heading)
        #Now, we can get the text content of the previous heading
        prev_text_content = content[first_underline_index:newline_character_index]
        print(prev_text_content)

        #replace the variables for next iteration
        first_underline_index = next_underline_index
        #need to remove the previous section so that we don't get into an infinite loop
        content = content[newline_character_index:]