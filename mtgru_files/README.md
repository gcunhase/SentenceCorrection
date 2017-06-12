## MTGRU

Multiple Timescale Gated Recurrent Unit (MTGRU) is a modification of the vanilla GRU that adds Multiple Timescales $\tau$ to it, where the smaller this coefficient, the slower the model is, meaning that it can remember more things from the past (longer memory).

Check related [paper](https://arxiv.org/abs/1607.00718): Minsoo Kim, Moirangthem Dennis Singh, Minho Lee. "Towards Abstraction from Extraction: Multiple Timescale Gated Recurrent Unit for Summarization". ArXiv, July 2016.

### Files modified:
* Add MTGRUCell and MultiMTRNNCell codes in whatever directory tensorflow is being used. In my case, it is in _/usr/local/lib/python2.7/dist-packages/tensorflow/contrib/rnn/python/ops/corernncellimpl.py_
* Add MTGRU usage option in _[my folder]/seq2seqmodel.py_

### Credits
Code credits to Dennis Moirangthem from ABRLab, KNU, Daegu, South Korea.