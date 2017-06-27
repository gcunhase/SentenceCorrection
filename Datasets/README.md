
# Incorrect Sentences Dataset

## First Solution: Q&A Data
Firstly, we tried to build an Incorrect Sentences Dataset by translating an existing Q&A dataset from Korean to English hoping that the English sentences obtained from such translation would be incorrect enough for us to achieve our goal. The original Q&A dataset already provided us with the corresponding correct English sentences.

The files used for this were:
* *Data-QnA*: folder containing (*Dataset.zip*), final results (*input1.en* and *output1.fr*) and necessary scripts used solely for this solution.
* *mtranslate-master*: translates files necessary to build the Dataset for our Language Correction model.
* *separate_train_test_data.py*: Python script to separate train and test data (80 and 20% respectively), includes optional shuffle function to shuffle sentences in the file. Obs: original data is formed by 40 files. In order to use this script, one has to first concatenate them all in one (*en_clean* should form 1 single file named *output1.en* and *en_translated_by_python* should form 1 single file named *input1.fr*).


#### Limitations
The problem with this dataset was that the goal of a Q&A task is too different from ours. There's no variety in a Q&A task and the sentences are very short. The same set of nouns and verbs are constantly being repeated, and that results in an extremely limited vocabulary. This is illustrated in the example below.

```
John traveled in the corridor.
Mary traveled to the bathroom.
Daniel went back to the bathroom.
John moves into the bedroom.
John went to the hallway.
Sandra travels to the kitchen.
Sandra travels in the corridor.
...
```

## Second Solution: WMT '15 Translated Data
The second solution found was to use the WMT '15 English-to-French dataset, which is in a more human-like text format, to perform a French-Korean-English translation in order to obtain the desired wrong sentences data.

#### Limitations
Translation bounded


## Third Solution: POS-Tagging of WMT'15 English Data


