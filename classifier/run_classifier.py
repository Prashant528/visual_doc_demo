# from classifier.classify_content import get_contributing_predictions
# import pandas as pd

# repository_links = {
#     'flutter': 'https://github.com/flutter/flutter/blob/master/CONTRIBUTING.md',
#     'node': 'https://github.com/nodejs/node/blob/main/CONTRIBUTING.md',
#     'electron': 'https://github.com/electron/electron/blob/main/CONTRIBUTING.md',
#     '30-seconds-of-code': 'https://github.com/Chalarangelo/30-seconds-of-code/blob/master/CONTRIBUTING.md',
#     'transformers': 'https://github.com/huggingface/transformers/blob/main/CONTRIBUTING.md',
#     'youtube-dl': 'https://github.com/ytdl-org/youtube-dl/blob/master/CONTRIBUTING.md',
#     'vscode': 'https://github.com/microsoft/vscode/blob/main/CONTRIBUTING.md',
#     'tensorflow': 'https://github.com/tensorflow/tensorflow/blob/master/CONTRIBUTING.md'
# }

# for repository_link in repository_links:
#     paragraphs, predictions = get_contributing_predictions(page=None, repository_url = repository_link)

#     for i in range(len(paragraphs)):
#         print("Paragraph = ", paragraphs[i])
#         print("Prediction = ", predictions[i])

import pandas as pd
from classifier.classify_content import get_contributing_predictions

# Define the repository links
repository_links = {
    'flutter': 'https://github.com/flutter/flutter/blob/master/CONTRIBUTING.md',
    'node': 'https://github.com/nodejs/node/blob/main/CONTRIBUTING.md',
    'electron': 'https://github.com/electron/electron/blob/main/CONTRIBUTING.md',
    '30-seconds-of-code': 'https://github.com/Chalarangelo/30-seconds-of-code/blob/master/CONTRIBUTING.md',
    'transformers': 'https://github.com/huggingface/transformers/blob/main/CONTRIBUTING.md',
    # 'youtube-dl': 'https://github.com/ytdl-org/youtube-dl/blob/master/CONTRIBUTING.md',
    'vscode': 'https://github.com/microsoft/vscode/blob/main/CONTRIBUTING.md',
    'tensorflow': 'https://github.com/tensorflow/tensorflow/blob/master/CONTRIBUTING.md'
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
