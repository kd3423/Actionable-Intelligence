
# coding: utf-8

# In[1]:
import csv
import pickle, json


# In[2]:

# names = ['vedant', 'dabas', 'abhinav']
# name = names[int(input('Choose name: \n%s'%(str(list(enumerate(names))))))]
with open('all_reviews.json', 'rb') as fp:
    arr = pickle.load(fp)


final = [['id','summary','text','category']]
count = 0
for elem in arr:
    id_ = count
    summary = elem['summary']
    text = elem['reviewText']
    category = elem['actionable']
    final.append([id_,summary,text,category])
    count +=1

myFile = open('all_reviews.csv', 'w')
with myFile:
    writer = csv.writer(myFile,delimiter = '\t')
    writer.writerows(final)

print("Writing complete")