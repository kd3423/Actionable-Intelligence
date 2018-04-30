from textblob import TextBlob
import pandas as pd
import re
news = pd.read_csv("all_reviews_old.csv",delimiter = '\t')

def normalize_text(s):
    s = str(s).lower()
    s = re.sub('\s\W',' ',s)
    s = re.sub('\W\s',' ',s)
    s = re.sub('\s+',' ',s)

    return s
news['text'] = [normalize_text(s) for s in news['text']]

final_results = dict()
sentiments = []
tags = []
id_ = []
cat_ = []
for n in news['text']:
    text = TextBlob(n)
    #print text.tags
    #print text.sentiment
    tags.append(text.tags) 
    sentiments.append({'polarity':text.sentiment.polarity,'subjectivity':text.sentiment.subjectivity})

for n in news['id']:
    id_.append(n)
for n in news['category']:
    cat_.append(n)

for i in range(len(news['id'])):
    final_results[id_[i]] = {'category': cat_[i], 'sentiments':sentiments[i], 'pos_tags': tags[i]}


f1 = open('pos_tag.txt','w')
f1.write(str(final_results))
f1.close()

f1 = open('pos_tag.txt','r')
yy = eval(f1.read())
print yy[0]
    #break

