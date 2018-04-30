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

opinion_words = {}
for id_ in pos_tag:
	pos_tags = pos_tag[id_]['pos_tags']
	for j in range(len(pos_tags)):
		if pos_tags[j][0] in features_list and j+1 < len(pos_tags):
			if pos_tags[j+1][1] == 'JJ':
				if pos_tags[j+1][0] not in opinion_words and pos_tags[j+1][0] not in stop_eng and pos_tags[j+1][0].isalnum():
					if pos_tags[j][0] in opinion_words:
						opinion_words[pos_tags[j][0]][0].append(pos_tags[j+1][0])
						opinion_words[pos_tags[j][0]][1].append(id_)
					else:
						opinion_words[pos_tags[j][0]] = [[pos_tags[j+1][0]],[id_]]
		if pos_tags[j][0] in features_list and j+2 < len(pos_tags):
			if pos_tags[j+2][1] == 'JJ':
				if pos_tags[j+2][0] not in opinion_words and pos_tags[j+2][0] not in stop_eng and pos_tags[j+2][0].isalnum():
					if pos_tags[j][0] in opinion_words:
						opinion_words[pos_tags[j][0]][0].append(pos_tags[j+2][0])
						opinion_words[pos_tags[j][0]][1].append(id_)
					else:
						opinion_words[pos_tags[j][0]] = [[pos_tags[j+2][0]],[id_]]

		if pos_tags[j][0] in features_list and j-1 > 0:
			if pos_tags[j-1][1] == 'JJ':
				if pos_tags[j-1][0] not in opinion_words and pos_tags[j-1][0] not in stop_eng and pos_tags[j-1][0].isalnum():
					if pos_tags[j][0] in opinion_words:
						opinion_words[pos_tags[j][0]][0].append(pos_tags[j-1][0])
						opinion_words[pos_tags[j][0]][1].append(id_)
					else:
						opinion_words[pos_tags[j][0]] = [[pos_tags[j-1][0]],[id_]]
		
		if pos_tags[j][0] in features_list and j-2 > 0:
			if pos_tags[j-2][1] == 'JJ':
				if pos_tags[j-2][0] not in opinion_words and pos_tags[j-2][0] not in stop_eng and pos_tags[j-2][0].isalnum():
					if pos_tags[j][0] in opinion_words:
						opinion_words[pos_tags[j][0]][0].append(pos_tags[j-2][0])
						opinion_words[pos_tags[j][0]][1].append(id_)
					else:
						opinion_words[pos_tags[j][0]] = [[pos_tags[j-2][0]],[id_]]
# print opinion_words

f= open('opinion_words.txt','w')
f.write(str(opinion_words))
f.close()