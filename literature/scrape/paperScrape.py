# paperScrape.py v0.00           damiancclarke             yyyy-mm-dd:2015-05-29
#---|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8
#
# Scrapes econpapers for all titles, abstracts, etc from all JPE issues.  Based
# on the url http://econpapers.repec.org/article/ucpjpolec/, and screen dumps of
# each issue.
#

import os
import urllib
import urllib2
from urllib2 import urlopen, URLError, HTTPError
import re

#-------------------------------------------------------------------------------
#--- (1) out
#-------------------------------------------------------------------------------
nameFile = open('namesJPE.txt', 'w')
absFile =  open('abstractsJPE.txt', 'w')

#-------------------------------------------------------------------------------
#--- (2) dump
#-------------------------------------------------------------------------------
base = 'http://econpapers.repec.org/article/ucpjpolec/'
addresses = ['http://econpapers.repec.org/article/ucpjpolec/default.htm']
for page in range(1,74):
    addresses += [base+'default'+str(page)+'.htm']

for a in addresses:
    source = urllib2.urlopen(a).read()
    papers = re.findall('<dt><a href="(.*)</a>', source)
    for p in papers:
        p = p.split('.htm')
        padd = base+'/'+p[0]+'.htm'
        det = urllib2.urlopen(padd).read()
        name     = re.search('<meta name="citation_title" content="(.*)">',det)
        abstract = re.search('<meta name="citation_abstract" content="(.*)">',det)        
        year     = re.search('<meta name="citation_year" content="(.*)">',det)
        volume   = re.search('<meta name="citation_volume" content="(.*)">',det)

        try:
            abstract = abstract.group(1)
        except:
            abstract = ''
        name = name.group(1)
        volume = volume.group(1)
        year = year.group(1)
        
        nameFile.write(year + ' | ' + volume + ' | ' + name +'\n')
        absFile.write(year + ' | ' + volume + ' | ' + abstract +'\n')

nameFile.close()
absFile.close()

