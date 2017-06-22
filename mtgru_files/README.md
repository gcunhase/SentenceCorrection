## MTGRU

Multiple Timescale Gated Recurrent Unit (MTGRU) is a modification of the vanilla GRU that adds Multiple Timescales $\tau$ to it, where the smaller this coefficient, the slower the model is, meaning that it can remember more things from the past (longer memory).

Check related [paper](https://arxiv.org/abs/1607.00718): Minsoo Kim, Moirangthem Dennis Singh, Minho Lee. "Towards Abstraction from Extraction: Multiple Timescale Gated Recurrent Unit for Summarization". ArXiv, July 2016.

### Files modified:
* Add MTGRUCell and MultiMTRNNCell codes in the Python script that has the GRUCell and MultiRNNCell and in whatever directory tensorflow is being used. In my case, it is in _/usr/local/lib/python2.7/dist-packages/tensorflow/contrib/rnn/python/ops/_ and the file name is _core_rnn_cell_impl.py_
* Add MTGRU usage option in _[my folder]/seq2seqmodel.py_
* _translate.py_: added _auto_decode()_ function to read a txt file with input sentences (_.en_) and writes the output sentences generated with the trained model in another file ([filename]_out_gru.txt or [filename]_out_mtgru.txt). This generated file is then compared with the file containing the expected sentences (_.fr_) to get the BLEU and ROUGE calculations (and in the future also METEOR). Furthermore, this file writes the checkpoint info to a text file for later plotting.
* _scores.sh_: automatically calculates the BLEU and ROUGE scores of 2 test datasets originated by the MTGRU model

### Credits
Code credits to Dennis Moirangthem from ABRLab, KNU, Daegu, South Korea.

Edited with prose.io
