#
# Script to ...
#
# Author: Gwena Cunha
# Date: July 30th 2017
# 

import tfidf
import copy
import re
import random

CORRECT_ENGLISH_FILENAME = "correct_english.txt"
MISSING_SIMPLE_WORDS_ENGLISH_FILENAME = "missing_simple_words_english.txt"
MISSING_COMPLEX_WORDS_ENGLISH_FILENAME = "missing_complex_words_english.txt"
DICT_FILENAME = "dictionary_docs"
DICT_PICKLE_FILENAME = DICT_FILENAME+"_pickle.txt"
PERCENTAGE_ALLOW_MISSING = 0.4

def save_dict_on_pickle():
    table = tfidf.TfIdf()
    table.add_docs_from_file(CORRECT_ENGLISH_FILENAME)
    dictionary_x = table.save_dictionary(DICT_FILENAME, "pickle")

def load_dict_from_pickle():
    table = tfidf.TfIdf()
    total_number_words, corpus_dict, sorted_x = table.load_dictionary_from_pickle(DICT_PICKLE_FILENAME)
    #sorted_x.reverse()
    return total_number_words, corpus_dict, sorted_x
        
def get_datasets_missing_simple_words(corpus_dict, sorted_x):
    print("Dataset SIMPLE words")
    sorted_inv_x = copy.copy(sorted_x)
    sorted_inv_x.reverse()
    top_words = 100
    
    f = open(CORRECT_ENGLISH_FILENAME, 'r')
    f_simple = open(MISSING_SIMPLE_WORDS_ENGLISH_FILENAME, 'w')
    data = f.read().split("\n")
    for sentence in data:
        #sentence  = sentence.lower()
        print(sentence)
        for i in range(0,top_words):
            if (random.random() < PERCENTAGE_ALLOW_MISSING): #[0, 1)
                #TODO: random selection of words when multiple exist in sentence.
                #TODO: I in I'm cannot be deleted
                sentence = re.sub('\\b'+sorted_inv_x[i][0]+'\\b', '', sentence, flags=re.IGNORECASE)
        print(sentence)
        f_simple.write(sentence+"\n")
        
    f.close()
    f_simple.close()
    

def get_datasets_missing_complex_words():
    print("TODO: dataset COMPLEX words")
   
def main(): 
    #Data from pickle
    save_dict_on_pickle()
    total_number_words, corpus_dict, sorted_x = load_dict_from_pickle()
    
    #Simple and complex datasets
    get_datasets_missing_simple_words(corpus_dict, sorted_x)
#    get_datasets_missing_complex_words()
    
if __name__ == "__main__":
    main()
    
    