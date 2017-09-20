#
# Script to make missing words dataset using the TF-IDF module to decide on important and non-important words
#
# Author: Gwena Cunha
#
# Date: July 30th 2017
# Modified: Sep 5th 2017 for SignalMedia News2News Dataset
# Modified: Sep 19th for real tf-idf (before we were using just df)
# 


from shutil import copyfile
import tfidf
import copy, os
import re, glob
import random
from math import floor
from timeit import default_timer as timer

CORRECT_ENGLISH_FILENAME = "newstest2013_small20.en"

INPUT_NEWS_FILENAME = "input_news.txt"
#output is the same as input #OUTPUT_NEWS_FILENAME = "output_news.txt"

MISSING_SIMPLE_WORDS_ENGLISH_FILENAME = "missing_simple_words_english.en"
MISSING_COMPLEX_WORDS_ENGLISH_FILENAME = "missing_complex_words_english.en"
DICT_FILENAME = "dictionary_docs"
DICT_PICKLE_FILENAME = DICT_FILENAME+"_pickle.txt"
#Simple
PERCENTAGE_ALLOW_MISSING_WORD = 0.4 #0.8 #0.5 #0.4
PERCENTAGE_ALLOW_MISSING_SUBSTRING = 0.3 #0.6
#Complex
#PERCENTAGE_ALLOW_MISSING_WORD = 0.6
#PERCENTAGE_ALLOW_MISSING_SUBSTRING = 0.4

'''
   Functions to save and load dictionary, same as incomplete_tfidf.py
   TODO: Maybe add to TF-IDF?
'''
def save_dict_fromMultipleFiles_on_pickle_and_file(data_dir, cnn_dir, dailymail_dir):
    table = tfidf.TfIdf()

    #DONE: get all files from cnn_dir and dailymail_dir    
    #files_cnn = glob.glob(data_dir+cnn_dir+"*.story") #full path
    #files_dailymail = glob.glob(data_dir+dailymail_dir+"*.story")
    files_cnn = [f for f in os.listdir(data_dir+cnn_dir) if f.endswith('.story')] #relative path
    files_dailymail = [f for f in os.listdir(data_dir+dailymail_dir) if f.endswith('.story')]
    
    new_data_dir = get_new_data_dir_name(data_dir, "-tfidf")
    # Adding files to dictionary
    print("Adding CNN files to dictionary...")
    for i in range(0, len(files_cnn)):
        table.add_docs_from_file(data_dir, cnn_dir, files_cnn[i], new_data_dir)
        
    print("Adding Daily Mail files to dictionary...")
    for i in range(0, len(files_dailymail)):
        table.add_docs_from_file(data_dir, dailymail_dir, files_dailymail[i], new_data_dir)

    # Save dictionary
    print("Saving dictionary...")
    table.save_dictionary(data_dir+DICT_FILENAME, "both")
    return new_data_dir
    
def save_dict_on_pickle_and_file():
    table = tfidf.TfIdf()
    table.add_docs_from_file(INPUT_NEWS_FILENAME)
    dictionary_x = table.save_dictionary(DICT_FILENAME, "both")
    return dictionary_x

def load_dict_from_pickle(data_dir):
    table = tfidf.TfIdf()
    total_number_words, corpus_dict, sorted_x, documents = table.load_dictionary_from_pickle(data_dir+DICT_PICKLE_FILENAME)
    #sorted_x.reverse()
    return total_number_words, corpus_dict, sorted_x, documents
        
def load_single_file_dict_from_pickle(new_data_dir, dataset_dir, filename):
    table = tfidf.TfIdf()
    words_in_doc, sorted_doc_inv_x = table.load_single_file_dictionary_from_pickle(new_data_dir, dataset_dir, filename)
    #sorted_x.reverse()
    return words_in_doc, sorted_doc_inv_x
        
        
def get_datasets_missing_simple_words(corpus_dict, sorted_x, top_words):
    print("Dataset SIMPLE words")
    sorted_inv_x = copy.copy(sorted_x)
    sorted_inv_x.reverse()
    #top_words = 100    
    get_datasets_missing_words(corpus_dict, sorted_inv_x, CORRECT_ENGLISH_FILENAME, MISSING_SIMPLE_WORDS_ENGLISH_FILENAME, top_words)
    
