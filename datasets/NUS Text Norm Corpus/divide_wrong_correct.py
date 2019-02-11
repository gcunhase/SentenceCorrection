#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Divides NUS Social Media Text Normalization and
#  Translation Corpus into 2 textfiles with wrong
#  and correct english respectively
# Corpus source: http://www.comp.nus.edu.sg/~nlp/corpora.html
#
# Dataset is actually to transform text messages into more
#  understandable english, but not necessarily correct
#
# Author: Gwena Cunha
# Date: June 28th 2017

def main():
    
    text_filename = 'en2cn-2k.en2nen2cn'
    text_file = open(text_filename,"r") 
    
    wrong_english_path = 'wrong_english.txt'
    wrong_file = open(wrong_english_path, 'w')
    
    correct_english_path = 'correct_english.txt'
    correct_file = open(correct_english_path, 'w')

    line_count = 1
    for sentence in text_file:
        if (line_count % 3 == 1): #wrong
            wrong_file.write(sentence)
        elif (line_count % 3 == 2): #right
            correct_file.write(sentence)
            
        line_count = line_count + 1

    text_file.close()
    wrong_file.close()
    correct_file.close()

if __name__ == "__main__":    
    main()
    
