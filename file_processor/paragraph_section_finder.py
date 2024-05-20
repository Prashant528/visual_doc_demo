'''
Extracts the paragraphs from the docs given in the file corpus.py and dumps them to a text file . 
Also prints out the section(segment) indices. i.e. indices of those paragraphs where there's a new segment.
Uses corpus.py as a baseline for sections. i.e. corpus should have sections as a list(I did this manually).
'''

from corpus import corpus
from export_paragraphs import markdn2text_gfm, split_into_paragraphs
import markdown
from bs4 import BeautifulSoup

def md_to_text(md):
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.get_text()

def get_paragraphs_from_corpus():
    para_corpus = []
    para_section_indices_ground= []
    for doc in corpus:
        #sad but the parser needs a file
        tmp_file = open("temp.md", 'w')
        tmp_file.write(doc)
        tmp_file.close()
        paragraphs = markdn2text_gfm('temp.md')
        #try the md_to_text parser and see it matches the gfm. => Didn't match so commented out.
        # text = md_to_text(doc)
        # print(text)
        # paragraphs = split_into_paragraphs(text)
        #try comment end
        for paragraph in paragraphs:
            para_corpus.append(paragraph)
            # print("-------------------")
            # print(paragraph)
        para_section_indices_ground.append(len(para_corpus))
        
    txt_file = open('./file_processor/outfiles/paragraphs.txt','w')
    txt_file.write(str(para_corpus))
    txt_file.close()
    print("Length of paragraphs(should be 101) = ", len(para_corpus))

    return para_section_indices_ground

print(get_paragraphs_from_corpus())
print("No of segments = ",len(get_paragraphs_from_corpus()))

