
import pandas as pd
from classifier.classify_content import get_contributing_predictions
import pickle
from classifier.get_features import convert_paragraphs_into_features

def run_classifier_with_paragraphs():
    # Define the repository links
    repository_links = {
        'flutter': 'https://github.com/flutter/flutter/blob/master/CONTRIBUTING.md',
        # 'node': 'https://github.com/nodejs/node/blob/main/CONTRIBUTING.md',
        # 'electron': 'https://github.com/electron/electron/blob/main/CONTRIBUTING.md',
        # '30-seconds-of-code': 'https://github.com/Chalarangelo/30-seconds-of-code/blob/master/CONTRIBUTING.md',
        # 'transformers': 'https://github.com/huggingface/transformers/blob/main/CONTRIBUTING.md',
        # # 'youtube-dl': 'https://github.com/ytdl-org/youtube-dl/blob/master/CONTRIBUTING.md',
        # 'vscode': 'https://github.com/microsoft/vscode/blob/main/CONTRIBUTING.md',
        # 'tensorflow': 'https://github.com/tensorflow/tensorflow/blob/master/CONTRIBUTING.md'
    }

    # Create a writer object to save the Excel file
    with pd.ExcelWriter('repository_contributions.xlsx', engine='xlsxwriter') as writer:
        
        # Loop through each repository and its link
        for repo_name, repository_link in repository_links.items():
            # Get paragraphs and predictions for each repository
            print(f"Writing results for {repo_name}")
            paragraphs, predictions = get_contributing_predictions(page=None, repository_url=repository_link)
            
            # Create a DataFrame with paragraphs and predictions
            data = {
                'Paragraph': paragraphs,
                'Prediction': predictions
            }
            df = pd.DataFrame(data)
            
            # Write the DataFrame to a specific sheet named after the repository
            df.to_excel(writer, sheet_name=repo_name, index=False)

    print("Data has been written to 'repository_contributions.xlsx'")


def run_classifier_with_paragraphs(paragraphs):
    print("Running classification model on segments ...")
    # Loads the classification model.
    model = pickle.load(open('classifier/classification_model.sav', 'rb'))
    # Using the estimator, predicts the classes for the paragraphs in the file
    predictions = model.predict(convert_paragraphs_into_features(paragraphs))
    return paragraphs, predictions

if __name__=='__main__':
    para = ['''Our code of conduct, which stipulates explicitly
    that everyone must be gracious, respectful, and professional. This
    also documents our conflict resolution policy and encourages people
    to ask questions.''',
    '''
    Triage is the process of going through bug reports and determining if they are valid, finding out
    how to reproduce them, catching duplicate reports, and generally making our issues list
    useful for our engineers.
    '''
    ]
    run_classifier_with_paragraphs(para)