def get_datasets_missing_complex_words(corpus_dict, sorted_x, top_words):
    print("Dataset COMPLEX words")
    #top_words = 2995    
    sorted_x_copy = copy.copy(sorted_x)
    get_datasets_missing_words(corpus_dict, sorted_x_copy, CORRECT_ENGLISH_FILENAME, MISSING_COMPLEX_WORDS_ENGLISH_FILENAME, top_words)
    
def get_datasets_missing_words(corpus_dict, vec_x, correct_english_path, missing_path, top_words):
    
    f = open(correct_english_path, 'r')
    f_simple = open(missing_path, 'w')
    data = f.read().split("\n")

    full_final_sentence = get_datasets_missing_words_from_sentences(data, vec_x, top_words)
    f_simple.write(full_final_sentence)
  
    f.close()
    f_simple.close()
   
'''
   Functions to get the datasets
'''
def get_datasets_missing_words_from_sentences(data, vec_x, top_words):
    '''
       Input:
	      data: collection/array of sentences.
	      vec_x: ranked words
	      top_words: top words to consider
          #ratio_missing: ratio of missing words in dataset, say 10%
    '''
    count = 0
    full_final_sentence = ""
    for sentence in data:
        sentence = sentence.lower()
        #print("SENTENCE: "+sentence+"\n")
        for i in range(0,top_words):
            if (random.random() < PERCENTAGE_ALLOW_MISSING_WORD): #[0, 1)
                word = vec_x[i][0]
                #print("\nWORD "+str(i)+": "+ word)
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
        full_final_sentence = full_final_sentence+sentence
        
        #print(sentence)
        count = count+1

    return full_final_sentence        

def get_missing_dataset(vec_x, top_words, data_dir, new_data_dir, stories_dir):
    '''
       Gets part of string that needs to be modified (before @highlight)
    '''
    
    files = [f for f in os.listdir(data_dir+stories_dir) if f.endswith('.story')]
    for i in range(0, len(files)):
        print("File %d: %s" % (i, files[i]))
        #DONE: read sentences in file, break when you read first @highlight
        tag = "@highlight"
        f = open(data_dir+stories_dir+files[i], 'r')
        f_new = open(new_data_dir+stories_dir+files[i], 'w')
        sentences = f.read().split("\n")
        selected_sentences = []
        j_break = 0
        for j in range(0, len(sentences)):
            if (tag in sentences[j]):
                 j_break = j
                 break;
            else:
                 #missing_filename = same as correct_english_filename, differing only on data_dir
                 selected_sentences.append(sentences[j])

        full_final_sentences = get_datasets_missing_words_from_sentences(selected_sentences, vec_x, top_words)
    
        #@highlight is not modified
        for j in range(j_break, len(sentences)):
            full_final_sentences = full_final_sentences+"\n"+sentences[j]
            
        #print(full_final_sentences)
        f_new.write(full_final_sentences)

    f.close()
    f_new.close()
     

def get_news_and_abstract_files(data_dir, new_data_dir_abs_news, stories_dir):
    
    if not os.path.exists(new_data_dir_abs_news+stories_dir):
        os.makedirs(new_data_dir_abs_news+stories_dir)
    
    files = [f for f in os.listdir(data_dir+stories_dir) if f.endswith('.story')]
    for i in range(0, len(files)):
     tag = "@highlight"
     f = open(data_dir+stories_dir+files[i], 'r')
     f_news = open(new_data_dir_abs_news+stories_dir+files[i].split('.story')[0]+"-news.story", 'w')
     f_abs = open(new_data_dir_abs_news+stories_dir+files[i].split('.story')[0]+"-abs.story", 'w')
     sentences = f.read().split("\n")
     news_sentences = ""
     j_break = 0
     for j in range(0, len(sentences)):
        if (tag in sentences[j]):
             j_break = j
             break;
        else:
             news_sentences = news_sentences + "\n" + sentences[j]

     abs_sentences = ""
     for j in range(j_break, len(sentences)):
          if (tag not in sentences[j]):
             abs_sentences = abs_sentences+"\n"+sentences[j]
        
     #print(full_final_sentences)
     f_news.write(news_sentences)
     f_abs.write(abs_sentences)  

     f.close()
     f_news.close()
     f_abs.close()

