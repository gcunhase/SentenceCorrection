#
# Script to ...
#
# Author: Gwena Cunha
#
# Date: July 30th 2017
# Modified: Sep 5th 2017 for SignalMedia News2News Dataset
# 


import tfidf
import copy
import re
import random

CORRECT_ENGLISH_FILENAME = "newstest2013_small20.en"

INPUT_NEWS_FILENAME = "input_news.txt"
#output is the same as input #OUTPUT_NEWS_FILENAME = "output_news.txt"

MISSING_SIMPLE_WORDS_ENGLISH_FILENAME = "missing_simple_words_english.en"
MISSING_COMPLEX_WORDS_ENGLISH_FILENAME = "missing_complex_words_english.en"
DICT_FILENAME = "dictionary_docs"
DICT_PICKLE_FILENAME = DICT_FILENAME+"_pickle.txt"
PERCENTAGE_ALLOW_MISSING_WORD = 1 #0.5 #0.4
PERCENTAGE_ALLOW_MISSING_SUBSTRING = 0.8

def save_dict_on_pickle_and_file():
    table = tfidf.TfIdf()
    table.add_docs_from_file(INPUT_NEWS_FILENAME)
    dictionary_x = table.save_dictionary(DICT_FILENAME, "both")
    return dictionary_x

def load_dict_from_pickle():
    table = tfidf.TfIdf()
    total_number_words, corpus_dict, sorted_x = table.load_dictionary_from_pickle(DICT_PICKLE_FILENAME)
    #sorted_x.reverse()
    return total_number_words, corpus_dict, sorted_x
        
def get_datasets_missing_simple_words(corpus_dict, sorted_x, top_words):
    print("Dataset SIMPLE words")
    sorted_inv_x = copy.copy(sorted_x)
    sorted_inv_x.reverse()
    #top_words = 100    
    get_datasets_missing_words(corpus_dict, sorted_inv_x, MISSING_SIMPLE_WORDS_ENGLISH_FILENAME, top_words)
    
def get_datasets_missing_complex_words(corpus_dict, sorted_x, top_words):
    print("Dataset COMPLEX words")
    #top_words = 2995    
    sorted_x_copy = copy.copy(sorted_x)
    get_datasets_missing_words(corpus_dict, sorted_x_copy, MISSING_COMPLEX_WORDS_ENGLISH_FILENAME, top_words)
    
def get_datasets_missing_words(corpus_dict, vec_x, missing_filename, top_words):
    
    f = open(CORRECT_ENGLISH_FILENAME, 'r')
    f_simple = open(missing_filename, 'w')
    data = f.read().split("\n")
    count = 0
    for sentence in data:
        sentence = sentence.lower()
        print("SENTENCE: "+sentence+"\n")
        for i in range(0,top_words):
            if (random.random() < PERCENTAGE_ALLOW_MISSING_WORD): #[0, 1)
                word = vec_x[i][0]
                print("\nWORD "+str(i)+": "+ word)
                exact_word = '\\b'+word+'\\b'
                # Subs all words in sentence                   
                #sentence = re.sub(exact_word, '', sentence, flags=re.IGNORECASE)

                #DONE: random selection of words when multiple exist in sentence.
                #TODO: I in I'm cannot be deleted ?                
                sent_split = re.split(exact_word, sentence)
                #print("SENT_SPLIT")
                #print(sent_split)
                final_sentence = sent_split[0]                
                for j in range(1, len(sent_split)-1):
                    if (random.random() < PERCENTAGE_ALLOW_MISSING_SUBSTRING):
                        final_sentence = final_sentence+sent_split[j]
                    else:
                        final_sentence = final_sentence+word+sent_split[j]
                if (len(sent_split)-1 > 0):
                   final_sentence = final_sentence+sent_split[len(sent_split)-1]                
                sentence = final_sentence                
        
        if (count != 0): # Avoids last paragraph to have an extra empty line
            sentence = "\n"+sentence
        f_simple.write(sentence)
        
        print(sentence)
        count = count+1
        
        
    f.close()
    f_simple.close()
   
   
def main(): 
    ## Data from pickle
    #save_dict_on_pickle_and_file()
    total_number_words, corpus_dict, sorted_x = load_dict_from_pickle()
    
    ## Simple and complex datasets
    top_words = 100
    #get_datasets_missing_simple_words(corpus_dict, sorted_x, top_words)
    top_words_complex = len(corpus_dict) - top_words*top_words #min(len(corpus_dict), top_words*top_words)
    get_datasets_missing_complex_words(corpus_dict, sorted_x, top_words_complex)
    print("Total number words: "+str(len(corpus_dict))+"; Top words complex: "+str(top_words_complex))
    
if __name__ == "__main__":
    main()
    
    
