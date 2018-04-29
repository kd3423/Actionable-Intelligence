import os
import pandas as pd
import re
from fuzzywuzzy import fuzz
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from collections import Counter
lemmatizer = WordNetLemmatizer()
stop_eng = stopwords.words("english")

news = pd.read_csv("all_reviews.csv",delimiter = '\t')
def normalize_text(s):
    s = str(s).lower()
    s = re.sub('\s\W',' ',s)
    s = re.sub('\W\s',' ',s)
    s = re.sub('\s+',' ',s)

    return s
f = open('transaction.txt','w')
review_list = []
news['text'] = [normalize_text(s) for s in news['text']]
if 'fuzzy_dict.txt' not in os.listdir('./'):
	fuzzy_dict = dict()
	for n in news['text']:
		word_list = []
		tokens = word_tokenize(n)
		for k in tokens:
			flag = 0
			if k not in stop_eng and k.isalnum():
				if k not in fuzzy_dict and len(fuzzy_dict) > 0:
					for j in fuzzy_dict:
						if fuzz.ratio(j,k) > 85 and j != k:
							fuzzy_dict[j].append(k)
							flag = 0
							k_new = j
						else:
							flag = 1
					if flag == 1:
						fuzzy_dict[k] = list()
						k_new = k
				else:
					fuzzy_dict[k] = list()
					k_new = k
			word_list.append(k_new)
		review_list.append(word_list)
		str_ = ' '.join(word_list)
		f.write(str_+'\n')
	f1 = open('fuzzy_dict.txt','w')
	f1.write(str(fuzzy_dict))
	f1.close()
	print('Done')

	f1 = open('review_list.txt','w')
	f1.write(str(review_list))
	f1.close()
	print('Done')

f.close()



# else:
# 	fuzzy_dict = eval(open('fuzzy_dict.txt','r').read())
# 	for n in news['text']:
# 		tokens = word_tokenize(n)
# 		for k in tokens:
# 			if k not in stop_eng and k.isalnum():
# 				for j in fuzzy_dict:
# 					if 