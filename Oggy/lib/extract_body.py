import json
import re
from lxml import html
from manage_extracts import *
import logging

def extract_body(body,test_case_response_extract_body):
	extraction_details = ''
	for test_extract in test_case_response_extract_body:
		i = 0
		#print "--------------"+test_extract['@type'] + " + " + test_extract['@method']+ " + " + test_extract['@exp']+ " --> " + test_extract['#text']
		if test_extract['@type'] == 'json' and test_extract['@method'] == 'path':
			body_json = json.loads(body)
			temp_json = body_json
			path = str(test_extract['@exp']).split(':')
			#print path
			while i < len(path):
			    if(type(temp_json[path[i]]) is list):
			        temp = int(path[i+1])
			        temp_json = temp_json[path[i]][temp]
			       # print "f",temp_json
			        i = i+2
			    else:
			        temp_json = temp_json[path[i]]
			        #print temp_json
			        i = i+1
			store_body_extract(str(test_extract['#text']),temp_json)
			extraction_details = extraction_details + " Extracted Body "+ str(test_extract['#text']) +" with value "+temp_json+"\n"

		if test_extract['@type'] == 'text' and test_extract['@method'] == 'regex':
			regex_string = str(test_extract['@exp'])
			searchobj = re.findall(regex_string,body,re.M|re.I)
			#print searchobj
			store_body_extract(str(test_extract['#text']),str(searchobj[0]))
			extraction_details = extraction_details + " Extracted Body "+ str(test_extract['#text']) +" with value "+str(searchobj[0])+"\n"

			
		if test_extract['@type'] == 'html' and test_extract['@method'] == 'regex':
			regex_string = str(test_extract['@exp'])
			searchobj = re.findall(regex_string,body,re.M|re.I)
			#print searchobj
			store_body_extract(str(test_extract['#text']),str(searchobj[0]))
			extraction_details = extraction_details + " Extracted Body "+ str(test_extract['#text']) +" with value "+str(searchobj[0])+"\n"

		if test_extract['@type'] == 'xml' and test_extract['@method'] == 'regex':
			regex_string = str(test_extract['@exp'])
			searchobj = re.findall(regex_string,body,re.M|re.I)
			#print searchobj
			store_body_extract(str(test_extract['#text']),str(searchobj[0]))
			extraction_details = extraction_details + " Extracted Body "+ str(test_extract['#text']) +" with value "+str(searchobj[0])+"\n"

		if test_extract['@type'] == 'xml' and test_extract['@method'] == 'xpath':
			regex_string = str(test_extract['@exp'])
			tree = html.fromstring(body)
			searchobj = tree.xpath(regex_string)
			#print searchobj
			store_body_extract(str(test_extract['#text']),str(searchobj[0]))
			extraction_details = extraction_details + " Extracted Body "+ str(test_extract['#text']) +" with value "+str(searchobj[0])+"\n"

		if test_extract['@type'] == 'html' and test_extract['@method'] == 'xpath':
			regex_string = str(test_extract['@exp'])
			tree = html.fromstring(body)
			searchobj = tree.xpath(regex_string)[0].strip()
			#print searchobj
			store_body_extract(str(test_extract['#text']),str(searchobj[0]))
			extraction_details = extraction_details + " Extracted Body "+ str(test_extract['#text']) +" with value "+str(searchobj[0])+"\n"

	return extraction_details

def extract_header(regex, headers):
	extraction_details = ''
	print regex,headers,type(headers)
	result = 'fail'
	regex_string = regex;
	searchobj = re.findall(regex_string,json.dumps(headers),re.M|re.I)
	return str(searchobj[0])



