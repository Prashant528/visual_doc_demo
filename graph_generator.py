from api_stub import api_stub
from scrape_website import extract_webpage_content

def get_final_graph(file, content, levels=3):
    main_doc_data = api_stub(file, content)
    
    if levels==0:
        return main_doc_data['Graph']
    # api_stub('CONTRIBUTING.md')

    for subheader in main_doc_data['Subheaders']:
        subheader_data = main_doc_data['Subheaders'][subheader]
        sub_header_links = subheader_data['links']
        for title in sub_header_links:
            link = sub_header_links[title]
            print(f"Checking for link: ", link)
            if "wiki" in link or ".md" in link:
                new_doc = title
                print(new_doc)
                new_content =  extract_webpage_content(link)
                print(new_content)
                #return [['Graph']] + get_final_graph(new_doc, new_content, levels-1)