# Sentence Correction
The goal of this project is to correct wrong english sentences

* ICONIP 2017: compare GRU and MTGRU's performance (Not Submitted)
* WCCI/IJCNN 2018 [[IEEE paper link](https://ieeexplore.ieee.org/abstract/document/8489499)]: compare GRU, LSTM, RNN and MTGRU (Submitted and **Accepted**)
* Check wiki page for more information

## 0. Requirements
Python 2.7, CUDA 8.0, CuDNN v5.0, Tensorflow 1.0.1
```bash
sudo apt-get install cuda-8-0
cd /tmp/tensorflow-pkg/; wget hhtp://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.0.1-cp27-none-linux_x86_64.whl
pip install --ignore-installed --upgrade tensorflow_gpu-1.0.1-cp27-none-linux_x86_64.whl
```

## 1. Dataset
* WMT'15 with POS-Tagging (Third Dataset Solution)
* [Option 1] Download incomplete data
    * Download [incomplete dataset](https://1drv.ms/f/s!Ai9Q4WIAUMvPhFhm_AHR9kMe21lpvv): `input1.en` and `output.fr`
    * Separate train and test: `cd ./datasets && python separate_train_test_data.py`
* [Option 2] Create your own incomplete dataset
    * Download [WMT dataset](http://www.statmt.org/wmt10/training-giga-fren.tar)
    * [TODO] Add script to make incomplete data

## 2. Training
* Follow setup in Wiki for MT model
* In *'./translate/'*, run each model:
    * RNN: `python translate_earlyStopping.py --use_rnn=True --train_dir=trainRNN --checkpoint_filename=checkpoint_perplexities_rnn.txt --checkpoint_filename_best=checkpoint_perplexities_rnn_best.txt`
    * GRU: `python translate_earlyStopping.py --train_dir=trainGRU --checkpoint_filename=checkpoint_perplexities_gru.txt --checkpoint_filename_best=checkpoint_perplexities_gru_best.txt`
    * LSTM: `python translate_earlyStopping.py --use_lstm=True --train_dir=trainLSTM --checkpoint_filename=checkpoint_perplexities_lstm.txt --checkpoint_filename_best=checkpoint_perplexities_lstm_best.txt`
    * MTGRU: `python translate_earlyStopping.py --use_mtgru=True --train_dir=trainMTGRU --checkpoint_filename=checkpoint_perplexities_mtgru.txt --checkpoint_filename_best=checkpoint_perplexities_mtgru_best.txt`
    * MTLSTM: `python translate_earlyStopping.py --use_mtlstm=True --train_dir=trainMTLSTM --checkpoint_filename=checkpoint_perplexities_mtlstm.txt --checkpoint_filename_best=checkpoint_perplexities_mtlstm_best.txt`

* Pre-trained 3-layer models are currently too big to be uploaded   

* Arguments

| Argument     | Type    | Property                           |
| ------------ | ------- | ---------------------------------- |
| `use_rnn`    | Boolean | Use RNN                            |
| `use_lstm`   | Boolean | Use LSTM                           |
| `use_mtgru`  | Boolean | Use MTGRU                          |
| `use_mtlstm` | Boolean | Use MTLSTM                         |
| `train_dir`  | String  | Directory to save model checkpoint |
> Check *translate_earlyStopping.py* for more arguments

## 3. Testing
* In *'./translate/'*:
    `python translate_earlyStopping.py --auto_decode`
> Use all the same parameters used during training of the model

## 4. Evaluation
* Clone [nlp-metrics](https://github.com/harpribot/nlp-metrics) to *'./evaluation/'* for use in `tester_allSentencesOneFile.py`
> Change import path if necessary

* Run: `./evaluation/scores.sh`
> Change paths to your generated and target text files if needed

## Results
* BLEU scores:
<p align="center">
<img src="https://github.com/gcunhase/SentenceCorrection-WCCI2018/blob/master/notes/imgs/3layer_models_bleu.png" width="500" alt="BLEU">
</p>

* Generated sentences: 
<p align="center">
<img src="https://github.com/gcunhase/SentenceCorrection-WCCI2018/blob/master/notes/imgs/3layer_models_sentences.png" width="500" alt="Generated Sentences">
</p>

## Future Work
* Refer to the [GRU+Attention model](https://github.com/gcunhase/PaperNotes/blob/master/notes/gruatt.md):
   1. Compare GRU vs [GRUAtt](https://github.com/DeepLearnXMU/CAEncoder-NMT) performance
   2. Add MT to GRUAtt if GRUAtt performs better than Vanilla GRU

* If we can find a way to apply [CoGAN](https://github.com/gcunhase/PaperNotes/edit/master/notes/cogan.md) to language models, we can tackle translation problems. Sentence correction could be seen as a monolingual translation where the 2 different domains are the correct and wrong english.
