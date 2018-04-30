# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from scrape import scrape
from check_senti import check_senti
from make_transaction import make_transaction
from apriorCBA import apriorCBA
from pymongo import MongoClient
from getOpinionWords import getOpinionWords

# Create your views here.
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
		print product_name
		make_csv(product_name)
		check_senti()
		make_transaction()
		apriorCBA()
		getOpinionWords()
		f = open('opinion_words.txt')
		arr = f.readlines()
		f.close()
		context = {
			'heading':'Here are the opinion words for %s'%(product_name) ,
			'opinion_words':arr[0]
		}
	return render(request,'index.html',context)