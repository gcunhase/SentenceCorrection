#Python script to add dot at the end of each sentence if it already doesn't have it
# Author: Gwena Cunha
# Date: Jan 24th 2017

import os
import glob #for listing files in dir
import fileinput, sys

    
#data_path = "en_translated_from_kr_clean_gwena/"
data_path = "./"

#files_path = glob.glob(data_path+"*.txt")
files_path = glob.glob(data_path+"output1.fr")

for i in range(0, len(files_path)):
	file_path = files_path[i]
	file = open(file_path,"r")
	#file_out_path = data_path+file_path.split('/')[1].split('.txt')[0]+'_add_dot.txt'
	file_out_path = data_path+file_path.split('/')[1].split('.fr')[0]+'_add_dot.fr'
	file_out = open(file_out_path,"w+")
	print(file_out_path)

	original_file_info = file.read().split("\n")
	#file.seek(0) #rewind to beginning of file
	print(original_file_info)
	for j in range(0, len(original_file_info)):
		file_content = original_file_info[j]
		if (len(original_file_info[j]) != 0): #to not consider empty lines
			if not ("." in file_content):
				file_content = file_content+"."
				#print(len(original_file_info[j]))
			file_content = file_content+"\n"
			file_out.write(file_content)
				
	file.close()
	file_out.close()

