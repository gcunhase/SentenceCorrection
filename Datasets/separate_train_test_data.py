#Python script to separate train and test data (80 and 20% respectively)
# Optional shuffle function
# Author: Gwena Cunha
# Date: Jan 24th 2017

import os
import glob #for listing files in dir
import random

shuffle_var = True

data_dir = "./" #data_dir = "./dataset/"
input_path = data_dir+"input1.en"
output_path = data_dir+"output1.fr"

input_train_p = "giga-fren.release2.fixed.en"
input_train_path = data_dir+input_train_p
output_train_p = "giga-fren.release2.fixed.fr"
output_train_path = data_dir+output_train_p

input_test_path = data_dir+"newstest2013.en"
output_test_path = data_dir+"newstest2013.fr"

train_percentage = 0.8 # 80%
test_percentage = 1-train_percentage

#Open files
print("Opening files...")
input_file = open(input_path,"r")
input_train_file = open(input_train_path,"w")
input_test_file = open(input_test_path,"w")

output_file = open(output_path,"r")
output_train_file = open(output_train_path,"w")
output_test_file = open(output_test_path,"w")

input_file_info = input_file.read().split("\n")
output_file_info = output_file.read().split("\n")
n_total = len(input_file_info)
n_train = int(round(n_total*train_percentage))
#n_test = n_total-n_train

#Shuffle
print("Shuffling sentences...")
if (shuffle_var==True):
	c = list(zip(input_file_info, output_file_info))
	random.shuffle(c)
	input_file_info, output_file_info = zip(*c)
#	r = random.random() #seed
#	random.shuffle(input_file_info, lambda : r)
#	random.shuffle(output_file_info, lambda : r)

#Divide train and test
for j in range(0, n_train):
	input_train_file.write(input_file_info[j]+"\n")
	output_train_file.write(output_file_info[j]+"\n")

for j in range(n_train, n_total):
	input_test_file.write(input_file_info[j]+"\n")
	output_test_file.write(output_file_info[j]+"\n")

os.system('gzip '+input_train_path)
os.system('gzip '+output_train_path)

os.system('cd '+data_dir+'; tar -cf training-giga-fren.tar '+input_train_p+'.gz '+output_train_p+'.gz')

#Close open files
print("Closing files...")	
input_file.close()
input_train_file.close()
input_test_file.close()

output_file.close()
output_train_file.close()
output_test_file.close()
