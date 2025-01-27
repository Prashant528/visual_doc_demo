from cmarkgfm import github_flavored_markdown_to_html
from bs4 import BeautifulSoup

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
    return plain_text.strip()

# Read the Markdown file
with open("./test_segmenter/markdown_parsers/node.md", "r", encoding="utf-8") as f:
    markdown_content = f.read()

# Convert to plain text while preserving links
plain_text_with_links = markdown_to_plain_text_with_links(markdown_content)

# Output the result
print(plain_text_with_links)

# Optionally, save the plain text to a file
with open("./test_segmenter/markdown_parsers/output.txt", "w", encoding="utf-8") as f:
    f.write(plain_text_with_links)

