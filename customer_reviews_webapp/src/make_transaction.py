import os
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from collections import Counter

def make_transaction():
	lemmatizer = WordNetLemmatizer()
	stop_eng = stopwords.words("english")
	f = open('pos_tag.txt','r')
	dict_  = eval(f.read())
	f2 = open('fuzzy_dict.txt','r')
	fuzzy = eval(f2.read())
	f3 = open('new_transaction.txt','w')
	final = []
	for id_ in dict_:
		lreview = []
		pos_tag_list = dict_[id_]['pos_tags']
		# print pos_tag_list
		for word in pos_tag_list:
			if (word[1] == 'NN' or word[1] == 'NNS') and word[0] not in stop_eng and word[0].isalnum():
				# print word
				word_new = word[0]
				lreview.append(word_new)
		print lreview
		fstr = ' '.join(lreview)
		f3.write(fstr+'\n')
	f.close()
	f2.close()
	f3.close()
