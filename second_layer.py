from flask import jsonify
from scrape_website import save_to_md
from segmenter.segment import segment
from flask_cors import CORS
from code_from_visdoc.github_service import GitHubService
from code_from_visdoc.openai_service import OpenAIService
from code_from_visdoc.config import Config
from code_from_visdoc.utils import parse_openai_single_json
from code_from_visdoc.github_link_parser import parse_github_url
from segmenter.transformers_call import SentenceFeatureExtractor
import json
import copy
from datetime import datetime
import os, requests
from utils import save_llm_output

def process_md_and_wiki(topic, link, data, github_service, github_url_components, custom_file_path=None):
    """
    Dummy function to process .md or .wiki links.
    """

    print(f"Processing MD/WIKI link: {link}")

    clean_link = link.split('#')[0].split('?')[0]
    content_from_link = None
    if clean_link.endswith(".md"):
        print(f"Processing MD filepath: {github_url_components.filepath}")
        content_from_link = get_new_nodes_from_md(link, github_service, github_url_components, custom_file_path=custom_file_path)
        print("Fetching content_from_link successful.")

    elif clean_link.endswith(".wiki"):
        print(f"Processing wiki link: {link}")
        content_from_link =  get_new_nodes_from_wiki(link, github_service, github_url_components)

    elif '/tree/' in clean_link and 'github.com' in clean_link:
        print(f"Processing file inside another folder: {link}")
        content_from_link =  get_new_nodes_from_md(link, github_service, github_url_components, custom_file_path=custom_file_path)

    else:
        print("Link is outbound to other pages than current repository.")
    
    return content_from_link

def get_new_nodes_from_md(link, github_service, github_url_components, custom_file_path=None):
    '''
    Get all the segments from the file like in app.py.
    '''
    owner = github_url_components.owner
    repo = github_url_components.name
    if custom_file_path:
        file_path = custom_file_path
    else:
        file_path = github_url_components.filepath
    print(owner, repo, file_path)
    if not owner or not repo or not file_path:
        return jsonify({"error": "The link doesn't contain one or many of these (owner, repo, file)."}), 400
    
    openai_service = OpenAIService(Config.OPENAI_API_KEY, repo)
    sentence_feature_extractor = SentenceFeatureExtractor()
    files_and_contents = github_service.download_recursive(owner, repo, file_path)
    if files_and_contents:
        file_and_content = files_and_contents[0]

        file_name = repo + '_' + file_and_content[0].split('/')[-1]
        content = file_and_content[1]
        md_file_path = save_to_md(content, file_name)

        predicted_segmentation, segments, segmented_file_path  = segment(sentence_feature_extractor, md_file_path, openai_service, file_name,  segmentation_method='langchain', sentence_method= 'stanza', save_to_file=True, repo=repo, filename=file_path)

        prompt_for_llm = 'PROMPT_FOR_SEQUENCING_SECOND_LAYER'

        #Call the LLM to find the sequence
        prompt = copy.deepcopy(openai_service.fetch_prompt(prompt_for_llm))

        for item in prompt:
                if item["role"] == "user":
                    item["content"] += str(segments)

        with open('llm_prompt.txt', 'w') as outfile:
            outfile.write(str(prompt))
        # print(full_prompt_with_segments)
        llm_result = parse_openai_single_json(openai_service.get_llm_response_json(prompt))
        # print(f"\nActual response from API:\n {segments_flow_and_contents}")
        return llm_result
    else:
        return None
    
def get_new_nodes_from_wiki(link, github_service, github_url_components):
    '''
    Get all the segments from the file like in app.py.
    '''
    pass


