from flask import jsonify
from utils import download_file, segregate_segments_by_classes, modfify_json_for_ui, add_links_to_json_from_content
from scrape_website import save_to_md
from graph_generator import get_final_graph
from segmenter.segment import segment
from classifier.run_classifier import run_classifier_with_paragraphs
from flask_cors import CORS
from code_from_visdoc.github_service import GitHubService
from code_from_visdoc.openai_service import OpenAIService
from code_from_visdoc.config import Config
from code_from_visdoc.utils import parse_openai_single_json
from code_from_visdoc.github_link_parser import parse_github_url
from segmenter.transformers_call import SentenceFeatureExtractor
import sys

def process_md_and_wiki(topic, link, data, github_service, github_url_components):
    """
    Dummy function to process .md or .wiki links.
    """
    print(f"Processing MD/WIKI link: {link}")

    clean_link = link.split('#')[0].split('?')[0]
    content_from_link = None
    if clean_link.endswith(".md"):
        print(f"Processing MD filepath: {github_url_components.filepath}")
        content_from_link = get_new_nodes_from_md(link, github_service, github_url_components)
        print("Fetching content_from_link successful.")
        with open('second_layer_output.txt', 'w') as outfile:
            outfile.write(str(content_from_link))

    elif clean_link.endswith(".wiki"):
        print(f"Processing wiki link: {link}")
        content_from_link =  get_new_nodes_from_wiki(link, github_service, github_url_components)
    else:
        print("Link is outbound to other pages than current repository.")
    
    merged_json = attach_second_layer(data, content_from_link, topic)
    return merged_json

def get_new_nodes_from_md(link, github_service, github_url_components):
    '''
    Get all the segments from the file like in app.py.
    '''
    owner = github_url_components.owner
    repo = github_url_components.name
    file_path = github_url_components.filepath
    print(owner, repo, file_path)
    if not owner or not repo or not file_path:
        return jsonify({"error": "The link doesn't contain one or many of these (owner, repo, file)."}), 400
    
    openai_service = OpenAIService(Config.OPENAI_API_KEY, repo)
    sentence_feature_extractor = SentenceFeatureExtractor()
    files_and_contents = github_service.download_recursive(owner, repo, file_path)
    file_and_content = files_and_contents[0]

    file_name = repo + '_' + file_and_content[0].split('/')[-1]
    content = file_and_content[1]
    md_file_path = save_to_md(content, file_name)

    predicted_segmentation, segments, segmented_file_path  = segment(sentence_feature_extractor, md_file_path, openai_service, file_name,  segmentation_method='langchain', sentence_method= 'stanza', save_to_file=True)

    prompt_for_llm = 'PROMPT_FOR_SEQUENCING_SECOND_LAYER'

    #Call the LLM to find the sequence
    prompt = openai_service.fetch_prompt(prompt_for_llm)

    for item in prompt:
            if item["role"] == "user":
                item["content"] += str(segments)

    with open('llm_prompt.txt', 'w') as outfile:
        outfile.write(str(prompt))
    # print(full_prompt_with_segments)
    llm_result = parse_openai_single_json(openai_service.get_llm_response_json(prompt))
    # print(f"\nActual response from API:\n {segments_flow_and_contents}")
    return llm_result

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

    # Iterate over each topic and its list of extracted links
    for topic, links_list in data.get("links", {}).items():
        topic_links = []
        for link in links_list:
            # We check the portion before possible '#' or query params
            # to see if it ends with .md or .wiki
            clean_link = link.split('#')[0].split('?')[0]

            if clean_link.endswith(".md") or clean_link.endswith(".wiki"):
                topic_links.append(clean_link)

            else:
                # Increment our counter for the next external link
                outbound_link_counter += 1
            
        #now process the unique links in each topic
        uniq_topic_links = list(set(topic_links))
        #if there is a link to the same page(different element), remove that too.
        if file_path in topic_links:
            topic_links.remove(file_path)
        for clean_link in uniq_topic_links:
            print("Processing for link : ", clean_link)

            if clean_link.startswith(('http://', 'https://')):
                # If the link is an absolute URL, add it directly
                print("Absolute link found")
                github_url_components = parse_github_url(link)
                print(clean_link)
                # print(github_url_components)
                merged_json  = process_md_and_wiki(topic, clean_link, data, github_service, github_url_components)
                break

            else:
                print("Relative link found")
                # Otherwise, add it to relative links
                new_link = github_service.create_new_filepath(file_path, clean_link)
                github_url_components.filepath = new_link
                print(new_link)
                # print(github_url_components)
                merged_json = process_md_and_wiki(topic, new_link, data, github_service, github_url_components)
                break
            break
        break

    return merged_json


def attach_second_layer(data, second_layer_nodes, topic):
    # Merge 'content'
    data["content"].update(second_layer_nodes.get("content", {}))

    # Get flow from second_layer_nodes
    flow_value = second_layer_nodes.get("flow", None)
    if not flow_value:
        # No flow => just return data after merging content
        return data

    # If it's a dict, wrap it in a list
    if isinstance(flow_value, dict):
        flow_items = [flow_value]
    elif isinstance(flow_value, list):
        flow_items = flow_value
    else:
        # Unexpected type => handle error or return
        print("ERROR: 'flow' is neither a list nor a dict.")
        return data

    # If flow_items is empty or doesn't have edges, bail out
    if not flow_items:
        return data

    first_flow_item = flow_items[0]
    first_edges = first_flow_item.get("edges", [])
    if not first_edges:
        return data

    first_node = first_edges[0]["source"]

    # Extract the existing sequence for 'topic'
    topic_sequence = None
    for flow_item in data["flow"]:
        for edge in flow_item.get("edges", []):
            if edge["source"] == topic or edge["target"] == topic:
                topic_sequence = flow_item.get("sequence")
                break
        if topic_sequence:
            break
    if topic_sequence is None:
        topic_sequence = "Attached second layer"

    # Create a link from 'topic' -> first_node
    new_flow_item = {
        "edges": [
            {
                "source": topic,
                "target": first_node
            }
        ],
        "sequence": topic_sequence
    }
    data["flow"].append(new_flow_item)

    # Append the second layer flow
    data["flow"].extend(flow_items)
    
    with open('new_flow_items.txt', 'w') as outfile:
        outfile.write(str(flow_items))
        
    return data
