#!/bin/env python2
# -*- coding: utf-8 -*-
"""
Downloads a Wikipedia article as XML via the MediaWiki API.
"""
import httplib, urllib
import xml.etree.ElementTree as ET
import sys
from sys import argv,exit
import os
import getopt

__author__ = "Maribel Acosta, Fabian Floeck, Felix Stadthaus, Eren Misirli, and Stefan Kasberger"
__copyright__ = "Copyright 2015"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Stefan Kasberger"
__email__ = "mail@stefankasberger.at"
__status__ = "Development"

# fetches wikipedia xml export
def getXMLFromApi(pageTitle, offset=False):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    if offset:
        params = urllib.urlencode({'title': 'Special:Export', 'action': 'submit', 'offset': offset, 'pages': pageTitle})
    else:
        params = urllib.urlencode({'title': 'Special:Export', 'action': 'submit', 'pages': pageTitle})

    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/xml"}
    conn = httplib.HTTPConnection("en.wikipedia.org")
    conn.request("POST", "/w/index.php", params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

    return data

# returns number of revisions and timestamp of last download
def getLastTimestampFromRoot(root):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    page = root.find('{http://www.mediawiki.org/xml/export-0.10/}page')

    if page == None:
        return False

    count = 0
    
    for revision in page.findall('{http://www.mediawiki.org/xml/export-0.10/}revision'):
        count += 1
        ts = revision.find('{http://www.mediawiki.org/xml/export-0.10/}timestamp').text

    return {'count': count, 'ts': ts}

# downloads and saves wikipedia article as xml
def getAllRevisions(article, filename, page_type='page', max=3000):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    root = ET.fromstring(getXMLFromApi(article))
    d = getLastTimestampFromRoot(root)
    count = d['count']
    ts = d['ts']
    oldts = False
    pagemain = root.find('{http://www.mediawiki.org/xml/export-0.10/}page')

    if(count==0):
        return False

    print article.upper()
    print 'Start:', ts
    
    while count <= max and ts != oldts:
        oldts = ts
        temproot = ET.fromstring(getXMLFromApi(article, ts))
        d = getLastTimestampFromRoot(temproot)
        if not d:
            break
        ts = d['ts']
        print ts
        if ts == oldts:
            break
        count += d['count']
        page = temproot.find('{http://www.mediawiki.org/xml/export-0.10/}page')
        pagemain.extend(page.findall('{http://www.mediawiki.org/xml/export-0.10/}revision'))

    if count >= 500 and count <= max or page_type == 'talk':
        tree = ET.ElementTree(root)
        tree.write(filename)
        print 'End:', ts
        print 'Revisions:', count
        return count
    else:
        return False

# starts computation and export            
def startScript(article, folder_xml):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    counter = 0
    # returns number of revisions if article fits into requirements or False if not
    is_good = getAllRevisions(article, folder_xml+'/'+article+'.xml')
    if is_good:
        getAllRevisions('Talk:'+article, folder_xml+'/'+'talk_'+article+'.xml', 'talk')
        counter += 1
        return counter

# reads out shell arguments and writes help statements
def main(my_argv):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    title = ''
    output = None

    if len(my_argv) <= 2:
        try:
            opts, _ = getopt.getopt(my_argv,"t:",["title="])
        except getopt.GetoptError:
            print 'Usage: wikiimport.py -t <title> [-o <output-folder>]'
            exit(2)
    else:
        try:
            opts, _ = getopt.getopt(my_argv,"t:o:",["title=","output="])
        except getopt.GetoptError:
            print 'Usage: wikiimport.py -t <title> [-o <output>]'
            exit(2)
    
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print "wikiimport"
            print
            print 'Usage: wikiimport.py -t <title> [-o <output-folder>]'
            print "-t --title title of wikipage to download (with underbars)"
            print "-o --output file with absolute or relative path."
            print "-h --help This help."
            exit()
        elif opt in ("-t", "--title"):
            title = arg
        elif opt in ("-o", "--output"):
            output = arg
         
    return title, output


# runs on start and call via shell
if __name__ == '__main__':

    # folder_xml = '../../data/xml/se-paper'
    folder_xml = '../../data/xml/se-paper'
    article, folder_xml = main(argv[1:])

    counter = startScript(article, folder_xml)
    print 'Anzahl Downloads:', counter



