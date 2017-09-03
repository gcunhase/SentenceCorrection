
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
The second solution found was to use the [WMT '15 English-to-French dataset](http://www.statmt.org/wmt15/translation-task.html), which is in a more human-like text format, to perform a French-Korean-English translation in order to obtain the desired wrong sentences data, using Korean as a pivot language.

![Pivot Language Translation](https://github.com/gcunhase/LanguageCorrection/blob/master/images/translationPivotLanguage.png "Pivot Language Translation")


#### Limitations
Translation bound


## Third Solution: POS-Tagging of WMT'15 English Data
The original data consists of 22,000,000 sentences of various lengths totaling about 20GB of disk space. However, MTGRU’s performance can be better observed in longer sentences. So, for this purpose, we consider only sentences that consist of 15 to 20 words, giving us a total of 3,000,000 sentences. The *target data* is said subset of the available English document.

As for the *input data*, it is a modification of the target data using Python’s Natural Language Toolkit ([NLTK](http://www.nltk.org/)) which allows for part-of-speech tagging, or POS-tagging, of words. In other terms, it allows for words to be classified into their respective lexical categories. After the tagging of words is completed, we choose a tagset that is considered irrelevant to be randomly deleted from sentences and thus form the incomplete dataset that we need. The tagset chosen, as well as each tags respective meaning and example, is displayed in the table below. In order to obtain the train and test data for both the target and input dataset, we divide each of them into 80 and 20% of the total data respectively.

<p align="center">

| Tag        | Meaning           | Example  |
| ------------- |:-------------:|:-----:|
| CC | coordinating conjunction | *and* |
| DT | determiner | *the* |
| IN | preposition/subordinating conjunction | *in, of, for, like* |
| LS | list marker | *1)* |
| TO | to	| *go 'to' the store* |
| UH | interjection | *errrrrrrrm* |

<\p>

