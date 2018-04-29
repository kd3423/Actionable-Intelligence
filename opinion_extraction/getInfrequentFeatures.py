import os
import numpy as np
from nltk.corpus import stopwords
from nltk import word_tokenize
from collections import Counter
stop_eng = stopwords.words("english")
f= open('pos_tag.txt','r')
pos_tag = eval(f.read())
f.close()

f= open('features_list.txt','r')
features_list = eval(f.read())[0]
f.close()

f= open('opinion_words.txt','r')
opinion_words = eval(f.read())[0]
f.close()


infrequent_list = []
for id_ in pos_tag:
	counter = 0
	pos_tags = pos_tag[id_]['pos_tags']
	flag = 1
	for j in range(len(pos_tags)):
		if pos_tags[j][0] in features_list:
			flag = 0
		if pos_tags[j][0] in opinion_words:
			counter+=1

	if flag == 1:
		if counter >=2:
			for j in range(len(pos_tags)):
				if pos_tags[j][1] == 'NN' or pos_tags[j][1] == 'NNS':
					infrequent_list.append(pos_tags[j][0])
print infrequent_list
f = open('infrequent_list.txt','w')
f.write(str(infrequent_list))
f.close()
