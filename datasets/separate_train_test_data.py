#
#Python script to separate train and test data (80 and 20% respectively)
# Optional shuffle function
# Author: Gwena Cunha
# Date: Jan 24th 2017
# Modified on Sep. 1st 2017 as a module
#

import os
import random
import argparse


def separate(data_dir, input_filename, output_filename, shuffle_var, train_percentage):
    ''' Function to separate train and test data into translate format

        Input:         
            shuffle_var: boolean that determines whether sentences will be shuffled or not.
            data_dir = "./signalmedia-1m-jsonl/"
            input_filename = "input.txt"
            output_filename = "output.txt"
            
        Output (saved files):
            input_train = "giga-fren.release2.fixed.en"
            output_train = "giga-fren.release2.fixed.fr"
            input_test = "newstest2013.en"
            output_test = "newstest2013.fr"            
            training-giga-fren.tar: compressed file with giga files
    '''
    
    input_path = data_dir+input_filename
    output_path = data_dir+output_filename
    
    input_train_p = "giga-fren.release2.fixed.en"
    input_train_path = data_dir+input_train_p
    output_train_p = "giga-fren.release2.fixed.fr"
    output_train_path = data_dir+output_train_p
    
    input_test_path = data_dir+"newstest2013.en"
    output_test_path = data_dir+"newstest2013.fr"
    
    # train_percentage = 0.95  # 95%
    # test_percentage = 1-train_percentage
    
    # Open files
    print("Opening files...")
    input_file = open(input_path, "r")
    input_train_file = open(input_train_path, "w")
    input_test_file = open(input_test_path, "w")
    
    output_file = open(output_path, "r")
    output_train_file = open(output_train_path, "w")
    output_test_file = open(output_test_path, "w")
    
    input_file_info = input_file.read().split("\n")
    output_file_info = output_file.read().split("\n")
    n_total = len(input_file_info)
    n_train = int(round(n_total*train_percentage))
    # n_test = n_total-n_train

    # Shuffle
    print("Shuffling sentences...")
    if shuffle_var:
        c = list(zip(input_file_info, output_file_info))
        random.shuffle(c)
        input_file_info, output_file_info = zip(*c)

    # Divide train and test
    for j in range(0, n_train):
        input_train_file.write(input_file_info[j]+"\n")
        output_train_file.write(output_file_info[j]+"\n")
    
    for j in range(n_train, n_total):
        input_test_file.write(input_file_info[j]+"\n")
        output_test_file.write(output_file_info[j]+"\n")
    
    os.system('gzip '+input_train_path)
    os.system('gzip '+output_train_path)
    
    os.system('cd '+data_dir+'; tar -cf training-giga-fren.tar '+input_train_p+'.gz '+output_train_p+'.gz')
    
    # Close open files
    print("Closing files...")	
    input_file.close()
    input_train_file.close()
    input_test_file.close()
    
    output_file.close()
    output_train_file.close()
    output_test_file.close()


def init_parse():
    parser = argparse.ArgumentParser(description='Extract original PTB train, val, test datasets.')
    parser.add_argument('--data_dir', default='IncompleteData/train-incompleteDataPOS-15_20words',
                        help='Directory for incomplete data')
    parser.add_argument('--input_filename', default='input1.en', help='Input filename (incomplete data)')
    parser.add_argument('--output_filename', default='output1.fr', help='Output filename (complete data)')
    parser.add_argument('--shuffle_var', action='store_true', help='Shuffle or not')
    parser.add_argument('--train_perc', default=95, help='Percentage saved for train in %')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = init_parse()
    args.data_dir = args.data_dir + "/"
    print(args.shuffle_var)
    separate(args.data_dir, args.input_filename, args.output_filename, args.shuffle_var, args.train_perc/100)