def get_new_data_dir_name(data_dir, extension):
    data_dir_split = data_dir.split("/")
    new_data_dir = ""
    for i in range(0, len(data_dir_split)-2):
        new_data_dir = new_data_dir+data_dir_split[i]+"/"
    new_data_dir = new_data_dir+data_dir_split[max(0, len(data_dir_split)-2)]+extension+"/"
    print("New data_dir: "+new_data_dir)
    return new_data_dir


def get_datasets_fromMultipleFiles_missing_simple_words(sorted_x, top_words, data_dir, cnn_dir, dailymail_dir):
    print("Dataset SIMPLE words - multiple files")
    sorted_inv_x = copy.copy(sorted_x)
    sorted_inv_x.reverse()
    vec_x = sorted_inv_x
    #top_words = 100    

    #DONE: new folder data-missingsimple/
    new_data_dir = get_new_data_dir_name(data_dir, "-missingsimple-"+str(PERCENTAGE_ALLOW_MISSING_WORD)+"-"+str(PERCENTAGE_ALLOW_MISSING_SUBSTRING)+"rand-"+str(top_words)+"top")
    get_datasets_fromMultipleFiles_missing_words(vec_x, top_words, data_dir, new_data_dir, cnn_dir, dailymail_dir)
    

def get_datasets_fromMultipleFiles_missing_complex_words(sorted_x, top_words, data_dir, cnn_dir, dailymail_dir):
    print("Dataset COMPLEX words - multiple files")
    vec_x = copy.copy(sorted_x)
    
    #DONE: new folder data-missingcomplex/
    new_data_dir = get_new_data_dir_name(data_dir, "-missingcomplex-"+str(PERCENTAGE_ALLOW_MISSING_WORD)+"-"+str(PERCENTAGE_ALLOW_MISSING_SUBSTRING)+"rand-"+str(top_words)+"top")
    get_datasets_fromMultipleFiles_missing_words(vec_x, top_words, data_dir, new_data_dir, cnn_dir, dailymail_dir)


def get_datasets_fromMultipleFiles_missing_words(vec_x, top_words, data_dir, new_data_dir, cnn_dir, dailymail_dir):
    # Run through all files in files_cnn  
    if not os.path.exists(new_data_dir+cnn_dir):
        os.makedirs(new_data_dir+cnn_dir)
    print("Modifying CNN dataset...")  
    get_missing_dataset(vec_x, top_words, data_dir, new_data_dir, cnn_dir)
    
    # Run through all files in files_dailymail  
    if not os.path.exists(new_data_dir+dailymail_dir):
        os.makedirs(new_data_dir+dailymail_dir)
    print("Modifying Daily Mail dataset...")
    get_missing_dataset(vec_x, top_words, data_dir, new_data_dir, dailymail_dir) 




'''
    Real TF-IDF
'''


def get_datasets_fromMultipleFiles_missing_complex_words_fixedRatioPercentage(percentage_missing_words_per_file, data_dir, docs_dic_dir, cnn_dir, dailymail_dir):
    print("Dataset COMPLEX words - multiple files - percentage")
    
    new_data_dir = get_new_data_dir_name(data_dir, "-missingcomplex-"+str(percentage_missing_words_per_file)+"perc")
    get_datasets_fromMultipleFiles_missing_words_fixedRatioPercentage(percentage_missing_words_per_file, data_dir, docs_dic_dir, new_data_dir, cnn_dir, dailymail_dir)

def get_datasets_fromMultipleFiles_missing_words_fixedRatioPercentage(percentage_missing_words_per_file, data_dir, docs_dic_dir, new_data_dir, cnn_dir, dailymail_dir):
    # Run through all files in files_cnn  
    if not os.path.exists(new_data_dir+cnn_dir):
        os.makedirs(new_data_dir+cnn_dir)
    print("Modifying CNN dataset...")  
    get_missing_dataset_fixedRatioPercentage(percentage_missing_words_per_file, data_dir, docs_dic_dir, new_data_dir, cnn_dir)
    
    # Run through all files in files_dailymail  
    if not os.path.exists(new_data_dir+dailymail_dir):
        os.makedirs(new_data_dir+dailymail_dir)
    print("Modifying Daily Mail dataset...")
    get_missing_dataset_fixedRatioPercentage(percentage_missing_words_per_file, data_dir, docs_dic_dir, new_data_dir, dailymail_dir) 


