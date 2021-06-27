from dependency import * 
tokenizer = ToktokTokenizer()

def remove_html(text):
  parse = BeautifulSoup(text,'lxml')
  return parse.get_text(' ').lower()


def remove_accented_chars(text):
  text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
  return text

def remove_special_characters(text, remove_digits=False):
  pattern = re.compile('[^a-zA-z0-9\s]') if not remove_digits else r'[^a-zA-z\s]'
  text = re.sub(pattern, ' ', text)
  return text

def remove_stopwords(text, is_lower_case=False):
  nltk.download('stopwords')
  stopword_list = nltk.corpus.stopwords.words('english')
  
  tokens = tokenizer.tokenize(text)
  tokens = [token.strip() for token in tokens]
  if is_lower_case:
    filtered_tokens = [token for token in tokens if token not in stopword_list]
  else:
    filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
  
  filtered_text = ' '.join(filtered_tokens)
  return filtered_text
    

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": 'a',
                "N": 'n',
                "V": 'v',
                "R": 'r'}
    return tag_dict.get(tag)


def wordnet_lemmatize(text): 
  from nltk.stem import WordNetLemmatizer
  nltk.download('wordnet')
  nltk.download('averaged_perceptron_tagger')
  w = WordNetLemmatizer()
  
  tokens = tokenizer.tokenize(text)
  tokens = [token.strip() for token in tokens]
  lemma_tokens = [w.lemmatize(token, get_wordnet_pos(token)) for token in tokens]
  
  lemma_text = ' '.join(lemma_tokens)
  return lemma_text 


def spacy_lemmatize(text): 
  import spacy  
  nlp = spacy.load('en', disable=['parser', 'ner'])
  lemma_text = nlp(text)
  lemma_text = " ".join([token.lemma_ for token in lemma_text])
  return lemma_text 
    

def quick_clean(text, html=1, specchar=1, stopword=1, lemmatize=1): 
    if html == 1:
        text = remove_html(text)
    if specchar == 1: 
        text = remove_special_characters(text,remove_digits=True)
    if stopword == 1:
        text = remove_stopwords(text)
    if lemmatize == 1:
        text = wordnet_lemmatize(text)
    if lemmatize == 2:
        text = spacy_lemmatize(text)
    return text