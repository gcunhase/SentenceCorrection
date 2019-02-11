
## Data
* *Dataset.zip*: compressed folder including original data, cleaned data and translated data.
* *input1.en* and *output1.fr*: used by *separate_train_test_data.py* to obtain all the files necessary in the tensorflow's translation model

## Scripts
* *clean_data.py*: pre-processesses the original data (*en* and *kr*), which are given in the Q&A format, so as to be in the format of one sentence per line.
* *add_dot.py*: after translation, some sentences don't include a stop sign at the end, so this script aims to do that.
