from flask import Flask, render_template, request
from utils import download_file
from scrape_website import save_to_md
from graph_generator import get_final_graph
from segmenter.segment import segment
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#this loads the editing window for the document segment editing
@app.route('/edit_segments', methods=['POST'])
def edit_segments():
    if request.method == 'POST':
        owner = request.form['owner']
        repo = request.form['repo']
        file = request.form['file']
        # Here you can do whatever you want with the submitted link
        # For example, you can process it and generate some output
        print(f"The submitted link is: {owner}/{repo}/{file}.")
        content =  download_file(owner, repo, file)
        file_name = repo + '_contrib.md'
        md_file_path = save_to_md(content, file_name)
        # content = 'hello'
        #commented for demo, need to uncomment
        # graph = get_final_graph(file, content, owner, repo)
        # return graph
        segmented_file_path  = segment(md_file_path, repo)

    return render_template('text_segment_editor.html', file_path=segmented_file_path)

@app.route('/generate')
def generate():
    return render_template('flutter_flutter.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
