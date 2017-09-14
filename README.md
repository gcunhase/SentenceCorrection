# Sentence Correction
The goal of this project is to correct wrong english sentences

NMT: numbers and proper nouns don't need to be considered. If you can translate *John loves Mary*, you can translate *Mary loves John*. If you can translate *Mary is 25 years old*, you can translate *Mary is 35 years old*.

## Dataset
Third Solution, check folder Datasets

## Approach
ICONIP 2017 paper comparing GRU and MTGRU's performance when applied to the Sentence Correction issue

## New idea
Refer to the [GRU+Attention model](https://github.com/gcunhase/PaperNotes/blob/master/notes/gruatt.md):
   1. Compare GRU vs GRUAtt performance
   2. Add MT to GRUAtt if GRUAtt performs better than Vanilla GRU

