from selenium import webdriver
from selenium.webdriver.common.by import By
from contextlib import closing
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pymongo
import json
connection = MongoClient()
db = connection['flipkart_reviews']



import unicodedata

def remove_non_ascii_1(text):

    return ''.join([i if ord(i) < 128 else ' ' for i in text])

def scrape(site):
	browser = webdriver.Chrome('/Library/Application Support/Google/chromedriver')
	# product = open('product.txt','r')
	# for line in product:
	# 	link = line.split(' : ')[1].rstrip()
	# 	prod_name = line.split(' : ')[0]

	# site = "https://www.flipkart.com/apple-iphone-x-space-gray-256-gb/product-reviews/itmexrgvf2yxeqjr?pid=MOBEXRGVCYGG2KXA"
	browser.get(site)
	collection = db['all_products']

	# file = open("review.txt", "w")
	product_name = None
	try:
		for count in range(1, 25):
			time.sleep(2)
			nav_btns = browser.find_elements_by_class_name('_33m_Yg')

			button = ""

			for btn in nav_btns:
				number = int(btn.text)
				if(number==count):
					button = btn
					break

			button.send_keys(Keys.RETURN)
			WebDriverWait(browser, timeout=10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_2xg6Ul")))

			try:
				read_more_btns = browser.find_elements_by_class_name('_1EPkIx')

				for rm in read_more_btns:
					browser.execute_script("return arguments[0].scrollIntoView();", rm)
					browser.execute_script("window.scrollBy(0, -150);")
					rm.click()
			except:
				pass
			page_source = browser.page_source

			soup = BeautifulSoup(page_source, "lxml")
			ans = soup.find_all("div", class_="_3DCdKt")
			product_title = soup.find_all("div", class_="_1SFrA2")
			if product_name is None:
				product_name = product_title[0].text
				print collection.find({'name':product_name}).count()
				if collection.find({'name':product_name}).count() > 0:
					browser.close()
					return product_name

			for tag in ans:
				# title = str(tag.find("p", class_="_2xg6Ul").string).replace(u"\u2018", "'").replace(u"\u2019", "'")
				title = tag.find("p", class_="_2xg6Ul").text
				title = remove_non_ascii_1(title)
				title.encode('ascii','ignore')
				# content = tag.find("div", class_="qwjRop").div.prettify().replace(u"\u2018", "'").replace(u"\u2019", "'")
				content = tag.find("div", class_="qwjRop").text
				# print content
				content = remove_non_ascii_1(content)
				content.encode('ascii','ignore')
				content = content.replace('READ MORE','')
				# content = content[15:-7]

				votes = tag.find_all("span", class_="_1_BQL8")
				upvotes = int(votes[0].string)
				downvotes = int(votes[1].string)

				# file.write("Review Title : %s\n\n" % title )
				# file.write("Upvotes : " + str(upvotes) + "\n\nDownvotes : " + str(downvotes) + "\n\n")
				# file.write("Review Content :\n%s\n\n\n\n" % content )
				collection.insert({'name':product_title[0].text ,'link':str(site), 'review title':str(title), 'upvotes':str(upvotes), 'downvotes': str(downvotes), 'content': str(content)})
	except:
		print('pass with error')
	browser.close()
	return product_name
	# file.close()

