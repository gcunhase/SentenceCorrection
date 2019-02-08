# Sentence Correction
The goal of this project is to correct wrong english sentences

* ICONIP 2017: compare GRU and MTGRU's performance (Not Submitted)
* WCCI/IJCNN 2018: compare GRU, LSTM, RNN and MTGRU (Submitted and **Accepted**)
* Check wiki page for more information

## 0. Dataset
* Third Dataset Solution: WMT'15 with POS-Tagging
* [TODO]: how to create incomplete dataset

## 1. Running code
* RNN

* GRU

* LSTM

* MTLSTM

## 2. Results

## 3. Future Work
* Refer to the [GRU+Attention model](https://github.com/gcunhase/PaperNotes/blob/master/notes/gruatt.md):
   1. Compare GRU vs [GRUAtt](https://github.com/DeepLearnXMU/CAEncoder-NMT) performance
   2. Add MT to GRUAtt if GRUAtt performs better than Vanilla GRU

* If we can find a way to apply [CoGAN](https://github.com/gcunhase/PaperNotes/edit/master/notes/cogan.md) to language models, we can tackle translation problems. Sentence correction could be seen as a monolingual translation where the 2 different domains are the correct and wrong english.
