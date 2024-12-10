import pandas as pd
import glob, os
from nltk.metrics.segmentation import pk, windowdiff


parent_dir = os.getcwd()
path = parent_dir + "/test_segmenter/files_for_ground_truth/*.csv"
print(path)
csv_files = glob.glob(path)
dataframes = [pd.read_csv(file, skipinitialspace=True) for file in csv_files]
combined_df = pd.concat(dataframes, ignore_index=True)

print(combined_df.columns)
ground_truth = combined_df['ground_truth'].tolist()
ground_truth_str = ''.join(str(x) for x in ground_truth)
all_columns = ['segments_from_unsupervised_0.05_4','segments_from_langchain_90_2', 'segments_from_langchain_default', 'segments_from_llm']

for column in all_columns:
    if not combined_df[column].isna().any():
        method_boundaries = combined_df[column].tolist()
        method_boundaries_str = ''.join(str(x) for x in method_boundaries)
        pk_score = pk(ground_truth_str, method_boundaries_str, boundary='1')
        windowdiff_score = windowdiff(ground_truth_str, method_boundaries_str, k=2, boundary='1', weighted=False)
        print(f"For column {column}:")
        print(f"PK score = {pk_score}")
        print(f"window diff score = {windowdiff_score}")