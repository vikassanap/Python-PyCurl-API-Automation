import re
import string
import logging
from manage_extracts import *

regex_string = "\$\{EXTRACT:(.+?)\}"

def extract_process_base_url(base_url):
	temp_body  = str(base_url)
	searchobj = re.findall(regex_string,temp_body,re.M|re.I)
	for dp in searchobj:
		temp = "${EXTRACT:"+dp+"}"
		if temp in temp_body:
			temp_body = temp_body.replace(temp, read_header(str(dp)))
	return temp_body

def extract_process_request_body(body,request_body_type):
	if(request_body_type == 'form'):
		temp_body  = body
		for request_parameter in temp_body:
			if("${EXTRACT:" in str(request_parameter['@value'])):
				searchobj = re.findall(regex_string,str(request_parameter['@value']),re.M|re.I)
				for dp in searchobj:
					temp = "${EXTRACT:"+dp+"}"
					if temp in str(request_parameter['@value']):
						request_parameter['@value'] = str(request_parameter['@value']).replace(temp, read_header(str(dp)))
		return temp_body
	else:
		temp_body  = str(body)
		searchobj = re.findall(regex_string,temp_body,re.M|re.I)
		for dp in searchobj:
			temp = "${EXTRACT:"+dp+"}"
			if temp in temp_body:
				temp_body = temp_body.replace(temp, read_header(str(dp)))
		return temp_body

def extract_process_request_headers(request_headers):
	temp_body  = request_headers
	for request_parameter in temp_body:
		if("${EXTRACT:" in str(request_parameter['@value'])):
			searchobj = re.findall(regex_string,str(request_parameter['@value']),re.M|re.I)
			for dp in searchobj:
				temp = "${EXTRACT:"+dp+"}"
				if temp in str(request_parameter['@value']):
					request_parameter['@value'] = request_parameter['@value'].replace(temp, read_header(str(dp)))
	return temp_body

def extract_process_response_body(response_body):
	temp_body  = str(response_body)
	searchobj = re.findall(regex_string,temp_body,re.M|re.I)
	for dp in searchobj:
		temp = "${EXTRACT:"+dp+"}"
		if temp in temp_body:
			temp_body = temp_body.replace(temp, read_header(str(dp)))
	return temp_body

def extract_process_assert_response_body(assert_response_body):
	temp_body  = assert_response_body
	for request_parameter in temp_body:
		if("${EXTRACT:" in str(request_parameter['#text'])):
			searchobj = re.findall(regex_string,str(request_parameter['#text']),re.M|re.I)
			for dp in searchobj:
				temp = "${EXTRACT:"+dp+"}"
				if temp in str(request_parameter['#text']):
					request_parameter['#text'] = request_parameter['#text'].replace(temp, read_header(str(dp)))
	return temp_body


