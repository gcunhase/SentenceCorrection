## MTGRU Files

Multi Time GRU is a modification of GRU with Multiple Timescales \tau, where the smaller this coefficient, the slower the model is, meaning that it can remember more things from the past (longer memory).

Check related [paper](https://arxiv.org/abs/1607.00718): Minsoo Kim, Moirangthem Dennis Singh, Minho Lee. "Towards Abstraction from Extraction: Multiple Timescale Gated Recurrent Unit for Summarization". ArXiv, July 2016.

### Files modified:
* Add MTGRUCell and MultiMTRNNCell codes in whatever directory tensorflow is being used. In my case, it is in /usr/local/lib/python2.7/dist-packages/tensorflow/contrib/rnn/python/ops/core_rnn_cell_impl.py
* Add MTGRU option in [my folder]/seq2seq_model.py

### Credits
Code: credits to Dennis Moirangthem from ABRLab, KNU, Daegu, South Korea