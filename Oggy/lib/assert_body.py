import json
import re
from lxml import html
import logging

def assert_body(body,test_case_response_assert_body):
	logging.info("assert_body:Processing assert body operation")
	result = 'NA'
	reason = ''
	for test_assert in test_case_response_assert_body:
		i = 0
		#print "--------------"+test_assert['@type'] + " + " + test_assert['@method']+ " + " + test_assert['@exp']+ " --> " + test_assert['#text']
		if test_assert['@type'] == 'json' and test_assert['@method'] == 'path':
			body_json = json.loads(body)
			temp_json = body_json
			path = str(test_assert['@exp']).split(':')
			#print path
			while i < len(path):
			    if(type(temp_json[path[i]]) is list):
			        temp = int(path[i+1])
			        temp_json = temp_json[path[i]][temp]
			        #print "f",temp_json
			        i = i+2
			    else:
			        temp_json = temp_json[path[i]]
			        #print temp_json
			        i = i+1
			if(str(temp_json) == test_assert['#text']):
				logging.info("assert_body:Assert body operation success")
				result = 'pass'
			else:
				result = 'fail'
				logging.error("assert_body:Assert Body operation failed")
				reason = 'Asset Response Body Error: Expected contents => '+ test_assert['#text']+" Actual contents => "+str(temp_json)

		if test_assert['@type'] == 'text' and test_assert['@method'] == 'regex':
			regex_string = str(test_assert['@exp'])
			searchobj = re.findall(regex_string,body,re.M|re.I)
			for i in range(len(searchobj)):
				if test_assert['#text'] == searchobj[i]:
					result = 'pass'
					logging.info("assert_body:Assert body operation success")
					break
				else:
					result = 'fail'
					logging.error("assert_body:Assert Body operation failed")
					reason = 'Asset Response Body Error: Expected contents => '+ test_assert['#text']+" Actual contents => "+searchobj[i]

		if test_assert['@type'] == 'html' and test_assert['@method'] == 'regex':
			regex_string = str(test_assert['@exp'])
			searchobj = re.findall(regex_string,body,re.M|re.I)
			#print searchobj
			for i in range(len(searchobj)):
				if test_assert['#text'] == searchobj[i]:
					logging.info("assert_body:Assert body operation success")
					break
				else:
					result = 'fail'
					logging.error("assert_body:Assert Body operation failed")
					reason = 'Asset Response Body Error: Expected contents => '+ test_assert['#text']+" Actual contents => "+searchobj[i]

		if test_assert['@type'] == 'xml' and test_assert['@method'] == 'regex':
			regex_string = str(test_assert['@exp'])
			searchobj = re.findall(regex_string,body,re.M|re.I)
			#print searchobj
			for i in range(len(searchobj)):
				if test_assert['#text'] == searchobj[i]:
					result = 'pass'
					logging.info("assert_body:Assert body operation success")
					break
				else:
					result = 'fail'
					logging.error("assert_body:Assert Body operation failed")
					reason = 'Asset Response Body Error: Expected contents => '+ test_assert['#text']+" Actual contents => "+searchobj[i]

		if test_assert['@type'] == 'xml' and test_assert['@method'] == 'xpath':
			regex_string = str(test_assert['@exp'])
			tree = html.fromstring(body)
			searchobj = tree.xpath(regex_string)
			#print searchobj
			for i in range(len(searchobj)):
				if test_assert['#text'] == searchobj[i]:
					result = 'pass'
					logging.info("assert_body:Assert body operation success")
					break
				else:
					result = 'fail'
					logging.error("assert_body:Assert Body operation failed")
					reason = 'Asset Response Body Error: Expected contents => '+ test_assert['#text']+" Actual contents => "+searchobj[i]

		if test_assert['@type'] == 'html' and test_assert['@method'] == 'xpath':
			regex_string = str(test_assert['@exp'])
			tree = html.fromstring(body)
			searchobj = tree.xpath(regex_string)
			#print searchobj
			for i in range(len(searchobj)):
				if test_assert['#text'] == searchobj[i]:
					result = 'pass'
					logging.info("assert_body:Assert body operation success")
					break
				else:
					result = 'fail'
					logging.error("assert_body:Assert Body operation failed")
					reason = 'Asset Response Body Error: Expected contents => '+ test_assert['#text']+" Actual contents => "+searchobj[i]
	return (result,reason)
