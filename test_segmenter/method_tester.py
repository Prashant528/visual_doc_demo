import pandas as pd
import os
from segmenter.transformers_call import generate_sentences_for_text
from tqdm import tqdm
from segmenter.segment import segment
from nltk.metrics.segmentation import pk, windowdiff

def get_binaries_for_indices(indices):
    binaries = [0] * (max(indices)+1)
    binaries = [bin+1 if i in indices else bin for i, bin in enumerate(binaries)]
    return binaries

def calculate_pk(ground_truth, predicted_segments):
    #The window size for pk and windowdiff (usually kept half of the actual s)
    k_for_metrics = int(len(ground_truth)/2)

    #convert the segments found to strings (since that's how the scores work)
    reference = ''.join(str(x) for x in ground_truth)
    prediction = ''.join(str(x) for x in predicted_segments)


    test_pk_score = pk(reference, prediction, boundary='1')
    test_windowdiff_score = windowdiff(reference, prediction, k=2, boundary='1', weighted=False)

    print(f"PK score = {test_pk_score}")
    print(f"Windowdiff score = {test_windowdiff_score}")

    return test_pk_score, test_windowdiff_score

def test_segments():
    # Read the CSV file
    root_dir_path = os.getcwd()
    file_path = root_dir_path+ "/test_segmenter/ground_truth.xlsx"  # Replace with your actual file path
    excel_data = pd.ExcelFile(file_path)

    total_pk = 0
    total_windowdiff_score = 0
    number_of_files = len(excel_data.sheet_names)
    print(f"Number of files = {number_of_files}")
    for sheet in excel_data.sheet_names:
        print(f"Starting checking segments for {sheet}...")
        sheet_data = pd.read_excel(file_path, sheet_name=sheet)
        indices_for_segments = []
        # sentences_counter to keep track of the sentences so far.
        sentences_counter = 0
        for index, row in tqdm(sheet_data.iterrows()):
            paragraph = row['Paragraph']
            has_segment_after_prashant = row['Has segment after (Prashant)']
            sentences = generate_sentences_for_text(paragraph, method='stanza')
            sentences_counter = sentences_counter + len(sentences)
            #check if the ending sentence is a  'topic' or 'no_topic'. If topic, then add it to the segments indices.
            if has_segment_after_prashant != 'no_topic':
                #Add the length of current sentences to total previous sentences (-1 to make it start from 0)
                indices_for_segments.append(sentences_counter + len(sentences) -1)
        print(indices_for_segments)

        md_file_path = root_dir_path+ "/test_segmenter/files_for_ground_truth/" + sheet
        print(f"Segmenting {md_file_path}")
        predicted_segmentation, segments, segmented_file_path = segment(md_file_path, out_filename=sheet, save_to_file=True)
        #adding the ending segment marker since my algorithm doesn't add that automatically.
        predicted_segmentation.append(indices_for_segments[-1])

        # find binary boundaries and calculate PK
        ground_truth = get_binaries_for_indices(indices_for_segments)
        prediction = get_binaries_for_indices(predicted_segmentation)
        pk_score, windowdiff_score = calculate_pk(ground_truth, prediction)    
        total_pk = total_pk + pk_score
        total_windowdiff_score = total_windowdiff_score + windowdiff_score
    
    return (total_pk/number_of_files), (total_windowdiff_score/number_of_files)

if __name__=='__main__':
    # ind_1 = get_binaries_for_indices([1,5])
    # ind_2 = get_binaries_for_indices([1,5])
    # calculate_pk(ind_1, ind_2)
    pk_score, windowdiff_score  = test_segments()
    print(f"Final scores : pk = {pk_score}, windowdiff = {windowdiff_score}")