import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from collections import defaultdict

class NModule(object):
    def __init__(self):
        pass
    
    # Tokenizes sentence without punctuation
    def split_sentence(self, sentence):
        tokenizer = RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(sentence)

    # Part-of-speech tagging
    def pos_tagging(self, sentence):
        splitted = self.split_sentence(sentence)
        return nltk.pos_tag(self, splitted)

    # Returns a list of nouns (NN) in a pos-tagged sentence
    def extract_objects(self, pos_tagged_sentence):
        obj_lst=[]
        for tagged_word in pos_tagged_sentence:
            if(tagged_word[1]=="NN"):
                obj_lst.append(tagged_word[0])
        return obj_lst

    # Alternative: Returns a dictionary with pos-tags as keys
    # and list of corresponding words as values 
    def generate_pos_dict(self, pos_tagged_sentence):
        pos_dict = defaultdict(list)
        for word in pos_tagged_sentence:
            pos_dict[word[1]].append(word[0])
        return pos_dict

    def test(self, sentence_lst):
        for sentence in sentence_lst:
            print(sentence)
            print(self.split_sentence(sentence))
            print(self.pos_tagging(sentence))
            print(self.extract_objects(self.pos_tagging(sentence)))
            print()
    pass