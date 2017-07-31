#
# Script to manipulate audio
#
# Modified by: Gwena Cunha
# Date: July 26th 2017
# 
# Source: https://github.com/hrs/python-tf-idf
# 

import tfidf
import unittest


class TestTfIdf(unittest.TestCase):
    '''
    def test_similarity(self):
        table = tfidf.TfIdf()
        table.add_document("foo", ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "kilo"])
        table.add_document("bar", ["alpha", "bravo", "charlie", "india", "juliet", "kilo"])
        table.add_document("baz", ["kilo", "lima", "mike", "november"])
        print table.similarities(["alpha", "bravo", "charlie"]) # => [['foo', 0.6875], ['bar', 0.75], ['baz', 0.0]]

    def test_dictionary(self):
        table = tfidf.TfIdf()
        table.add_document("foo", ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "kilo"])
        table.add_document("bar", ["alpha", "bravo", "charlie", "india", "juliet", "kilo"])
        table.add_document("baz", ["kilo", "lima", "mike", "november"])
        dictionary_x = table.save_dictionary_in_file("dictionary")
        print(dictionary_x)
    
    def test_add_doc_sentences(self):
        table = tfidf.TfIdf()        
        table.add_doc_sentence("sent1", "Do you want me to reserve seat for you or not")
        table.add_doc_sentence("sent2", "They become more expensive already")
        table.add_doc_sentence("sent3", "Mine is like 25")
        table.add_doc_sentence("sent4", "So horrible and they did less things than I did last time")        
        table.add_doc_sentence("sent5", "I'm Thai")
        table.add_doc_sentence("sent5", "What do you do")        
        dictionary_x = table.save_dictionary_in_file("dictionary2")
        print(dictionary_x)
        
#How did your week go?
#Haven't heard from you for some time.
#Look for it on the glass table in front of TV.
#Okay, see you next time then.
#I am Ellen, 18 years old, Chinese, from KL.

    def test_add_docs_from_file(self):
        table = tfidf.TfIdf()
        table.add_docs_from_file("correct_english.txt")
        dictionary_x = table.save_dictionary_in_file("dictionary_docs_from_file")
        print(dictionary_x)
    '''        
    
#    def test_datasets_test_train_simple_words(self):

    def test_save_tfidftable_on_pickle(self):
        table = tfidf.TfIdf()
        table.add_docs_from_file("correct_english.txt")
        dictionary_x = table.save_dictionary("dictionary_docs", "pickle")
        
        total_number_words, corpus_dict, sorted_x = table.load_dictionary_from_pickle("dictionary_docs_pickle.txt")
        print(total_number_words)
        #sorted_x.reverse()
        print(sorted_x)       
        

#    def test_datasets_test_train_complex_words(self):

if __name__ == "__main__":
    unittest.main()
    
 
