# -*- coding: utf-8 -*-
#Python script to translate cleaned data from Korean to English
# P.S.: first line in this script needed to show korean (https://pastelinux.wordpress.com/2010/12/31/showing-korean-in-python/)
# https://github.com/mouuff/mtranslate
# Author: Gwena Cunha
# Date: Jan 24th 2017

import os
import glob #for listing files in dir
from mtranslate import translate
import codecs #reading korean

data_path_korean = "../kr_clean"
data_path_translation = "../en_translated_by_python"

##Example translation code
#to_translate = ''
#print(translate(to_translate, 'en'))


if not os.path.isdir(data_path_translation):
	os.makedirs(data_path_translation)

korean_files = glob.glob(data_path_korean+"/*.txt")
print(korean_files)
print(len(korean_files))

for i in range(0, len(korean_files)):
	file = korean_files[i]
	#kr_file = codecs.open(file,'r',encoding='utf-8')
	kr_file = open(file,'r')
	
	new_file_path = file.split("/", 2)
	new_file_path = data_path_translation+"/"+new_file_path[2]
	new_file = open(new_file_path,"w")
	print(new_file_path)				
				
	kr_file_info = kr_file.read().split("\n")
	for j in range(0, len(kr_file_info)):
		file_content = translate(kr_file_info[j], 'en')+"\n"
		new_file.write(file_content)
				
	new_file.close()
	kr_file.close()

