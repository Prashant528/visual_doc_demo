from flask import Flask, render_template, request, jsonify
from utils import download_file, segregate_segments_by_classes
from scrape_website import save_to_md
from graph_generator import get_final_graph
from segmenter.segment import segment
from classifier.run_classifier import run_classifier_with_paragraphs
from flask_cors import CORS
from code_from_visdoc.github_service import GitHubService
from code_from_visdoc.openai_service import OpenAIService
from code_from_visdoc.config import Config
from code_from_visdoc.utils import parse_openai_single_json, parse_github_link

app = Flask(__name__)
CORS(app) 

# Initialize services
github_service = GitHubService(Config.GITHUB_TOKEN)
openai_service = OpenAIService(Config.OPENAI_API_KEY)


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
        owner, repo, file_path = parse_github_link(repo_link)
        if not owner or not repo or not file_path:
            return jsonify({"error": "The link doesn't contain one or many of these (owner, repo, file)."}), 400
        # Download contributing.md and related files PTANDAN(remove the below comment)
        #TODO: I need to add some mechanism to store the contents of each file and return them as a list here inside download_recursive function.
        files_and_contents = github_service.download_recursive(owner, repo, file_path)

        print(files_and_contents)

        segments_and_classes_in_all_files = []
        for file_and_content in files_and_contents:
            file_name = repo + file_and_content[0]
            content = file_and_content[1]
            md_file_path = save_to_md(content, file_name)
            # content = 'hello'
            #commented for demo, need to uncomment
            # graph = get_final_graph(file, content, owner, repo)
            # return graph
            segments, segmented_file_path  = segment(md_file_path, repo, segmentation_method='unsupervised_window_based', sentence_method= 'stanza', save_to_file=True)
            segments, segment_classes = run_classifier_with_paragraphs(segments)
            print(segment_classes)
            segments_and_classes_in_all_files.append((segments, segment_classes))

        print(len(segments_and_classes_in_all_files))
        # Returns a dictionary with class: list of segments
        segregated_segments = segregate_segments_by_classes(segments_and_classes_in_all_files)
        #Call the LLM to find the sequence
        segments_flow_and_contents = openai_service.find_sequences_for_allsegments(segregated_segments)
    # return render_template('text_segment_editor.html', file_path=segmented_file_path)
    return segments_flow_and_contents

@app.route('/generate')
def generate():
    return render_template('flutter_flutter.html')

if __name__ == '__main__':
    app.run(port=8080, debug=True, threaded=True)
