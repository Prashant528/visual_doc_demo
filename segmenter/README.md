# Unsupervised Topic Segmentation of Meetings with BERT Embeddings

This is the code for the paper **Unsupervised Topic Segmentation of Meetings with BERT Embeddings**.

Link to the paper https://arxiv.org/pdf/2106.12978 and original repository: https://github.com/gdamaskinos/unsupervised_topic_segmentation .

The code doesn't require training and uses a pretrained model from https://huggingface.co/transformers/model_doc/roberta.html
See paper appendix for more information.


# Changes made in this repo:
### Major new feature: Can segment on a custom corpus.

*[The original code uses AMI and ICSI datasets. If you're trying segmentation on those datasets, the original code should be more suitable.]*

1. Unpacked the major running functions in a notebook format.  See the Unsupervised_text_seg.ipynb.
2. We can run the code for our custom corpus. See the example corpus in the same notebook.
3. Changed the import method of RoBERTa to be compatible with latest Huggingface library.
4. There are minor modifications made in other base files like core.py and eval.py to make it compatible to the corpus I have.