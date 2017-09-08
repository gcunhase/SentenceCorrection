#
# Script to make missing words dataset using the TF-IDF module to decide on important and non-important words
#
# Author: Gwena Cunha
#
# Date: July 30th 2017
# Modified: Sep 5th 2017 for SignalMedia News2News Dataset
# 


from shutil import copyfile
import tfidf
import copy, os
import re, glob
import random

CORRECT_ENGLISH_FILENAME = "newstest2013_small20.en"

INPUT_NEWS_FILENAME = "input_news.txt"
#output is the same as input #OUTPUT_NEWS_FILENAME = "output_news.txt"

MISSING_SIMPLE_WORDS_ENGLISH_FILENAME = "missing_simple_words_english.en"
MISSING_COMPLEX_WORDS_ENGLISH_FILENAME = "missing_complex_words_english.en"
DICT_FILENAME = "dictionary_docs"
DICT_PICKLE_FILENAME = DICT_FILENAME+"_pickle.txt"
#Simple
#PERCENTAGE_ALLOW_MISSING_WORD = 0.8 #0.5 #0.4
#PERCENTAGE_ALLOW_MISSING_SUBSTRING = 0.6
#Complex
PERCENTAGE_ALLOW_MISSING_WORD = 0.6
PERCENTAGE_ALLOW_MISSING_SUBSTRING = 0.4


def save_dict_fromMultipleFiles_on_pickle_and_file(data_dir, cnn_dir, dailymail_dir):
    table = tfidf.TfIdf()

    #DONE: get all files from cnn_dir and dailymail_dir    
    files_cnn = glob.glob(data_dir+cnn_dir+"*.story") #full path
    files_dailymail = glob.glob(data_dir+dailymail_dir+"*.story")

    # Adding files to dictionary
    print("Adding CNN files to dictionary...")
    for i in range(0, len(files_cnn)):
        table.add_docs_from_file(files_cnn[i])
        
    print("Adding Daily Mail files to dictionary...")
    for i in range(0, len(files_dailymail)):
        table.add_docs_from_file(files_dailymail[i])

    # Save dictionary
    print("Saving dictionary...")
    dictionary_x = table.save_dictionary(data_dir+DICT_FILENAME, "both")
    return dictionary_x

def save_dict_on_pickle_and_file():
    table = tfidf.TfIdf()
    table.add_docs_from_file(INPUT_NEWS_FILENAME)
    dictionary_x = table.save_dictionary(DICT_FILENAME, "both")
    return dictionary_x

def load_dict_from_pickle(data_dir):
    table = tfidf.TfIdf()
    total_number_words, corpus_dict, sorted_x = table.load_dictionary_from_pickle(data_dir+DICT_PICKLE_FILENAME)
    #sorted_x.reverse()
    return total_number_words, corpus_dict, sorted_x
        
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
   
def get_datasets_missing_words_from_sentences(data, vec_x, top_words):
    '''
	data = collection/array of sentences.
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

    

def get_new_data_dir_name(data_dir, extension):
    data_dir_split = data_dir.split("/")
    new_data_dir = ""
    for i in range(0, len(data_dir_split)-2):
        new_data_dir = new_data_dir+data_dir_split[i]+"/"
    new_data_dir = new_data_dir+data_dir_split[max(0, len(data_dir_split)-2)]+extension+"/"
    print("New data_dir: "+new_data_dir)
    return new_data_dir


def get_datasets_fromMultipleFiles_missing_simple_words(corpus_dict, sorted_x, top_words, data_dir, cnn_dir, dailymail_dir):
    print("Dataset SIMPLE words - multiple files")
    sorted_inv_x = copy.copy(sorted_x)
    sorted_inv_x.reverse()
    vec_x = sorted_inv_x
    #top_words = 100    

    #DONE: new folder data-missingsimple/
    new_data_dir = get_new_data_dir_name(data_dir, "-missingsimple")
    get_datasets_fromMultipleFiles_missing_words(vec_x, top_words, data_dir, new_data_dir, cnn_dir, dailymail_dir)
    

def get_datasets_fromMultipleFiles_missing_complex_words(corpus_dict, sorted_x, top_words, data_dir, cnn_dir, dailymail_dir):
    print("Dataset COMPLEX words - multiple files")
    vec_x = copy.copy(sorted_x)
    
    #DONE: new folder data-missingcomplex/
    new_data_dir = get_new_data_dir_name(data_dir, "-missingcomplex")
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

    data_dir = "/data/Gwena/cnn-dm-data/" #"../../data/"
    cnn_dir = "cnn/stories/"
    dailymail_dir = "dailymail/stories/"
    
    ## Subset of data
    #n_files = 1000 
    #data_dir = "../../data/"
    #multiple_files_sample(data_dir, cnn_dir, n_files)
    #multiple_files_sample(data_dir, dailymail_dir, n_files)

    #save_dict_fromMultipleFiles_on_pickle_and_file(data_dir, cnn_dir, dailymail_dir)
    total_number_words, corpus_dict, sorted_x = load_dict_from_pickle(data_dir)
    
    ## Simple dataset
    top_words = 100
    #get_datasets_fromMultipleFiles_missing_simple_words(corpus_dict, sorted_x, top_words, data_dir, cnn_dir, dailymail_dir)

    ## Complex dataset
    #top_words_complex = len(corpus_dict) - top_words*top_words #min(len(corpus_dict), top_words*top_words)
    top_words_complex = 100000 #len(corpus_dict) = 503,680
    get_datasets_fromMultipleFiles_missing_complex_words(corpus_dict, sorted_x, top_words_complex, data_dir, cnn_dir, dailymail_dir)
    print("Total number words: "+str(len(corpus_dict))+"; Top words complex: "+str(top_words_complex))


def main():
    ## Singla media dataset
    #single_file()
    
    ## CNN and daily mail multiple files .story files dataset
    multiple_files()
    
if __name__ == "__main__":
    main()
    
    
