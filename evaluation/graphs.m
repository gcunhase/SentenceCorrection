%
% Train and test perplexities
%
% A.colheaders{1, k}
% https://kr.mathworks.com/help/matlab/ref/importdata.html
%
% Author: Gwena Cunha
% Date: Jan 23rd 2018
%

format long

%global_step learning_rate step_time train_perp bucket_perps
filename = 'WCCI_paper_results/translate-gru/logs-25000steps-15_20wordsData/checkpoint_perplexities_rnn_25000steps-3layers-train2.txt';
delimiterIn = ' ';
headerlinesIn = 1;
A = importdata(filename,delimiterIn,headerlinesIn);
rnn_global_step = A.data(:,1);
rnn_train_perp = A.data(:,4);
rnn_test_perp = sum(A.data(:,5:end), 2)/4;

filename = 'WCCI_paper_results/translate-gru/logs-25000steps-15_20wordsData/checkpoint_perplexities_lstm_25000steps.txt';
delimiterIn = ' ';
headerlinesIn = 1;
A = importdata(filename,delimiterIn,headerlinesIn);
lstm_global_step = A.data(:,1);
lstm_train_perp = A.data(:,4);
lstm_test_perp = sum(A.data(:,5:end), 2)/4;

filename = 'WCCI_paper_results/translate-gru/logs-25000steps-15_20wordsData/checkpoint_perplexities_gru_25000steps.txt';
delimiterIn = ' ';
headerlinesIn = 1;
A = importdata(filename,delimiterIn,headerlinesIn);
gru_global_step = A.data(:,1);
gru_train_perp = A.data(:,4);
gru_test_perp = sum(A.data(:,5:end), 2)/4;

filename = 'WCCI_paper_results/translate-gru/logs-25000steps-15_20wordsData/checkpoint_perplexities_mtgru-25000steps-1-0.999-0.998.txt';
delimiterIn = ' ';
headerlinesIn = 1;
A = importdata(filename,delimiterIn,headerlinesIn);
mtgru_global_step = A.data(:,1);
mtgru_train_perp = A.data(:,4);
mtgru_test_perp = sum(A.data(:,5:end), 2)/4;

plot_from = 1;
%plot(rnn_global_step(plot_from:end), rnn_train_perp(plot_from:end), 'g'); grid on; hold on;
%plot(rnn_global_step(plot_from:end), rnn_test_perp(plot_from:end), '--g'); grid on; hold on;
plot(lstm_global_step(plot_from:end), lstm_train_perp(plot_from:end), 'b', 'LineWidth',1.5); grid on; hold on;
plot(lstm_global_step(plot_from:end), lstm_test_perp(plot_from:end), '--b', 'LineWidth',1.5); grid on; hold on;
plot(gru_global_step(plot_from:end), gru_train_perp(plot_from:end), 'k', 'LineWidth',1.5); grid on; hold on;
plot(gru_global_step(plot_from:end), gru_test_perp(plot_from:end), '--k', 'LineWidth',1.5); grid on; hold on;
plot(mtgru_global_step(plot_from:end), mtgru_train_perp(plot_from:end), 'r', 'LineWidth',1.5); grid on; hold on;
plot(mtgru_global_step(plot_from:end), mtgru_test_perp(plot_from:end), '--r', 'LineWidth',1.5); grid on; hold on;
legend({'LSTM Train', 'LSTM Test', 'GRU Train', 'GRU Test', 'MTGRU Train', 'MTGRU Test'});
xlabel('Steps'); ylabel('Perplexity');

%% Difference between BLEU-scores
%Vanilla_RNN_small2 = [0.0603, 4.49e^-10, 8.93$e^{-13}$ & 4.04$e^{-14}$ \\
%LSTM & 0.454 & 0.312 & 0.230 & 0.179 \\
GRU_small2 = [0.504, 0.360, 0.273, 0.217];
MTGRU_small2 = [0.525, 0.386, 0.301, 0.242];
(sum(GRU_small2 - MTGRU_small2))/4

%Vanilla RNN & 0.0512 & 4.30$e-10$ & 8.91$e-13$ & 4.12$e-14$ \\
LSTM_small2_4layers = [0.489, 0.348, 0.270, 0.215];
%GRU_small2_4layers = [0.479 & 0.332 & 0.250 & 0.201 \\ 
MTGRU_small2_4layers = [0.521, 0.385, 0.310, 0.261];
(sum(LSTM_small2_4layers - MTGRU_small2_4layers))/4



%Vanilla RNN & 0.0634 & 0.00259 & 7.22$e^{-09}$ & 1.22$e^{-11}$ \\
%LSTM & 0.430 & 0.302 & 0.223 & 0.169 \\
GRU_1000 = [0.469, 0.336, 0.251, 0.192];
MTGRU_1000 = [0.484, 0.350, 0.263, 0.202];
(sum(GRU_1000 - MTGRU_1000))/4


%Vanilla RNN & 0.0682 & 0.00281 & 7.84$e-09$ & 1.33$e-11$ \\
LSTM_1000_4layers = [0.449, 0.328, 0.249, 0.194];
%GRU_1000_4layers =  & 0.454 & 0.325 & 0.243 & 0.186 \\ 
MTGRU_1000_4layers = [0.489, 0.353, 0.266, 0.203];
(sum(LSTM_1000_4layers - MTGRU_1000_4layers))/4

