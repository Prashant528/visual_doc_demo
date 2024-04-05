from api_stub import api_stub
from scrape_website import extract_webpage_content
from utils import download_file

def get_final_graph(file, content, owner, repo, max_levels=3,all_graphs = []):  
    if max_levels==1:
        return all_graphs  

    main_doc_data = api_stub(file, content)
    #add the graph to all_graphs
    print("Appending new graph:", main_doc_data['Graph'])
    all_graphs.append(main_doc_data['Graph'])
    # print("Graphs state: ", all_graphs)

    for subheader in main_doc_data['Subheaders']:
        #process the links
        subheader_data = main_doc_data['Subheaders'][subheader]
        sub_header_links = subheader_data['links']
        for title in sub_header_links:
            link = sub_header_links[title]
            print(f"Checking for link: ", link)
            if "wiki" in link:
                new_file = link
                print(new_file)
                #commenting below line for testing purposes, need that in original code
                # new_content =  extract_webpage_content(link)
                new_content = ''
                print(new_content)
                return get_final_graph(new_file, new_content, owner, repo, max_levels-1, all_graphs)
                
            elif ".md" in link:
                # may need code to extract the filepath from the link for md files, kept dummy for now
                new_file = link
                print(new_file)
                #commenting below line for testing purposes, need that in original code
                # new_content =  download_file(owner, repo, new_file)
                new_content = ''
                print(new_content)
                return get_final_graph(new_file, new_content, owner, repo, max_levels-1, all_graphs)
            
    return all_graphs

if __name__ == "__main__":
    final_graph = get_final_graph('CONTRIBUTING.md', '', 'flutter', 'flutter')
    print(final_graph)