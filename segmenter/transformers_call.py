from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')

#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def get_features_from_sentence(sentences):
  batch_features = []
  # Load model from HuggingFace Hub
  tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-roberta-large-v1')
  model = AutoModel.from_pretrained('sentence-transformers/all-roberta-large-v1')

  for sentence in sentences:
    # Tokenize sentence
    encoded_input = tokenizer(sentence, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

    batch_features.append(sentence_embeddings[0])
    # print("Sentence embeddings:")
    # print(sentence_embeddings)
  return batch_features


def generate_sentences(para):
  '''
  returns a list of sentences given a a paragraph.
  I'm aware that this should not have been a function.
  '''
  sentences = sent_tokenize(para)
  return sentences