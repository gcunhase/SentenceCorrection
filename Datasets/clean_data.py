#Python script to clean data from Udon's Q&A project
# Author: Gwena Cunha
# Date: Jan 23rd 2017

import os
import glob #for listing files in dir

#data_path = "en"
data_path = "kr"
data_path_clean = data_path + "_clean"

if not os.path.isdir(data_path_clean):
	os.makedirs(data_path_clean)

original_files = glob.glob(data_path+"/*.txt")
#print(len(original_files))

for i in range(0, len(original_files)):
	file = original_files[i]
	original_file = open(file,"r")
	
	new_file_path = file.split("/", 1)
	new_file_path = data_path_clean+"/"+new_file_path[1]
	new_file = open(new_file_path,"w")
	print(new_file_path)				
				
	original_file_info = original_file.read().split("\n")
	for j in range(0, len(original_file_info)):
		#if not any(i in "?" for i in (original_file_info[j])):			
		if not ("?" in original_file_info[j]):
			file_content = original_file_info[j].split(" ", 1) #split only once
			if (len(file_content) == 2):
				file_content = file_content[1]+"\n"
				new_file.write(file_content)
				
	new_file.close()
	#print(original_file_info)
	original_file.close()

