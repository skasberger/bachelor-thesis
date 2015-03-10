#!/bin/env python2
# -*- coding: utf-8 -*-

"""
This scripts selects needed wikipedia articles (non-protected, no lists, only maintained template) and start to download them.
"""

from wikitools import wiki, api
import pprint
import wikipedia
import json
import csv
import re
import wikiimport
from datetime import datetime

__author__ = "Stefan Kasberger, Felix Stadthaus and Eren Misirli"
__copyright__ = "Copyright 2015"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Stefan Kasberger"
__email__ = "mail@stefankasberger.at"
__status__ = "Development"

REL_TO_ROOT = '../'
FILE_WIKIPAGES = REL_TO_ROOT+'/data/csv/wikipages.csv'
FILE_JSON_MAINTAINED = REL_TO_ROOT+'/data/json/second-try/request-maintained.json'
FILE_JSON_WIKIPAGES = REL_TO_ROOT+'/data/json/second-try/wikipages.json'
BASE_URL = 'http://en.wikipedia.org/w/api.php'
NUMBER_ARTICLES__EVALUATE = 400
NUMBER_ARTICLES__DOWNLOAD = 20

# save data to file
def save_to_file(data, filename):
	"""DESCRIPTION
	
	Args:
		param1: The first parameter.
		param2: The second parameter.
	
	Returns:
		True if successful, False otherwise.
	"""
	"""
	save data to file
	"""
	try:
		text_file = open(filename, "w")
		text_file.write(data)
		text_file.close()
	except:
		print 'Error writing', filename
		return False

# open json from file
def open_json(filename):
	"""DESCRIPTION
	
	Args:
		param1: The first parameter.
		param2: The second parameter.
	
	Returns:
		True if successful, False otherwise.
	"""
	"""
	open json from file
	"""
	try:
		f = open(filename, 'r')
		results = json.loads(f.read())
		f.close()
	except:
		print 'Error opening', filename
		return None
	return results

def get_maintained_articles():
	"""DESCRIPTION
	
	Args:
		param1: The first parameter.
		param2: The second parameter.
	
	Returns:
		True if successful, False otherwise.
	"""
	"""
	get article titles with maintained template via wikipedia api
	help: https://www.mediawiki.org/wiki/API:Embeddedin
	example url: https://en.wikipedia.org/w/api.php?action=query&list=embeddedin&eititle=Template:Maintained&eilimit=20
	"""
	pages = []
	params = {
				'action': 'query', 
				'list':'embeddedin',
				'eititle': 'Template:Maintained',
				'format': 'json'
			}
	try:
		# make API call
		start = datetime.now()
		site = wiki.Wiki(BASE_URL)
		request = api.APIRequest(site, params)
		results = request.query()
		
		# validate query response
		template_query = results['query']['embeddedin']
	except:
		print 'API query for template pages did not work!'
		return None, None
	
	# strip off 'Talk:' from title
	pages = [ {'title': article['title'][5:], 'title-talk-page': article['title'], 'access-mediawiki-api-template-tag': start} for article in template_query if article['title'][:5] == 'Talk:']
	return results, pages

def filter_pages(pages):
	"""DESCRIPTION
	
	Args:
		param1: The first parameter.
		param2: The second parameter.
	
	Returns:
		True if successful, False otherwise.
	"""
	"""
	exclude pages which are protected, semi-protected or lists
	help: https://en.wikipedia.org/w/api.php?action=help&modules=query+info
	example: http://en.wikipedia.org/w/api.php?action=query&titles=Operation_Ivy&prop=info&inprop=protection|url
	"""
	count_protected = 0
	tmp_pages = []
	page_urls = []

	# check all pages
	for page in pages:
		# make API call via wikitools
		try:
			params = {
						'action': 'query', 
						'prop':'info',
						'titles': page['title'],
						'inprop': 'protection|url',
						'format': 'json'
					}
			start = datetime.now()
			site = wiki.Wiki(BASE_URL)
			request = api.APIRequest(site, params)
			results = request.query()
			page['access-mw-api-page-details'] = start
		except:
			print 'Error connecting API!'
			page['access-mw-api-page-details'] = 'Error'

		for ids in results['query']['pages'].keys():
			is_list = False
			# make API call for page via wikipedia module
			try:
				start = datetime.now()
				wikipage = wikipedia.page(page)
				page['access-mw-api-page-details'] = start
			except:
				print 'Could not access API for category query of', page , '!'
				break

			# check if protected
			if not results['query']['pages'][ids]['protection']:
				# check if list
				for cat in wikipage.categories:
					match_obj = re.match( r'^list.*$', cat, re.I) # regex for 'List' and 'list' at the beginning of line
					if match_obj:
						is_list = True
						break
				if is_list:
					print page, 'is a list!'
					page['is-list'] = True
				else:
					# get computeable title and url of page
					page['url'] = results['query']['pages'][ids]['fullurl'].split('/')
					page['canonical-title'] = results['query']['pages'][ids]['fullurl'].split('/')[-1]
					page['is-list'] = False
				page['is-protected'] = False
			else:
				print page, 'is protected!'
				page['is-protected'] = True
				count_protected += 1
		tmp_pages.append(page)
	print 'Protected:', count_protected, 'of', len(pages), 'pages.'
	return tmp_pages

def get_final_wikipages(pages):
	"""DESCRIPTION
	
	Args:
		param1: The first parameter.
		param2: The second parameter.
	
	Returns:
		True if successful, False otherwise.
	"""
	tmp_pages = [page for page in pages if page['is-list'] == False and page['is-protected'] == False ]
	return tmp_pages

def get_filename(wikipages):
	"""DESCRIPTION
	
	Args:
		param1: The first parameter.
		param2: The second parameter.
	
	Returns:
		True if successful, False otherwise.
	"""
	tmp_pages = []
	for page['title'] in wikipages:
	    # replace '/' and ':' character with '_', because '/' is not allowed in a filename
	    if page.find('/') not -1:
	        page = page.replace('/', '_')
	    elif page.find(':') not -1:
	        filename = page.replace(':', '_'):
	    else:
	        filename = article
	    page['filename'] = filename
		tmp_pages.append(page)
    return tmp_pages

def download_wikipages(pages, folder, start=0, end=NUMBER_ARTICLES__DOWNLOAD):
	"""DESCRIPTION
	
	Args:
		param1: The first parameter.
		param2: The second parameter.
	
	Returns:
		True if successful, False otherwise.
	"""
	# download xml of all pages
	for page in pages[start:end]:
		wikiimport.startScript(page['filename'], folder)

if __name__ == '__main__':
	wikipages = []
	# results_api, wikipages = get_maintained_articles()
	# save_to_file(json.dumps(results_api, indent=2), )
	# wikipages = open_json(FILE_JSON_MAINTAINED)
	# wikipages = filter_pages(wikipages)
	# wikipages = get_final_wikipages(wikipages)
	# wikipages = get_filename(wikipages)
	# save_to_file(json.dumps(wikipages, indent=2), FILE_JSON_WIKIPAGES)
	wikipages = open_json(FILE_JSON_WIKIPAGES)
	download_wikipages(wikipages, REL_TO_ROOT+'/tmp')
	# wikipages = [ {'title': page} for page in pages]

	# save state of wikipages from first api access to final selection of pages => json
		# timestamp download end, title, number revisions, page-ID, url_title, talk, filename xml, filename talkpage xml, url_title talk page, page id talk page, template, reason filtering (protected, list, too big, too small, error),
	# save final state of wikipages: csv, json
	# save article metadata in wikipages.csv
	# timestamp download, title, number revisions, page-ID



