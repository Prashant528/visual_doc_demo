import numpy as np
import pandas as pd
import torch
from segmenter.langchain_semantic_chunker import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

from segmenter.core import *
from segmenter.transformers_call import generate_sentences_not_considering_blocks
# mean_pooling, get_features_from_sentence, generate_sentences_considering_blocks, generate_sentences_not_considering_blocks
from segmenter.clean_markdown import markdn2text_gfm
from segmenter.bullet_points_finder import get_block_lines, add_block_identifier, find_block_markers_in_sentences

def segment(sentence_feature_extractor, md_file_path, out_filename='latest', segmentation_method='unsupervised_window_based', sentence_method= 'stanza', save_to_file=False):
    '''
    Methods:
    1. unsupervised_window_based (https://arxiv.org/pdf/2106.12978)
    2. langchain (https://python.langchain.com/v0.2/docs/how_to/semantic-chunker/)
    '''

    #Parse the file and get the unseparable blocks
    #gfm parser gets the md file and parses it to a text file.
    parsed_file_path = markdn2text_gfm(md_file_path)

    #adding blocks information in parsed file since it preserves the formatting of md.
    block_of_lines = get_block_lines(parsed_file_path)
    print("Block of lines = ", block_of_lines)
    #add block identifiers in the file
    add_block_identifier(parsed_file_path, block_of_lines)
    #get the sentences with the block markers as sentences too.
    sentences = generate_sentences_not_considering_blocks(parsed_file_path, method=sentence_method)
    #get the block marker indices, remove the marker sentences and return original sentences.
    block_marker_indices, sentences = find_block_markers_in_sentences(sentences)
    print("Block markers in sentences:", block_marker_indices)

    if segmentation_method=='unsupervised_window_based':
        predicted_segmentation, segments = segment_unsupervised(sentence_feature_extractor, sentences, block_marker_indices)
        #account for the ending topic border => already did inside the function
        # predicted_segmentation.append(1)
        # predicted_segmentation[-1] = 1
    elif segmentation_method=='langchain':
        predicted_segmentation, segments = segment_langchain(sentences, block_marker_indices)
        #account for the ending topic border
        # predicted_segmentation.append(1)
        predicted_segmentation[-1] = 1

    else:
        raise Exception("Unknown segmentation method provided. Please check segment() method in /segmenter/segment file")
    
    file_name= None
    if save_to_file:
        file_name = 'static/segmenter_outputs/'+ out_filename +'_segmented_file.txt'
        file1  = open(file_name, "w")
        #works for both sentences and paragraphs
        for segment in segments:
            file1.write(segment)
            file1.write("\n\n-----------------------------<PREDICTEDSEGMENT>--------------------------\n\n")
        file1.close()

        file_name = 'segmenter/parsed_sentences/'+ out_filename +'_parsed_by_algo.txt'
        file2  = open(file_name, "w")
        #works for both sentences and paragraphs
        for sentence in sentences:
            file2.write(sentence)
            file2.write("\n--------\n")
        file2.close()
    print("Number of sentences in our segmentation algo = ", len(sentences))
    return predicted_segmentation, segments, file_name

def segment_unsupervised(sentence_feature_extractor, sentences, block_marker_indices):
    #'S' for sentence level, 'P' for paragraph level
    # corpus_type = 'S'
    corpus_type = 'P'

    TOPIC_CHANGE_THRESHOLD = 0.05

    WINDOW_SIZE = 4


    features = sentence_feature_extractor.get_features_from_sentence(sentences)

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
            predicted_section_indices.append(idx + offset -1)

    predicted_segmentation = [0] * len(sentences)

    for idx in predicted_section_indices:
        for line_block in block_marker_indices:
                #shift the segmentation marker to the end of the block
                if idx > line_block[0] and idx < line_block[1]:
                    print(f"Segment found inside a block at: {idx} between {line_block[0]} and {line_block[1]}.")
                    idx = line_block[1]
        predicted_segmentation[idx] = 1
    #for the last sentence
    predicted_segmentation[-1] = 1

    # print(predicted_segmentation)
    print(len(predicted_segmentation))
    print("Old preditcion section indices = ", predicted_section_indices)
    new_indices = [i for i, value in enumerate(predicted_segmentation) if value == 1]
    print("New preditcion section indices (after shifting to end of block)= ", new_indices)

    print("Preparing segments...")
    segments = []
    sentences_in_this_segment = ''
    for idx, sentence in enumerate(sentences):
        sentences_in_this_segment = sentences_in_this_segment + '\n' + sentence
        if predicted_segmentation[idx]==1:
            segments.append(sentences_in_this_segment)
            sentences_in_this_segment = ''
    
    return predicted_segmentation, segments
    

def segment_langchain(sentences, block_marker_indices):
    TOPIC_CHANGE_THRESHOLD = 90
    WINDOW_SIZE = 2

    text_splitter = SemanticChunker(
                        OpenAIEmbeddings(), 
                        breakpoint_threshold_type="gradient",
                        # breakpoint_threshold_amount=TOPIC_CHANGE_THRESHOLD,
                        # buffer_size=WINDOW_SIZE
                    )
    predicted_segmentation, segments = text_splitter.split_text_modified(sentences, block_marker_indices)
    
    return predicted_segmentation, segments