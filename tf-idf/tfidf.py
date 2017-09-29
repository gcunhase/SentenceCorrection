#
# Modified by: Gwena Cunha
# Date: July 26th 2017
#
# Source: https://github.com/hrs/python-tf-idf
# 

"""The simplest TF-IDF library imaginable.

Add your documents as two-element lists `[docname,[list_of_words_in_the_document]]`
with `addDocument(docname, list_of_words)`.

Get a list of all the `[docname, similarity_score]` pairs relative to a
document by calling `similarities([list_of_words])`.

See the README for a usage example.

"""

import sys
import os
import operator
import string, copy
import pickle
import re
from math import log10

class TfIdf:
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpus_dict = {}
        self.n_doc_words_appearance = {}
        self.total_number_words = 0


    def add_docs_from_file(self, data_dir, dataset_dir, filename, new_data_dir):
        #DONE: send all sentences as one
        text_file = open(data_dir+dataset_dir+filename,"r") 
        all_sents = ""
        for sentence in text_file:
            sentence = sentence.split("\n")[0]
            all_sents = all_sents+sentence+" "

        self.add_doc_sentence(data_dir, dataset_dir, filename, all_sents, new_data_dir)            
        text_file.close()

    
    def add_doc_sentence(self, data_dir, dataset_dir, doc_name, sentence, new_data_dir):
        # Assume no special characters or markers
        # Old way of getting words
        #list_of_words = sentence.split(" ")
        # New way of getting words: https://stackoverflow.com/questions/6181763/converting-a-string-to-a-list-of-words
        list_of_words = re.sub("[^\w]", " ",  sentence).split()
        self.add_document(data_dir, dataset_dir, doc_name, list_of_words, new_data_dir)

    def add_document(self, data_dir, dataset_dir, doc_name, list_of_words, new_data_dir):
        #Already being done: DF - most important words in corpus
        #DONE: documents.append - Implement TF x IDF for a document (and rank according to that value to get the most important words in file)
   
        #Lower or Upper case doesn't matter
        #Remove all special punctuation from word: https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        table = string.maketrans("","")
        for i in range(0, len(list_of_words)):
            list_of_words[i] = list_of_words[i].lower().translate(table, string.punctuation)

        # building a dictionary.
        # Count the number of occurrences of each character: if it already has
        #  a count for a given character, get returns it (so it's just incremented
        #  by one), else get returns 0 (so the incrementing correctly gives 1 at
        #  a character's first occurrence in the string).
        doc_dict = {}
        for w in list_of_words:
            if (doc_dict.get(w, 0.) == 0.):
		self.n_doc_words_appearance[w] = self.n_doc_words_appearance.get(w, 0) + 1
            doc_dict[w] = doc_dict.get(w, 0.) + 1.0
            self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0
            self.total_number_words = self.total_number_words+1                
            
        
        # normalizing the dictionary
        #doc_dict_norm = {}
        #length = float(len(list_of_words))
        #for k in doc_dict:
        #    doc_dict_norm[k] = doc_dict[k] / length

        
        # add the normalized document to the corpus
        self.documents.append([data_dir, new_data_dir, dataset_dir, doc_name, len(list_of_words), doc_dict])
                
    def get_dictionary(self):
        #print("\n")
        #print(list(self.corpus_dict.items()))
        return self.corpus_dict;

    def get_dictionary_normalized(self):
        total_number_words = len(self.corpus_dict)
        test = {}
        for k in self.corpus_dict:
            test[k] = self.corpus_dict[k]/total_number_words
        #print(test.items())
        return test;

    def save_dictionary(self, filename, where):
        if (where.lower() == "file"): #file
           self.save_dictionary_in_file(filename)
        elif (where.lower() == "pickle"): #pickle
           self.save_dictionary_in_pickle(filename)
        elif (where.lower() == "both"): #both
           self.save_dictionary_in_file(filename)
           self.save_dictionary_in_pickle(filename)
        else: #not found
            print("Save dictionary command not found\n")            

    def save_dictionary_in_pickle(self, filename):
        # Corpus pickle
        output = open(filename+'_pickle.txt', 'w')
        pickle.dump(self.total_number_words, output)
        pickle.dump(self.corpus_dict, output)
        sorted_x = sorted(self.corpus_dict.items(), key=operator.itemgetter(1))
        pickle.dump(sorted_x, output)
        pickle.dump(self.documents, output)
        pickle.dump(self.n_doc_words_appearance, output)
        output.close()
        
        # Documents pickle        
        N = len(self.documents)
        for i in range(0, N):
            data_dir = self.documents[i][0]
            new_data_dir = self.documents[i][1]
            dataset_dir = self.documents[i][2]
            doc_name = self.documents[i][3]
            words_in_doc = self.documents[i][4]            
            doc_dict = self.documents[i][5]
            sorted_doc_inv_x = self.tfidf_score(doc_dict, words_in_doc, N)
            
            # save tfidf dictionary in respective file
            if not os.path.exists(new_data_dir+dataset_dir):
                os.makedirs(new_data_dir+dataset_dir)
            output_doc = open(new_data_dir+dataset_dir+doc_name.split(".")[0]+"_pickle.tfidf", 'w')        
            pickle.dump(words_in_doc, output_doc)
            pickle.dump(doc_dict, output_doc)
            pickle.dump(sorted_doc_inv_x, output_doc)
            output_doc.close()
            
        

    def load_dictionary_from_pickle(self, filename):
        output = open(filename, 'rb')
        total_number_words = pickle.load(output)
        corpus_dict = pickle.load(output)
        sorted_x = pickle.load(output)
        documents = pickle.load(output) #new_data_dir+dataset_dir+doc_name.split(".")[0]+"_pickle.tfidf"
        n_doc_words_appearance = pickle.load(output)
        output.close()
        return total_number_words, corpus_dict, sorted_x, documents

    def load_single_file_dictionary_from_pickle(self, new_data_dir, dataset_dir, filename):
        output_doc = open(new_data_dir+dataset_dir+filename.split(".")[0]+"_pickle.tfidf", 'rb')
        words_in_doc = pickle.load(output_doc)
        doc_dict = pickle.load(output_doc)
        sorted_doc_inv_x = pickle.load(output_doc)
        return words_in_doc, sorted_doc_inv_x
        

    def save_dictionary_in_file(self, filename):
        
        # Save entire corpus in file
        print("Corpus...")
        words = "# words: "+str(self.total_number_words)
        #print(words)
        dist_words = "# distinct words: "+str(len(self.corpus_dict))
        #print(dist_words)
        ##print("# mean frequency")
        ##print("# standard deviation")
        ##Sort dictionary from most to less frequent occurrences
        ## It is not possible to sort a dict, only to get a representation of a
        ##  dict that is sorted. Dicts are inherently orderless, but other types,
        ##  such as lists and tuples, are not. So you need a sorted representation,
        ##  which will be a list-probably a list of tuples
        sorted_x = sorted(self.corpus_dict.items(), key=operator.itemgetter(1))
        header = "Rank - Word - Occurrence - Normalized Occurrence - Docs it appears on"
        #print(header)
        info_str = ""
        for i in range(0,len(sorted_x)):
            corpus_item = sorted_x[i]
            info = str(i+1)+" "+corpus_item[0]+" "+str(corpus_item[1])+" "+str(round(corpus_item[1]/self.total_number_words, 4)) + " " + str(self.n_doc_words_appearance.get(corpus_item[0], 0))
            info_str = info_str+info+"\n"
            #print(info)
            
        file_str = words+"\n"+dist_words+"\n\n"+header+"\n"+info_str+"\n"
        f = open(filename+".txt", 'w')
        f.write(file_str)
        f.close()
        
        sorted_inv_x = copy.copy(sorted_x)
        sorted_inv_x.reverse()
        info_str = ""
        for i in range(0,len(sorted_inv_x)):
            corpus_item = sorted_inv_x[i]
            info = str(i+1)+" "+corpus_item[0]+" "+str(corpus_item[1])+" "+str(round(corpus_item[1]/self.total_number_words, 4)) + " " + str(self.n_doc_words_appearance.get(corpus_item[0], 0))
            info_str = info_str+info+"\n"
            #print(info)
        file_inv_str = words+"\n"+dist_words+"\n\n"+header+"\n"+info_str+"\n"
        f_inv = open(filename+"_inv.txt", 'w')        
        f_inv.write(file_inv_str)
        f_inv.close()
        
        
        # Save multiple files' dictionary -> tfidf
        print("Documents...")
        #print(self.documents[0][4].items()[0][0])
        N = len(self.documents)
        for i in range(0, N):
            data_dir = self.documents[i][0]
            new_data_dir = self.documents[i][1]
            dataset_dir = self.documents[i][2]
            doc_name = self.documents[i][3]
            #print("\n"+dataset_dir+doc_name)
            words_in_doc = self.documents[i][4]            
            doc_dict = self.documents[i][5]
            
            words = "# words: "+str(words_in_doc)
            dist_words = "# distinct words: "+str(len(doc_dict))
            
            sorted_doc_inv_x = self.tfidf_score(doc_dict, words_in_doc, N)
        
            header = "Rank - Word - tfidf"
            info_str = ""
            for j in range(0,len(sorted_doc_inv_x)):
                doc_item = sorted_doc_inv_x[j]
                info = str(j+1)+" "+doc_item[0]+" "+str(doc_item[1])
                info_str = info_str+info+"\n"
                #print(info)
                   
           
            # save tfidf dictionary in respective file
            if not os.path.exists(new_data_dir+dataset_dir):
                os.makedirs(new_data_dir+dataset_dir)
            #write new_data_dir+dataset_dir
            file_str = words+"\n"+dist_words+"\n\n"+header+"\n"+info_str+"\n"
            f_doc = open(new_data_dir+dataset_dir+doc_name.split(".")[0]+".tfidf", 'w')        
            f_doc.write(file_str)
            f_doc.close()
        
                
        return sorted_x

    def save_dictionary_in_file_from_pickle(self, filename):
        print("TODO")

    def tfidf_score(self, doc_dict, words_in_doc, N):
        tfidf = {}
        for j in range(0, len(doc_dict)):
            item = doc_dict.items()[j]
            w = item[0]
            #print("word: "+w)
            tf = float(item[1]) / float(words_in_doc)
            #print("tf: "+str(tf))
            df = self.n_doc_words_appearance.get(w, 0)
            #df = self.corpus_dict.get(w)
            #print("df: "+str(df))
            #tfidf[w] = tf * log10( float(N - df + 1) / float(1 + df) )
            tfidf[w] = tf * log10( float(N) / float(1 + df) )
            #tfidf[w] = tf * log10( float(N) / float(df) )
            #print("tfidf: "+str(tfidf.get(w)))
                
        sorted_doc_inv_x = sorted(tfidf.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_doc_inv_x            
        
    def similarities(self, list_of_words):
        """Returns a list of all the [docname, similarity_score] pairs relative to a
list of words.
        """

        # building the query dictionary
        query_dict = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0

        # normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
            query_dict[k] = query_dict[k] / length

        # computing the list of similarities
        sims = []
        for doc in self.documents:
            score = 0.0
            doc_dict = doc[1]
            for k in query_dict:
                if k in doc_dict:
                    score += (query_dict[k] / self.corpus_dict[k]) + (
                      doc_dict[k] / self.corpus_dict[k])
            sims.append([doc[0], score])

        return sims

