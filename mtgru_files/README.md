MTGRU Files

Multi Time GRU is a modification of GRU with Multiple Timescales \tau, where the smaller this coefficient, the slower the model is, meaning that it can remember more things from the past (longer memory).

Files modified:
Add MTGRUCell and MultiMTRNNCell codes in whatever directory tensorflow is being used. In my case, it is in /usr/local/lib/python2.7/dist-packages/tensorflow/contrib/rnn/python/ops/core_rnn_cell_impl.py
Add MTGRU option in [my folder]/seq2seq_model.py

Code: credits to Dennis Moirangthem from ABRLab, KNU, Daegu, South Korea
