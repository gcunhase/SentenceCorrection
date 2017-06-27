
# Incorrect Sentences Dataset

## First Solution: Q&A Data
Firstly, we tried to build an Incorrect Sentences Dataset by translating an existing Q&A dataset from Korean to English hoping that the English sentences obtained from such translation would be incorrect enough for us to achieve our goal. The Q&A dataset already provided us with the corresponding correct English sentences.

The files used for this were:
* *clean_data.py*: pre-processesses the original data (*en* and *kr*), which are given in the Q&A format, so as to be in the format of one sentence per line.
* *translate_sentences.py*: 
* : original Q&A dataset
* : final result

### Limitations
The problem with this dataset was that the goal of a Q&A task is too different from our goal. In a Q&A task, the same set of nouns and verbs are constantly being repeated, there's no variety, and that results in an extremely limited vocabulary. Also, sentences are very short.

Example of Q&A:
```
Include example
```

## Second Solution: WMT '15 Translated Data
The second solution found was to use the WMT '15 English-to-French dataset, which is in a more human-like text format, to perform a French-Korean-English translation in order to obtain the desired wrong sentences data.

### Limitations
Translation bounded


## Third Solution: POS-Tagging of WMT'15 English Data


