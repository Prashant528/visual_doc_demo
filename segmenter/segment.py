import numpy as np
import pandas as pd
import torch

from segmenter.core import *
from segmenter.transformers_call import mean_pooling, get_features_from_sentence, generate_sentences
from segmenter.clean_markdown import markdn2text_gfm

def segment(md_file_path, out_filename):
    #'S' for sentence level, 'P' for paragraph level
    # corpus_type = 'S'
    corpus_type = 'S'

    TOPIC_CHANGE_THRESHOLD = 0.05

    WINDOW_SIZE = 5

    paragraphs = markdn2text_gfm(md_file_path)
    corpus = ''
    for paragraph in paragraphs:
        corpus  =  corpus + '\n' + paragraph
    sentences = generate_sentences(corpus)
    print("Sentences:", len(sentences))

    features = get_features_from_sentence(sentences)

    print(len(features[0]))


    res = []
    k= WINDOW_SIZE
    for i in range(k, len(features) - k):

        #unpacking compute_window function for first window features
        stack = torch.stack([features for features in features[i-k:i+1]])
        stack = stack.unsqueeze(
            0
        )
        stack_size = i+1 - (i-k)
        pooling = torch.nn.MaxPool2d((stack_size - 1, 1))
        first_window_features = pooling(stack)
        #end of compute_window_function (the stack size varies)

        #unpacking compute_window function for second window features
        stack = torch.stack([features for features in features[i+1:i+k+2]])
        stack = stack.unsqueeze(
            0
        )
        stack_size = i+k+2 - (i+1)
        pooling = torch.nn.MaxPool2d((stack_size - 1, 1))
        second_window_features = pooling(stack)
        res.append(
            sentences_similarity(first_window_features[0], second_window_features[0])
        )

    block_comparison_score_timeseries = res

    #smooth out the similiarity scores by averaging over a smoothing window.
    block_comparison_score_timeseries = smooth(
        block_comparison_score_timeseries,
        n=2,
        s=1,
    )

    timeseries = block_comparison_score_timeseries
    print("Length of timeseries: ", len(timeseries))

    depth_scores = []
    for i in range(1, len(timeseries) - 1):
        left, right = i - 1, i + 1
        while left > 0 and timeseries[left - 1] > timeseries[left]:
            left -= 1
        while (
            right < (len(timeseries) - 1) and timeseries[right + 1] > timeseries[right]
        ):
            right += 1
        depth_scores.append(
            (timeseries[right] - timeseries[i]) + (timeseries[left] - timeseries[i])
        )
    depth_score_timeseries = depth_scores

    TOPIC_CHANGE_THRESHOLD = 0.05
    n = len(depth_score_timeseries)
    print("Length of depth score timeseries (should be actual length-2*window size+1?) = ", n)
    threshold = TOPIC_CHANGE_THRESHOLD * max(depth_score_timeseries)
    print("TOPIC_CHANGE_THRESHOLD = ", TOPIC_CHANGE_THRESHOLD)
    print("Threshold = ", threshold)
    print("Max of depth score = ", max(depth_score_timeseries))

    local_maxima_indices, local_maxima = get_local_maxima(depth_score_timeseries)
    print(f"Local maxima: {local_maxima}")
    print(f"Number of local maxima : {len(local_maxima)}")

    if local_maxima == []:
        print("No local maxima found")


    # this is the vanilla TextTiling used for Pk optimization
    filtered_local_maxima_indices = []
    filtered_local_maxima = []

    for i, m in enumerate(local_maxima):
        if m > threshold:
            filtered_local_maxima.append(m)
            filtered_local_maxima_indices.append(i)

    local_maxima = filtered_local_maxima
    local_maxima_indices = filtered_local_maxima_indices

    print("Filtered LOCAL_MAXIMA_INDICES:")
    print(list(local_maxima_indices))
    print("Filtered LOCAL_MAXIMA_VALUES:")
    print(list(local_maxima))

    segments = local_maxima_indices

    offset = k
    predicted_section_indices = []
    for idx, score in enumerate(depth_score_timeseries):
        if score in local_maxima:
            predicted_section_indices.append(idx + offset)

    predicted_segmentation = [0] * len(sentences)
    for idx in predicted_section_indices:
        predicted_segmentation[idx] = 1

    # print(predicted_segmentation)
    print(len(predicted_segmentation))
    print("Preditcion section indices = ", predicted_section_indices)

    file_name = 'static/segmenter_outputs/'+ out_filename +'_segmented_file.txt'
    file1  = open(file_name, "w")
    #works for both sentences and paragraphs
    for idx, sentence in enumerate(sentences):
        if idx in predicted_section_indices:
            file1.write("\n\n-----------------------------<PREDICTEDSEGMENT>--------------------------\n\n")
        file1.write(sentence)
        file1.write('\n')
    file1.close()

    return file_name

# segmented_file_name = segment('downloaded_files/flutter_contrib.md')
# print(segmented_file_name)