def get_missing_dataset_fixedRatioPercentage(percentage_missing_words_per_file, data_dir, docs_dic_dir, new_data_dir, stories_dir):
    files = [f for f in os.listdir(data_dir+stories_dir) if f.endswith('.story')]
    all_files_log_info = ""
    for i in range(0, len(files)):
       filename = files[i] 
       print("File %d: %s" % (i, filename))
       #DONE: read sentences in file, break when you read first @highlight
       tag = "@highlight"
       f = open(data_dir+stories_dir+filename, 'r')
       f_new = open(new_data_dir+stories_dir+filename, 'w')
   
       words_in_doc, sorted_doc_inv_x = load_single_file_dict_from_pickle(docs_dic_dir, stories_dir, filename)
       
   
       sentences = f.read().split("\n")
       selected_sentences = []
       j_break = 0
       for j in range(0, len(sentences)):
          if (tag in sentences[j]):
              j_break = j
              break;
          else:
              #missing_filename = same as correct_english_filename, differing only on data_dir
              selected_sentences.append(sentences[j])
    
       full_final_sentences, log_info = get_datasets_missing_words_from_sentences_fixedRatioPercentage(selected_sentences, percentage_missing_words_per_file, words_in_doc, sorted_doc_inv_x)
       all_files_log_info = all_files_log_info + "File: "+filename+"\n"+log_info+"\n"
       
       #@highlight is not modified
       for j in range(j_break, len(sentences)):
          full_final_sentences = full_final_sentences+"\n"+sentences[j]
        
       #print(full_final_sentences)
       f_new.write(full_final_sentences)


       f.close()
       f_new.close()
    
    print("Saving log missing...")
    f_log = open(new_data_dir+"log_missing_"+stories_dir.split("/")[0]+".txt", 'w')    
    f_log.write(all_files_log_info)
    f_log.close()
    
    
    
def get_datasets_missing_words_from_sentences_fixedRatioPercentage(data, percentage_missing_words_per_file, words_in_doc, sorted_doc_inv_x):
    '''
     data = collection/array of sentences.
    '''
    
    words_to_be_missing = int(min(floor(percentage_missing_words_per_file*words_in_doc), words_in_doc))
    allow_missing = 1
    count = 0
    count_missing_words = 0
    full_final_sentence = ""
    for sentence in data:
        sentence = sentence.lower()
        #print("SENTENCE: "+sentence+"\n")
        for i in range(0, words_to_be_missing):
            word = sorted_doc_inv_x[i][0]
            #print("\nWORD "+str(i)+": "+ word)
            exact_word = '\\b'+word+'\\b'
            ## Subs all words in sentence                   
            sentence, n = re.subn(exact_word, '', sentence, flags=re.IGNORECASE)
            count_missing_words = count_missing_words + n                    
            
            
            #sent_split = re.split(exact_word, sentence)
            #final_sentence = sent_split[0]                
            #for j in range(1, len(sent_split)-1):
            #    if (random.random() < allow_missing): # missing word
            #        print("missing")
            #        final_sentence = final_sentence+sent_split[j]
            #        count_missing_words = count_missing_words + 1
            #    else: # scramble word
            #        final_sentence = final_sentence+word+sent_split[j]
            #if (len(sent_split)-1 > 0):
            #   final_sentence = final_sentence+sent_split[len(sent_split)-1]                
            #sentence = final_sentence                 
            
            
        if (count != 0): # Avoids last paragraph to have an extra empty line
            sentence = "\n"+sentence
        full_final_sentence = full_final_sentence+sentence
        
        count = count+1

    log_info = "Words in doc: "+str(words_in_doc)+" - Min words missing: "+str(words_to_be_missing)+" - Missing: "+str(count_missing_words)
    #print(log_info)
    #TODO: save in log file min missing words and actual missing words

    return full_final_sentence, log_info


