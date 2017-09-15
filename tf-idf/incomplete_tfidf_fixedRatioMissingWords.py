#
# Script to make missing words dataset using the TF-IDF module to decide on important and non-important words
#  Approach: delete a fixed ratio of words, say 10%, from each story file
#    
# Author: Gwena Cunha
#
# Date: Sep 15th 2017
# 


from shutil import copyfile
import tfidf
import copy, os
import re, glob
import random

DICT_FILENAME = "dictionary_docs"
DICT_PICKLE_FILENAME = DICT_FILENAME+"_pickle.txt"
PERCENTAGE_MISSING_WORDS_FROM_FILE = 0.1

'''
   Functions to save and load dictionary, same as incomplete_tfidf.py
   TODO: Maybe add to TF-IDF?
'''
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
       

'''
   Functions to get the datasets
'''
def get_datasets_missing_words_from_sentences(data, vec_x, ratio_missing):
    '''
       Input:
	      data: collection/array of sentences.
	      vec_x: ranked words
	      ratio_missing: ratio of missing words in dataset, say 10%
              
       TODO: CHANGE THIS FUNCTION to consider ratio_missing in each story file
             and not top_words in entire corpus!!!!
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


def get_missing_dataset(vec_x, ratio_missing, data_dir, new_data_dir, stories_dir):
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

        full_final_sentences = get_datasets_missing_words_from_sentences(selected_sentences, vec_x, ratio_missing)
	
	#@highlight is not modified
	for j in range(j_break, len(sentences)):
	    full_final_sentences = full_final_sentences+"\n"+sentences[j]
        
	#print(full_final_sentences)
        f_new.write(full_final_sentences)

	f.close()
	f_new.close()

def get_datasets_fromMultipleFiles_missing_words(vec_x, ratio_missing, data_dir, new_data_dir, dataset_dir):
    # Run through all files in files_cnn or dm
    if not os.path.exists(new_data_dir+dataset_dir):
        os.makedirs(new_data_dir+dataset_dir)
    get_missing_dataset(vec_x, ratio_missing, data_dir, new_data_dir, dataset_dir)    


def get_datasets_fromMultipleFiles_missing_complex_words(corpus_dict, sorted_x, ratio_missing, data_dir, cnn_dir, dailymail_dir):
    print("Dataset COMPLEX words - multiple files")
    vec_x = copy.copy(sorted_x)
    
    new_data_dir = get_new_data_dir_name(data_dir, "-missingcomplex-approach2-"+str(PERCENTAGE_ALLOW_MISSING_WORD)+"-"+str(PERCENTAGE_ALLOW_MISSING_SUBSTRING)+"rand-"+str(top_words)+"top")
    print("Modifying CNN dataset...")  
    get_datasets_fromMultipleFiles_missing_words(vec_x, ratio_missing, data_dir, new_data_dir, cnn_dir)
    print("Modifying Daily Mail dataset...")
    get_datasets_fromMultipleFiles_missing_words(vec_x, ratio_missing, data_dir, new_data_dir, dailymail_dir)

def main():
    ## CNN and daily mail multiple files .story files dataset
    data_dir = "../../data-1000/"
    cnn_dir = "cnn/stories/"
    dailymail_dir = "dailymail/stories/"
    
    #save_dict_fromMultipleFiles_on_pickle_and_file(data_dir, cnn_dir, dailymail_dir)
    total_number_words, corpus_dict, sorted_x = load_dict_from_pickle(data_dir)
    
    ## Complex dataset
    ratio_missing = 0.1 #10%
    get_datasets_fromMultipleFiles_missing_complex_words(corpus_dict, sorted_x, ratio_missing, data_dir, cnn_dir, dailymail_dir)
    
    
if __name__ == "__main__":
    main()
    
    
