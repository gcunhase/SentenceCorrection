# LanguageCorrection
The goal of this project is to correct wrong english sentences


* *mtranslate-master*: translates files necessary to build the Dataset for our Language Correction model.
* *Dataset.zip*: compressed folder including original data, cleaned data and translated data.
* *clean_data.py*: pre-processese the original data (*en* and *kr*), which are given in the Q&A format, so as to be in the format of one sentence per line.
* *separate_train_test_data.py*: Python script to separate train and test data (80 and 20% respectively), includes optional shuffle function to shuffle sentences in the file. Obs: original data is formed by 40 files. In order to use this script, one has to first concatenate them all in one (*en_clean* should form 1 single file named *output1.en* and *en_translated_by_python* should form 1 single file named *input1.fr*)
