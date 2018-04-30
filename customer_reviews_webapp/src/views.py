# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from scrape import scrape

# Create your views here.
def home(request):
	if request.method == 'GET':
		context = {
			'heading':'Enter the link of a product whose reviews you want to analyze'
		}
	if request.method == 'POST':
		scrape(request.POST.get('url_text'))
	return render(request,'index.html',context)