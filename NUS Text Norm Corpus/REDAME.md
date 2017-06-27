
## NUS Social Media Text Normalization and Translation Corpus Modified


### Files
* _en2cn-2k.en2nen2cn_: [original corpus](http://www.comp.nus.edu.sg/~nlp/corpora.html), containing 2,000 sentences of wrong english, correct english and chinese each interlaced. Example:
```javascript
U wan me to "chop" seat 4 u nt?
Do you want me to reserve seat for you or not?
你要我帮你预留坐位吗？
```
* _divide_wrong_correct.py_: Python script to divide original corpus into wrong and correct English (every other 1st and 2nd sentences)
* _wrong_english.txt_ and _correct_english.txt_: resulting dataset
* _NUS_README_: original README that came with the dataset

