import re
import unicodedata
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import nltk
from nltk.tokenize.toktok import ToktokTokenizer


#import spacy


#nlp = spacy.load('en_core', parse=True, tag=True, entity=True)
#nlp_vec = spacy.load('en_vecs', parse = True, tag=True, #entity=True)

#stopword_list.remove('no')
#stopword_list.remove('not')



tokenizer = ToktokTokenizer()
nltk.download('stopwords')
stopword_list = nltk.corpus.stopwords.words('english')

#Remove accented characters 
def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, ' ', text)
    return text

def remove_stopwords(text, is_lower_case=False,return_str=True):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    if return_str:
        filtered_text = ' '.join(filtered_tokens)
        return filtered_text
    else: 
        return filtered_tokens
    

def remove_html(text):
    parse = BeautifulSoup(text,'lxml')
    return parse.get_text()

#Translate to English using Google API (but with Limit!)   
def to_eng(x):
    trans = Translator()
    try: 
        return(trans.translate(x,dest='en').text)
    except:
        return(np.nan)
    
#extract excel file of text to be translated 

def get_file(df,filename): #text is a DataFrame of columns = attributes to be translated
    df.to_excel(filename,index=False)

