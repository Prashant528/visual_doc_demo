import markdown
from xml.etree.ElementTree import tostring

text = """
# Heading

Some **bold** text and [a link](https://example.com).
"""

# Create a Markdown instance with extensions (if needed)
md = markdown.Markdown(extensions=[])

# Convert the Markdown text to HTML to trigger parsing
html_output = md.convert(text)

# Access the ElementTree object that was used internally
tree = md.parser.parseDocument(text.splitlines()).getroot()

# Print the tree as XML
# print(tostring(tree, encoding="unicode"))

def print_tree(element, level=0):
    indent = "  " * level
    # print(f"{indent}<{element.tag}> text={element.text!r}")
    if element.text:
        print(f"{indent}{element.text!r}")
    for child in element:
        print_tree(child, level + 1)

print_tree(tree)
