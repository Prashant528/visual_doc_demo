import requests
from collections import defaultdict
import regex as re

def download_file(owner, repo, file_path):
    # GitHub repository information. Example:
    # owner = 'flutter'
    # repo = 'flutter'
    # file_path = 'CONTRIBUTING.md'

    # Construct the URL to download the raw file
    raw_url = f'https://raw.githubusercontent.com/{owner}/{repo}/main/{file_path}'

    try:
        # Send a GET request to download the file
        response = requests.get(raw_url)
        if response.status_code == 200:
            print("Response code 200")
            response.encoding = 'UTF-8'
            # If the request is successful, return the file as a response
            return(response.content)
        else:
            return f"Failed to download file: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def segregate_segments_by_classes(segments_and_classes_in_all_files):
    print("Started segregating segments ...")
    #Find all distinct classes in the files
    all_classes =[]
    for segments_and_classes_in_each_file in segments_and_classes_in_all_files:
        classes_in_that_file = segments_and_classes_in_each_file[1]
        print(f"Classes in that file = ", classes_in_that_file)
        all_classes = all_classes + classes_in_that_file
    all_classes = set(all_classes)
    print(f"All distinct classes found =  {all_classes}")
    #For each segment class, initialize a list to hold the segments.
    class_segments_holder = {}
    for each_class in all_classes:
        class_segments_holder[each_class] = []

    #For each segment, add it to correct class in the dictionary
    for segments_and_classes_in_each_file in segments_and_classes_in_all_files:
        segments = segments_and_classes_in_each_file[0]
        segment_classes = segments_and_classes_in_each_file[1]
        for segment, segment_class in zip(segments, segment_classes):
            class_segments_holder[segment_class].append(segment)
    print("Completed segregating segments ...")
    return class_segments_holder

def modfify_json_for_ui(old_json, repo_name):
    new_json = {"content": {}, "flow": []}

    # Dictionary to keep track of occurrences of each step
    step_counter = defaultdict(int)
    step_rename_map = {}  # Maps old step names to new step names
    step_rename_map['Parent Node'] = f'Contributing to {repo_name}'

    for sequence_name, sequence_data in old_json.items():
        # Process content
        updated_content = {}
        for step, description in sequence_data["content"].items():
            step_counter[step] += 1
            new_step_name = f"{step} #{step_counter[step]}" if step_counter[step] > 1 else step
            step_rename_map[step] = new_step_name  # Update the map
            updated_content[new_step_name] = description

        # Add updated content to new_json
        new_json["content"].update(updated_content)

        # Process flow edges
        updated_edges = []
        for edge in sequence_data["flow"]["edges"]:
            source = step_rename_map[edge["source"]]
            target = step_rename_map[edge["target"]]
            updated_edges.append({"source": source, "target": target})

        # Add flow with updated edges and sequence name
        new_json["flow"].append({"edges": updated_edges, "sequence": sequence_name})
    return new_json


def add_links_to_json_from_content(data):
    #Extract links from each content topic
    links_dict = {}
    for topic, markdown_content in data["content"].items():
        links_dict[topic] = extract_links_from_markdown(markdown_content)
    
    #Add the 'links' key to the JSON structure
    data["links"] = links_dict

    return data

def extract_links_from_markdown(markdown_text):
    """
    Extract all links from a Markdown string.
    Returns a list of link URLs (including relative paths, anchors, etc.).
    """
    # This regex captures the URL within parentheses following a standard Markdown link [text](URL).
    pattern = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
    return pattern.findall(markdown_text)


if __name__ == '__main__':
    print(download_file('flutter', 'flutter', 'CONTRIBUTING.md'))
