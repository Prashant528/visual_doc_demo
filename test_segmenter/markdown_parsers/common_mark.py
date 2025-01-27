from commonmark import Parser

# Example Markdown text
text = """
# Heading 1

This is a **bold** statement and [a link](https://example.com).

## Heading 2

1. First item
2. Second item with *italic* text.
"""

# Initialize the CommonMark parser
parser = Parser()

# Parse the Markdown text into an abstract syntax tree (AST)
ast = parser.parse(text)

# Function to traverse and display the AST
def print_ast(node, level=0):
    indent = "    " * level
    print(f"{indent}- type: {node.t}")  # Node type (e.g., 'heading', 'paragraph', 'text', etc.)

    # Print literal content if available (e.g., for 'text' nodes)
    if hasattr(node, 'literal') and node.literal:
        print(f"{indent}  literal: {node.literal!r}")

    # Print the heading level if it's a heading
    if node.t == 'heading':
        print(f"{indent}  level: {node.level}")

    # Traverse child nodes
    child = node.first_child
    while child:
        print_ast(child, level + 1)
        child = child.nxt

# Print the AST
print_ast(ast)
