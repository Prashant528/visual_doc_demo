from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from nltk.tokenize import sent_tokenize
import nltk
from tqdm import tqdm
from segmenter.bullet_points_finder import find_bullet_points
nltk.download('punkt')
import stanza

#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def get_features_from_sentence(sentences):
  batch_features = []
  # Load model from HuggingFace Hub
  print("Loading the ROBERTA model...")
  tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-roberta-large-v1')
  model = AutoModel.from_pretrained('sentence-transformers/all-roberta-large-v1')

  print("Generating sentence embeddings...")
  for sentence in tqdm(sentences):
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


def generate_sentences_considering_blocks(corpus_file):
  '''
  returns a list of sentences given a a paragraph.
  We treat lines in between the bullet points as a single sentence(unit).
  Reason: The segmenter was creating segments in between the bullet points which is not desirable in our segments.
  '''
  print("Finding bullet points...")
  bullet_points_indices = find_bullet_points(corpus_file)

  print("Tokenizing into sentences...")
  #get the sentences of the sections
  #sections between bullet points are treated as a single sentence.
  all_sentences = []
  with open(corpus_file, 'r') as f:
      #if there were no bullet points
      if len(bullet_points_indices)==0:
        whole_content = f.read()
        return sent_tokenize(whole_content)
      
      #if there were bullet points, then we have to filter those lines.
      print("Bullet points found. Tokenizing the sentences with that consideration.")
      all_lines = f.readlines()
      start_idx = 1   
      #don't split the bullet points into paragraphs.
      for bullet_start, bullet_end in bullet_points_indices:
          #add sentences in non_bullet sections
          #For start_idx-1: I noticed that one line before bullet points is almost always together so including that line too.
          lines_till_bullets = all_lines[start_idx-1:bullet_start]
          non_bullet_section = ' '.join(lines_till_bullets)
          sentences = sent_tokenize(non_bullet_section)
          all_sentences = all_sentences + sentences

          #add the bullet point section as a single sentence
          lines_in_between_bullets = all_lines[bullet_start:bullet_end]
          bullet_section = ' '.join(lines_in_between_bullets)
          all_sentences.append(bullet_section)

          #update the start of next bullet point to find another non-bullet points section.
          start_idx = bullet_end
      #add the section after the bullet points
      rem_lines =  all_lines[start_idx-1:]
      rem_section = ' '.join(rem_lines)
      sentences = sent_tokenize(rem_section)
      all_sentences = all_sentences + sentences

  return all_sentences

def generate_sentences_not_considering_blocks(corpus_file, method='nltk'):
  '''
  returns a list of sentences given a a paragraph.
  We  don't treat lines in between the bullet points as a single sentence(unit).
  Methods = nltk, stanza
  '''
  print("Tokenizing into sentences...")
  with open(corpus_file, 'r') as f:
      whole_content = f.read()
  if method=='nltk':
      return sent_tokenize(whole_content)
  elif method=='stanza':
      stanza.download('en')
      nlp = stanza.Pipeline(lang='en', processors='tokenize')
      doc = nlp(whole_content)
      sentences = [sentence.text for sentence in doc.sentences]
      return sentences
  
if __name__=='__main__':
    filename = '/Users/tandanp/Documents/doc_scraper/segmenter/outputs/parsed_file_'+'.txt'
    sentences = generate_sentences_not_considering_blocks(filename, method='nltk')
    print(sentences)

