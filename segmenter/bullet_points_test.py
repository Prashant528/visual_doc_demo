import re
from clean_markdown import markdn2text_gfm

def find_bullet_points(file_path):

    with open(file_path, 'r') as file:
        lines = file.readlines()

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

# Usage
repo = 'transformers'
md_file_path = '/Users/tandanp/Documents/doc_scraper/downloaded_files/'+repo+'_contrib.md'
txt_file_path = '/Users/tandanp/Documents/doc_scraper/segmenter/outputs/parsed_file_'+repo+'.txt'
markdn2text_gfm(md_file_path, repo)
bullet_points = find_bullet_points(txt_file_path)
print("No of sections found = ", len(bullet_points))
for start, end in bullet_points:
    print(f"Bullet point section starts at line {start + 1} and ends at line {end + 1}")