def add_second_layer_from_links(data, file_path, github_url_components):
    """
    Post-process the links after they have been extracted.
    1. If link ends with '.md' or '.wiki', call `process_md_and_wiki()`.
    2. Otherwise (external link), add it to 'content' under a new topic 
       'Outbound Link #<counter>', and append a new edge to 'flow'.
    """
    print("Current filepath = ", file_path)
    github_service = GitHubService(Config.GITHUB_TOKEN)

    outbound_link_counter = 1  # to label outbound links uniquely
    #dictionary to cache already processed links and their contents
    processed_links = {}

    #If there are no links, the data would be the final result
    merged_json = data

    print("\n\n LINKS in the first file:")
    print(len(data["links"]))

    # Iterate over each topic and its list of extracted links
    for topic, links_list in data.get("links", {}).items():
        print("Second page started...")
        print("Processing for topic: ", topic)
        topic_links = []
        for link in links_list:
            # We check the portion before possible '#' or query params
            # to see if it ends with .md or .wiki
            clean_link = link.split('#')[0].split('?')[0]

            if clean_link.endswith(".md") or clean_link.endswith(".wiki") or ('/tree/' in clean_link and 'github.com' in clean_link):
                topic_links.append(clean_link)

            else:
                # Increment our counter for the next external link
                outbound_link_counter += 1
            
        #now process the unique links in each topic
        uniq_topic_links = list(set(topic_links))
        print("Links in the topic: ", uniq_topic_links)
        #if there is a link to the same page(different element), remove that too.
        if file_path in topic_links:
            topic_links.remove(file_path)
        for clean_link in uniq_topic_links:
            print("Processing for link : ", clean_link)
            content_from_link = None
            if clean_link in processed_links:  # If the link has already been processed
                print(f"Reusing cached content for {clean_link}")
                content_from_link = processed_links[clean_link]
                print(content_from_link)
                attach_second_layer(data, content_from_link, topic, clean_link)

            else:
                if clean_link.startswith(('http://', 'https://')):
                    # If the link is an absolute URL, add it directly
                    print("Absolute link found")
                    # github_url_components = parse_github_url(link)
                    # print(clean_link)
                    # # print(github_url_components)
                    # content_from_link  = process_md_and_wiki(topic, clean_link, data, github_service, github_url_components)
                    
                    #If the link takes us to a github tree, get the md files from the tree
                    if '/tree/' in clean_link and 'github.com' in clean_link:
                        #handle templates differently
                        if 'templates' in clean_link:
                            print("Processing templates")
                            template_directory = clean_link.split('/')[-1]
                            template_dir_url = get_directory_url(template_directory, github_url_components)
                            dir_paths = get_child_dirs(template_dir_url)
                            for dir in dir_paths:
                                directory_url  = get_directory_url(dir, github_url_components)
                                file_paths = get_file_urls_from_dir(directory_url)
                                for file_pathe in file_paths:
                                    if file_pathe.endswith(".md"):
                                        print("Found a md file inside templates folder:", file_pathe)
                                        # github_url_components.filepath = file_path
                                        content_from_link = process_md_and_wiki(topic, clean_link, data, github_service, github_url_components, custom_file_path = file_pathe)    
                                        # print(content_from_link)
                                        attach_second_layer(data, content_from_link, topic, file_pathe)



                        #handle docs (non-templates) differently
                        else:
                            print("Processing other docs")
                            directory = clean_link.split('/')[-1]
                            dir_url = get_directory_url(directory, github_url_components)
                            file_paths = get_file_urls_from_dir(dir_url)
                            for file_pathe in file_paths:
                                if file_pathe.endswith(".md"):
                                    # github_url_components.filepath = file_path
                                    content_from_link = process_md_and_wiki(topic, clean_link, data, github_service, github_url_components, custom_file_path = file_pathe)    
                                    # print(content_from_link)
                                    attach_second_layer(data, content_from_link, topic, file_pathe)
                    


                else:
                    print("Relative link found")
                    # Otherwise, add it to relative links
                    new_link = github_service.create_new_filepath(file_path, clean_link)
                    github_url_components.filepath = new_link
                    print(new_link)
                    # print(github_url_components)
                    content_from_link = process_md_and_wiki(topic, new_link, data, github_service, github_url_components)                       
                    print(content_from_link)
                    # Store processed content in cache
                    processed_links[clean_link] = content_from_link
                    attach_second_layer(data, content_from_link, topic, clean_link)
            

    return data


def rename_duplicate_topics(data, second_layer_nodes):
    """
    Ensures no topics in second_layer_nodes['content'] duplicate each other
    or any existing topics in data['content'].
    
    If a collision is found, the duplicate second-layer topic is renamed with a #<counter> suffix.
    
    This updates second_layer_nodes in place (both 'content' keys and 'flow' edges).
    """

    # 1. Build a set of all existing topics from data
    existing_topics = set(data["content"].keys())

    # 2. Create a rename map for any second-layer topics
    rename_map = {}
    
    # We'll gather all second-layer topics in a list so we can iterate deterministically
    second_layer_topic_names = list(second_layer_nodes["content"].keys())

    for old_topic in second_layer_topic_names:
        # If we've not processed this old_topic yet:
        if old_topic not in rename_map:
            if old_topic in existing_topics:
                # We must generate a unique new topic name
                i = 1
                new_topic = f"{old_topic}#{i}"
                while new_topic in existing_topics:
                    i += 1
                    new_topic = f"{old_topic}#{i}"
                
                rename_map[old_topic] = new_topic
                existing_topics.add(new_topic)
            else:
                # The topic is new overall; keep it as-is
                rename_map[old_topic] = old_topic
                existing_topics.add(old_topic)

    # 3. Rename 'content' keys in second_layer_nodes
    new_content = {}
    for old_topic, text in second_layer_nodes["content"].items():
        new_content[rename_map[old_topic]] = text
    second_layer_nodes["content"] = new_content

    # 4. Update edges in second_layer_nodes['flow'] to reflect any renamed topics
    if "flow" in second_layer_nodes:
        flow_value = second_layer_nodes["flow"]
        # If it's a single dict, wrap it in a list to iterate
        if isinstance(flow_value, dict):
            flow_items = [flow_value]
        else:
            flow_items = flow_value

        for flow_item in flow_items:
            edges = flow_item.get("edges", [])
            for edge in edges:
                if edge["source"] in rename_map:
                    edge["source"] = rename_map[edge["source"]]
                if edge["target"] in rename_map:
                    edge["target"] = rename_map[edge["target"]]

        # Put them back if needed
        if isinstance(flow_value, dict):
            second_layer_nodes["flow"] = flow_items[0]
        else:
            second_layer_nodes["flow"] = flow_items


