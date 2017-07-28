#
# Script to manipulate audio
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

class TfIdf:
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpus_dict = {}
        self.total_number_words = 0


    def add_docs_from_file(self, filename):
        text_file = open(filename,"r") 
        
        line_count = 1
        for sentence in text_file:
            sentence = sentence.split("\n")[0]
            self.add_doc_sentence("sent"+str(line_count), sentence)
            line_count = line_count+1
            
        text_file.close()
    
    def add_doc_sentence(self, doc_name, sentence):
        # Assume no special characters or markers
        list_of_words = sentence.split(" ")
        self.add_document(doc_name, list_of_words)

    def add_document(self, doc_name, list_of_words):
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
            doc_dict[w] = doc_dict.get(w, 0.) + 1.0
            self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0
            self.total_number_words = self.total_number_words+1                
            
        
        # normalizing the dictionary
        length = float(len(list_of_words))
        for k in doc_dict:
            doc_dict[k] = doc_dict[k] / length


        # add the normalized document to the corpus
        self.documents.append([doc_name, doc_dict])
        
        
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

    def save_dictionary_in_file(self, filename):
        print("TODO: perform saving")
        words = "# words: "+str(self.total_number_words)
        print(words)
        dist_words = "# distinct words: "+str(len(self.corpus_dict))
        print(dist_words)
        #print("# mean frequency")
        #print("# standard deviation")
        #Sort dictionary from most to less frequent occurrences
        # It is not possible to sort a dict, only to get a representation of a
        #  dict that is sorted. Dicts are inherently orderless, but other types,
        #  such as lists and tuples, are not. So you need a sorted representation,
        #  which will be a list-probably a list of tuples
        sorted_x = sorted(self.corpus_dict.items(), key=operator.itemgetter(1))
        header = "Rank Word Occurrence Normalized Occurrence"
        print(header)
        info_str = ""
        for i in range(0,len(sorted_x)):
            corpus_item = sorted_x[i]
            info = str(i+1)+" "+corpus_item[0]+" "+str(corpus_item[1])+" "+str(round(corpus_item[1]/self.total_number_words, 4))
            info_str = info_str+info+"\n"
            print(info)
            
        file_str = words+"\n"+dist_words+"\n\n"+header+"\n"+info_str+"\n"
        f = open(filename+".txt", 'w')
        f.write(file_str)
        f.close()
        
        sorted_inv_x = copy.copy(sorted_x)
        sorted_inv_x.reverse()
        info_str = ""
        for i in range(0,len(sorted_inv_x)):
            corpus_item = sorted_inv_x[i]
            info = str(i+1)+" "+corpus_item[0]+" "+str(corpus_item[1])+" "+str(round(corpus_item[1]/self.total_number_words, 4))
            info_str = info_str+info+"\n"
            print(info)
        file_inv_str = words+"\n"+dist_words+"\n\n"+header+"\n"+info_str+"\n"
        f_inv = open(filename+"_inv.txt", 'w')        
        f_inv.write(file_inv_str)
        f_inv.close()
        return sorted_x
    

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