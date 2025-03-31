from flask import Flask, render_template, request, jsonify
from utils import download_file, segregate_segments_by_classes, modfify_json_for_ui, add_links_to_json_from_content, save_llm_output, modify_json_for_ui_without_classifier
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
from second_layer import *

app = Flask(__name__)
CORS(app) 

# Initialize services
github_service = GitHubService(Config.GITHUB_TOKEN)
TURN_CLASSIFIER_ON = False
turn_second_layer_on = True
save_llm_output_to_files = True


@app.route('/')
def index():
    return render_template('index.html')

#this loads the editing window for the document segment editing
@app.route('/fetch_and_analyze', methods=['POST'])
def fetch_and_analyze():
    if request.method == 'POST':
        # OLD: Data coming from Old homepage
        # owner = request.form['owner']
        # repo = request.form['repo']
        # file = request.form['file']
        # print(f"The submitted link is: {owner}/{repo}/{file}.")
        # content =  download_file(owner, repo, file)

        #NEW: Data coming from new homepage
        data = request.json
        print(data)
        repo_link = data.get('repo_link')
        github_url_components = parse_github_url(repo_link)
        owner = github_url_components.owner
        repo = github_url_components.name
        file_path = github_url_components.filepath
        print(owner, repo, file_path)
        if not owner or not repo or not file_path:
            return jsonify({"error": "The link doesn't contain one or many of these (owner, repo, file)."}), 400
        
        openai_service = OpenAIService(Config.OPENAI_API_KEY, repo)
        sentence_feature_extractor = SentenceFeatureExtractor()
        # Download contributing.md and related files PTANDAN(remove the below comment)
        #TODO: I need to add some mechanism to store the contents of each file and return them as a list here inside download_recursive function.
        files_and_contents = github_service.download_recursive(owner, repo, file_path)

        # print(files_and_contents)

        segments_and_classes_in_all_files = []
        for file_and_content in files_and_contents:
            file_name = repo + '_' + file_and_content[0].split('/')[-1]
            content = file_and_content[1]
            md_file_path = save_to_md(content, file_name)
            # content = 'hello'
            #commented for demo, need to uncomment
            # graph = get_final_graph(file, content, owner, repo)
            # return graph
            predicted_segmentation, segments, segmented_file_path  = segment(sentence_feature_extractor, md_file_path, openai_service, file_name,  segmentation_method='langchain', sentence_method= 'stanza', save_to_file=True, repo=repo, filename=file_path)
            # print(segments)
            if TURN_CLASSIFIER_ON:
                #returns two lists. First list = segment, second list = the class for that segment.
                segments, segment_classes = run_classifier_with_paragraphs(segments)
                prompt_for_llm = 'PROMPT_FOR_SEQUENCING_VER_MAKE_DISCRETE_TASKS_MERGE_AND_TRIM_WITH_SEG_CLASS_VER_2'
            else:
                segment_classes = [f'Contributing to {repo}']
                prompt_for_llm = 'PROMPT_FOR_SEQUENCING_VER_MAKE_DISCRETE_TASKS_MERGE_AND_TRIM_WITH_SEG_WITHOUT_CLASS_VER_2'
            print(segment_classes)
            segments_and_classes_in_all_files.append((segments, segment_classes))
            print("No of segments found = ", len(segments))


        if TURN_CLASSIFIER_ON:
            #------------------ <UNCOMMENT THIS
            # Returns a dictionary with {class: list of segments}
            segregated_segments = segregate_segments_by_classes(segments_and_classes_in_all_files)
            #Call the LLM to find the sequence, returns topics/contents and flow.
            segments_flow_and_contents = openai_service.find_sequences_for_allsegments(segregated_segments, prompt_for_llm)
            # print(f"\nActual response from API:\n {segments_flow_and_contents}")

            modified_json_for_ui = modfify_json_for_ui(segments_flow_and_contents, repo)
        else:
            #Returns a JSON with {topic: content} for all of the segments.
            topics_and_segments = openai_service.find_topics_and_flow_for_segments_without_classifier(segments_and_classes_in_all_files, prompt_for_llm)
            #create flow out of the topics.
            modified_json_for_ui = modify_json_for_ui_without_classifier(topics_and_segments, repo)
        # print(f"\nModified response from API:\n {modified_json_for_ui}")

        if save_llm_output_to_files:
            save_llm_output(modified_json_for_ui, 'modified_json_for_ui')

        if turn_second_layer_on:
            json_with_links = add_links_to_json_from_content(modified_json_for_ui)
            save_llm_output(json_with_links, 'json_with_links')
            #------------------ UNCOMMENT THIS>

            #-------------Starting second layer
            json_with_second_layer = add_second_layer_from_links(json_with_links, file_path, github_url_components)
            
            #-------------Removing the links
            result = {key: json_with_second_layer[key] for key in ["content", "flow"]}

            #--------------Saving the result
            save_llm_output(result, '1+2_layer')
            
        else:
            result = modified_json_for_ui
    # return render_template('text_segment_editor.html', file_path=segmented_file_path)
    return result

@app.route('/generate')
def generate():
    return render_template('flutter_flutter.html')

@app.route('/flutter_cached', methods=['GET'])
def flutter_cached():
    file_path = os.path.join('static', 'cached_results', 'flutter.json')

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format'}), 500
    

@app.route('/transformers_cached', methods=['GET'])
def node_cached():
    file_path = os.path.join('static', 'cached_results', 'transformers.json')

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format'}), 500

if __name__ == '__main__':
    app.run(port=8080, debug=True, threaded=True)
