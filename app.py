from flask import Flask, render_template, request
from utils import download_file, download_wiki_file
from graph_generator import get_final_graph
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        owner = request.form['owner']
        repo = request.form['repo']
        file = request.form['file']
        # Here you can do whatever you want with the submitted link
        # For example, you can process it and generate some output
        print(f"The submitted link is: {owner}/{repo}/{file}.")
        # content =  download_file(owner, repo, file)
        content = 'hello'
        #commented for demo, need to uncomment
        # graph = get_final_graph(file, content)
        # return graph
        return render_template('flutter_flutter.html')
    else:
        return "Method not allowed"

if __name__ == '__main__':
    app.run(debug=True)
