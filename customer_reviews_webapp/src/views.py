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
import json
import pandas as pd

# Create your views here.
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
		df = pd.read_csv("all_reviews.csv")
		id_to_title = {}
		id_to_text = {}
		for idx,row in df.iterrows():
			id_to_title[row['id']] = row['summary']
			id_to_text[row['id']] = row['text']
		context = {
			'heading':'Here are the features of the product along with opinion words for %s'%(product_name) ,
			'opinion_words':dic,
			'id_to_text':id_to_text,
			'id_to_title':id_to_title
		}
	return render(request,'index.html',context)