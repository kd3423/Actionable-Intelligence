# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from scrape import scrape
from check_senti import check_senti
from make_transaction import make_transaction
from apriorCBA import apriorCBA
from pymongo import MongoClient
from getOpinionWords import getOpinionWords
from normalizeFeatures import normalizeFeatures
from django.template.defaulttags import register
from django.utils.safestring import mark_safe
from textblob import TextBlob
import json
import pandas as pd

# Create your views here.
@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def make_csv(product_name):
	connection = MongoClient()
	db = connection['flipkart_reviews']
	collection = db['all_products']
	curr = collection.find({'name':product_name})
	arr = ['id\tsummary\ttext\tcategory\n']
	count = 0
	for doc in curr:
		s = '%d\t%s\t%s\t0\n'%(count,doc['review title'],doc['content'])
		arr.append(s)
		count += 1
	f = open('all_reviews.csv','w')
	for x in arr:
		f.write(x)
	f.close()

def home(request):
	if request.method == 'GET':
		context = {
			'heading':'Enter the link of a product whose reviews you want to analyze'
		}
	if request.method == 'POST':
		product_name = scrape(request.POST.get('url_text'))
		make_csv(product_name)
		check_senti()
		make_transaction()
		apriorCBA()
		getOpinionWords()
		normalizeFeatures()
		dic = json.load(open('opinion_words.txt'))
		dic = {k:[list(set(v[0])),list(set(v[1]))] for k,v in dic.items()}
		df = pd.read_csv("all_reviews.csv",delimiter='\t')
		id_to_title = {}
		id_to_text = {}
		id_to_polarity = {}
		for idx,row in df.iterrows():
			id_to_title[row['id']] = row['summary']
			id_to_text[row['id']] = row['text']
			text = TextBlob(row['text'])
			if row['id'] not in id_to_polarity:
				id_to_polarity[row['id']] = text.sentiment.polarity
		json_dic = {}
		for k,v in dic.items():
			json_dic[k] = {'name': k, 'children':[]}
			for word in v[0]:
				json_dic[k]['children'].append({'name':word,'size':721})
		print json_dic
		# json_dic = {
		# 	{"name": "Feature Name","children": [{"name": "Opinion 1", "size": 721}, {"name": "Opinion 1", "size": 721}]}
		# }
		context = {
			'heading':'Enter the link of a product whose reviews you want to analyze',
			'results_heading':'Here are the features along with opinion words for %s'%(product_name) ,
			'opinion_words':dic.items(),
			'id_to_text':id_to_text,
			'id_to_title':id_to_title,
			'id_to_polarity':id_to_polarity,
			'total':len(df),
			'json_dic':json_dic
		}
	return render(request,'index.html',context)