def attach_second_layer(data, second_layer_nodes, topic, link):
    """
    Merges second_layer_nodes into data so that:
      1) second_layer_nodes["content"] entries are merged into data["content"].
      2) All new edges are placed in the flow item with the same sequence as the parent topic.
      3) The 'first node' in second_layer_nodes is linked as a child of 'topic' in data.
      4) No duplicate topics remain in the final structure (renamed if necessary).
    """

    # A) Rename duplicates in second_layer_nodes to avoid conflicts
    rename_duplicate_topics(data, second_layer_nodes)

    # B) Merge the second-layer content into data
    data["content"].update(second_layer_nodes.get("content", {}))

    # C) Prepare second-layer flow as a list
    flow_value = second_layer_nodes.get("flow", [])
    if isinstance(flow_value, dict):
        flow_items = [flow_value]
    else:
        flow_items = flow_value

    if not flow_items:
        # No flow to attach
        print("Found no flow to attach.")
        return data

    print("Attaching flow from second layer")
    # print("Flow from the file (second layer): ", flow_items)
    # Identify the 'first node' in second_layer_nodes (assume it's the source of the first edge)
    first_flow_item = flow_items[0]
    first_edges = first_flow_item.get("edges", [])
    if not first_edges:
        print("Found no edges")
        return data  # No edges, nothing to attach

    first_node = first_edges[0]["source"]

    # D) Find the flow item in data with the same sequence as the parent topic
    topic_sequence = None
    parent_flow_item = None
    for flow_item in data["flow"]:
        if any(edge["source"] == topic or edge["target"] == topic for edge in flow_item["edges"]):
            topic_sequence = flow_item.get("sequence")
            parent_flow_item = flow_item
            break  # ← Ensure we stop once we find the correct sequence

    if topic_sequence is None:
        # If no matching sequence, default to a new sequence
        topic_sequence = "Attached second layer"

    # E) Ensure we have a parent flow item to append to
    if not parent_flow_item:
        # If no parent flow item matches, create a new one
        parent_flow_item = {"edges": [], "sequence": topic_sequence}
        data["flow"].append(parent_flow_item)

    # F) Add the bridging edge (topic -> first_node) to the parent flow item
    bridging_edge = {"source": topic, "target": first_node, "edge_label": link}
    parent_flow_item["edges"].append(bridging_edge)

    # G) **Fix: Append second-layer edges correctly**
    label_added = False
    for item in flow_items:
        for edge in item.get("edges", []):
            edge_with_label = {
                "source": edge["source"],
                "target": edge["target"],
            }
            if not label_added:
                edge_with_label["edge_label"] = link  # Add edge label to the first edge
                label_added = True  
            parent_flow_item["edges"].append(edge_with_label)  # **Fix: Append the updated edge**

    # H) Save the updated data to a file (optional)
    # saved_filename = "second_layer_merged_data" + link + ".json"
    # with open("second_layer_merged_data.json", "w") as f:
    #     json.dump(data, f, indent=4)
    file_prefix = "second_layer_merged_data" + topic
    save_llm_output(data, file_prefix)

    return data


def get_directory_url(dir, github_url_components):
    base_url = 'https://api.github.com/repos/'
    base_url = base_url + github_url_components.owner + '/' + github_url_components.name + '/contents/'
    file_url = base_url + dir
    return file_url


def get_file_urls_from_dir(dir_url):
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(dir_url, headers=headers)

    if response.status_code == 200:
        files = [file["path"] for file in response.json() if file["type"]=="file"]
        print("Files in the folder:", files)
    else:
        print("Failed to retrieve files. Status Code:", response.status_code, response.json())
    return files

def get_child_dirs(dir_url):
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(dir_url, headers=headers)

    if response.status_code == 200:
        dirs = [file["path"] for file in response.json() if file["type"]=="dir"]
        print("Children directories in the templates folder:", dirs)
    else:
        print("Failed to retrieve files. Status Code:", response.status_code, response.json())
    return dirs