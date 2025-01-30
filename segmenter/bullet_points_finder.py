import re
from segmenter.clean_markdown import markdn2text_gfm
# from clean_markdown import markdn2text_gfm

def find_bullet_points(lines):

    # with open(file_path, 'r') as file:
    #     lines = file.readlines()

    bullet_points = []
    bullet_start = None
    bullet_regex = re.compile(r'^\s*[\d\.\-\*\☐]') # Lines starting with numbers, dots, dashes, or asterisks
    indent_regex = re.compile(r'^\s')  # Lines with leading whitespace (indented lines)

    for i, line in enumerate(lines):
        if bullet_regex.match(line):
            if bullet_start is None:
                bullet_start = i
        else:
            if bullet_start is not None:
                if not indent_regex.match(line):
                    bullet_points.append((bullet_start, i - 1))
                    bullet_start = None

    # If the file ends with a bullet point section
    if bullet_start is not None:
        bullet_points.append((bullet_start, len(lines) - 1))

    return bullet_points

def find_tables(lines):
    # with open(file_path, 'r') as file:
        # lines = file.readlines()

    tables = []
    table_start = None
    table_regex = re.compile(r"^\s*\|") # Lines starting (pipes) or (spaces and pipes)

    for i, line in enumerate(lines):
        if table_regex.match(line):
            if table_start is None:
                table_start = i
        else:
            if table_start is not None:
                tables.append((table_start, i - 1))
                table_start = None

    # If the file ends with a table
    if table_start is not None:
        tables.append((table_start, len(lines) - 1))

    return tables

def find_codeblocks(lines):
    # with open(file_path, 'r') as file:
    #         lines = file.readlines()

    codeblocks = []
    code_start = None
    code_start_regex = re.compile(r'^\s*`+') # Lines starting with ticks '`'
    code_end_regex = re.compile(r'`\s*$') # Lines ending with ticks '`'

    for i, line in enumerate(lines):
        if code_start_regex.match(line):
            print("Code start found.")
            if code_start is None:
                code_start = i
        else:
            if code_start is not None:
                if code_end_regex.match(line):
                    codeblocks.append((code_start, i - 1))
                    code_start = None

    # If the file ends with a code block
    if code_start is not None:
        codeblocks.append((code_start, len(lines) - 1))

    return codeblocks

def get_block_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    bullet_points = find_bullet_points(lines)
    print("No of bullet point sections found = ", len(bullet_points))
    for start, end in bullet_points:
        print(f"Bullet point section starts at line {start + 1} and ends at line {end + 1}")

    tables = find_tables(lines)
    print("No of tables found = ", len(tables))
    for start, end in tables:
        print(f"Table starts at line {start + 1} and ends at line {end + 1}")

    codes = find_codeblocks(lines)
    print("No of code blocks found = ", len(codes))
    for start, end in codes:
        print(f"Code starts at line {start + 1} and ends at line {end + 1}")

    blocks = bullet_points + tables + codes
    print("Blocks list= ", blocks)

    smaller_blocks = set()

    #Filter out smaller blocks
    # Iterate over the blocks and check if any block is fully inside another
    for i in range(0, len(blocks)):
        block_1 = blocks[i]

        for j in range(i+1, len(blocks)):
            block_2 = blocks[j]
            # Check if block 1 is fully inside block 2
            if (block_1[0] > block_2[0]) and (block_1[1] < block_2[1]):
                print("Smaller block found. 1")
                smaller_blocks.add(block_1)
            # Check if block 2 is fully inside block 1
            elif (block_2[0] > block_1[0]) and (block_2[1] < block_1[1]):
                smaller_blocks.add(block_2) 
                print("Smaller block found. 2")

        break
    #convert the blocks to set to remove duplicates and also to make the removal of smaller blocks easier later.
    blocks = {tuple(block) for block in blocks}
    print("Blocks set= ", blocks)

    print("Smaller blocks: ", smaller_blocks)

    return blocks-smaller_blocks

def add_block_identifier(file_path, blocks):
    start_block_marker = "THIS IS START BLOCK MARKER."
    end_block_marker = "THIS IS END BLOCK MARKER."

    with open(file_path, 'r') as md_file:
        lines = md_file.readlines()
    
    block_marker_offset = 0
    blocks = sorted(blocks)
    for block in blocks:
        start_line, end_line = block
        lines.insert(start_line + block_marker_offset, start_block_marker + '\n')
        lines.insert(end_line + 2 + block_marker_offset, end_block_marker + '\n')
        block_marker_offset = block_marker_offset + 2


    # Write the modified content back to the markdown file
    with open(file_path, 'w') as md_file:
        md_file.writelines(lines)

def find_block_markers_in_sentences(sentences):
    start_block_marker = "THIS IS START BLOCK MARKER."
    end_block_marker   = "THIS IS END BLOCK MARKER."
    
    new_sentences = []
    block_markers = []
    
    start_block_index = None
    
    for i, sentence in enumerate(sentences):
        # If it *contains* the start marker, remove that substring:
        if start_block_marker in sentence:
            # Record where the block starts in terms of new_sentences
            if start_block_index is None:
                start_block_index = len(new_sentences)
            
            # Remove marker text but keep the rest of the line
            sentence = sentence.replace(start_block_marker, "")
            
            # If there's leftover text, keep it
            stripped_sentence = sentence.strip()
            if stripped_sentence:
                new_sentences.append(stripped_sentence)
        
        # Similarly for end marker
        elif end_block_marker in sentence:
            # Remove marker from the sentence
            sentence = sentence.replace(end_block_marker, "")
            
            # End block index is the last real sentence index we have
            end_block_index = len(new_sentences) - 1
            
            # If we had a start, record the block
            if start_block_index is not None:
                block_markers.append((start_block_index, end_block_index))
                start_block_index = None
            
            stripped_sentence = sentence.strip()
            if stripped_sentence:
                new_sentences.append(stripped_sentence)
        
        else:
            # Normal sentence with no markers
            new_sentences.append(sentence)
    
    return block_markers, new_sentences




def main():
    repo = 'flutter'
    md_file_path = '/Users/tandanp/Documents/doc_scraper/downloaded_files/'+repo+'_contrib.md'
    txt_file_path = '/Users/tandanp/Documents/doc_scraper/segmenter/outputs/parsed_file_'+repo+'.txt'
    markdn2text_gfm(md_file_path, repo)
    # bullet_points = find_bullet_points(txt_file_path)
    # tables = find_tables(txt_file_path)
    # codes = find_codeblocks(txt_file_path)

    blocks = get_block_lines(txt_file_path)
    print("Final blocks: ", blocks)

if __name__ == '__main__':
    main()