'''
    Single vs Multiple files
'''
    
def single_file():
    ## Data from pickle
    #save_dict_on_pickle_and_file()
    data_dir = "./"
    total_number_words, corpus_dict, sorted_x = load_dict_from_pickle(data_dir)
    
    ## Simple and complex datasets
    top_words = 100
    #get_datasets_missing_simple_words(corpus_dict, sorted_x, top_words)
    top_words_complex = len(corpus_dict) - top_words*top_words #min(len(corpus_dict), top_words*top_words)
    get_datasets_missing_complex_words(corpus_dict, sorted_x, top_words_complex)
    print("Total number words: "+str(len(corpus_dict))+"; Top words complex: "+str(top_words_complex))
    
def multiple_files_sample(data_dir, dataset_dir, n_files):
    #n_data_dir = "../../data-"+str(n_files)+"/"
    n_data_dir = get_new_data_dir_name(data_dir, "-"+str(n_files))
    print("New data_dir: "+n_data_dir)
    
    files = [f for f in os.listdir(data_dir+dataset_dir) if f.endswith('.story')] #relative path
    #files = glob.glob(data_dir+cnn_dir+"*.story") #full path
    if not os.path.exists(n_data_dir+dataset_dir):
        os.makedirs(n_data_dir+dataset_dir)
    for i in range(0, min(n_files, len(files))):
        src = data_dir+dataset_dir+files[i]
        dst = n_data_dir+dataset_dir+files[i]
        copyfile(src, dst)

def multiple_files():

    #data_dir = "/data/Gwena/cnn-dm-data/" #"../../data/"
    cnn_dir = "cnn/stories/"
    dailymail_dir = "dailymail/stories/"
    
    ## Subset of data
    #n_files = 100 
    data_dir = "../../data-100/"
    #multiple_files_sample(data_dir, cnn_dir, n_files)
    #multiple_files_sample(data_dir, dailymail_dir, n_files)

    ## Test vocab from news and abstract
    #data_dir = "../../data-1/"
    #new_data_dir_abs_news = get_new_data_dir_name(data_dir, "-abs-news")
    #get_news_and_abstract_files(data_dir, new_data_dir_abs_news, cnn_dir)
    #get_news_and_abstract_files(data_dir, new_data_dir_abs_news, dailymail_dir)
    #save_dict_fromMultipleFiles_on_pickle_and_file(new_data_dir_abs_news, cnn_dir, dailymail_dir)
    
    
    ## Realf TF-IDF
    # Saves corpus dictionary and also each .story tf-idf files in data_dir[-tfidf]/cnn/stories/[filename].tfidf
    start_time = timer()
    new_data_dir = save_dict_fromMultipleFiles_on_pickle_and_file(data_dir, cnn_dir, dailymail_dir)
    print(new_data_dir)

    total_number_words, corpus_dict, sorted_x, documents = load_dict_from_pickle(data_dir)
    
    ## Simple dataset
    #top_words = 100
    #get_datasets_fromMultipleFiles_missing_simple_words(sorted_x, top_words, data_dir, cnn_dir, dailymail_dir)
    
    ## Complex dataset
    percentage_missing_words_per_file = 0.1
    docs_dic_dir = documents[0][1]
    get_datasets_fromMultipleFiles_missing_complex_words_fixedRatioPercentage(percentage_missing_words_per_file, data_dir, docs_dic_dir, cnn_dir, dailymail_dir)

    end_time = timer() - start_time
    print("Program took %f seconds" % end_time)    
    
    '''    
    ## Complex dataset
    ##top_words_complex = len(corpus_dict) - top_words*top_words #min(len(corpus_dict), top_words*top_words)
    #top_words_complex = 100000 #len(corpus_dict) = 503,680
    #get_datasets_fromMultipleFiles_missing_complex_words(sorted_x, top_words_complex, data_dir, cnn_dir, dailymail_dir)
    '''

def main():
    ## Single media dataset
    #single_file()
    
    ## CNN and daily mail multiple files .story files dataset
    multiple_files()
    
if __name__ == "__main__":
    main()
    
    
