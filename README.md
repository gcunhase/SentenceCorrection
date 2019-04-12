## About
Tensorflow code referent to [*"Temporal Hierarchies in Sequence to Sequence for Sentence Correction"*](https://ieeexplore.ieee.org/abstract/document/8489499) (IEEE WCCI 2018)

Comparison of GRU, LSTM, RNN and MTGRU in the English sentence correction task. 

Check wiki page for more information

### Contents

[Dataset](#1.-dataset) • [Training](#2.-training) • [Testing](#3.-testing) • [Results](#results)

### Dependencies
* Python 2.7, NLTK, progressbar2
* CUDA 8.0
* CuDNN v5.0
* Tensorflow 1.0.1

```bash
sudo apt-get install cuda-8-0
cd /tmp/tensorflow-pkg/; wget hhtp://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.0.1-cp27-none-linux_x86_64.whl
pip install --ignore-installed --upgrade tensorflow_gpu-1.0.1-cp27-none-linux_x86_64.whl
pip install -r requirements.txt
```

## How to Use
### 1. Dataset
* WMT'15 with POS-Tagging (Third Dataset Solution)
* Download, pre-processing, and more: [Dataset README](./datasets/README)

### 2. Training
* Follow [setup in Wiki](https://github.com/gcunhase/SentenceCorrection-WCCI2018/wiki/MTGRU) for MTGRUCell and MultiMTRNNCell
* In *`./translate/`* folder, run following script for GRU model:
    ```
    python translate_earlyStopping.py --train_dir=trainGRU --checkpoint_filename=checkpoint_perplexities_gru.txt --checkpoint_filename_best=checkpoint_perplexities_gru_best.txt
    ```
    
* Note: Pre-trained 3-layer models are currently too big to be uploaded   

* Arguments

    | Argument                     | Type    | Description                            |
    | ---------------------------- | ------- | -------------------------------------- |
    | `--use_rnn`                  | Boolean | Use RNN                                |
    | `--use_lstm`                 | Boolean | Use LSTM                               |
    | `--use_mtgru`                | Boolean | Use MTGRU                              |
    | `--use_mtlstm`               | Boolean | Use MTLSTM                             |
    | `--train_dir`                | String  | Directory to save model checkpoint     |
    | `--checkpoint_filename`      | String  | Filename to save model checkpoint      |
    | `--checkpoint_filename_best` | String  | Filename to save best model checkpoint |
    > Check *translate_earlyStopping.py* for more arguments
    
    > Example MTGRU: `python translate_earlyStopping.py --use_mtgru=True --train_dir=trainMTGRU --checkpoint_filename=checkpoint_perplexities_mtgru.txt --checkpoint_filename_best=checkpoint_perplexities_mtgru_best.txt` 

### 3. Testing
In *`./translate/`* folder:
```
python translate_earlyStopping.py --auto_decode
```
> Use all the same parameters used during training of the model

### 4. Evaluation
* Clone [nlp-metrics](https://github.com/harpribot/nlp-metrics) to *'./evaluation/'* for use in `tester_allSentencesOneFile.py`
    > Change import path if necessary

* Run: `./evaluation/scores.sh`
    > Change paths to your generated and target text files if needed

* Plotting train and test perplexity curves (Matlab): `./evaluation/graphs.m`

## Results
Results for 3-layer models

<p align="left">
<img src="https://github.com/gcunhase/SentenceCorrection-WCCI2018/blob/master/images/3layer_models_bleu.png" width="450" alt="BLEU scores">
</p>

Generated sentences
<p align="left">
<img src="https://github.com/gcunhase/SentenceCorrection-WCCI2018/blob/master/images/3layer_models_sentences.png" width="600" alt="Generated Sentences">
</p>

## Acknowledgement
If you use this code please cite it as:
```
@inproceedings{sergio2018temporal,
  title={Temporal Hierarchies in Sequence to Sequence for Sentence Correction},
  author={Sergio, Gwenaelle Cunha and Moirangthem, Dennis Singh and Lee, Minho},
  booktitle={2018 International Joint Conference on Neural Networks (IJCNN)},
  pages={1--7},
  year={2018},
  organization={IEEE}
}
```

Multiple Timescale code based on [Singh's work](https://github.com/dennissm/mtgru).
