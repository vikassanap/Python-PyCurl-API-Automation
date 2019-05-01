import re
import string
import logging

regex_string = "\$\{DP:(.+?)\}"

def dp_process_base_url(data,base_url):
	temp_body  = str(base_url)
	searchobj = re.findall(regex_string,temp_body,re.M|re.I)
	for dp in searchobj:
		temp = "${DP:"+dp+"}"
		if temp in temp_body:
			index = int(dp)
			temp_body = temp_body.replace(temp, data[index])
	return temp_body

def dp_process_request_body(data,body,request_body_type):
	if(request_body_type == 'form'):
		temp_body  = body
		for request_parameter in temp_body:
			if("${DP:" in str(request_parameter['@value'])):
				searchobj = re.findall(regex_string,str(request_parameter['@value']),re.M|re.I)
				for dp in searchobj:
					temp = "${DP:"+dp+"}"
					if temp in str(request_parameter['@value']):
						index = int(dp)
						request_parameter['@value'] = str(request_parameter['@value']).replace(temp, data[index])
		return temp_body
	else:
		temp_body  = str(body)
		searchobj = re.findall(regex_string,temp_body,re.M|re.I)
		for dp in searchobj:
			temp = "${DP:"+dp+"}"
			if temp in temp_body:
				index = int(dp)
				temp_body = temp_body.replace(temp, data[index])
		return temp_body

def dp_process_request_headers(data,request_headers):
	temp_body  = request_headers
	for request_parameter in temp_body:
		if("${DP:" in str(request_parameter['@value'])):
			searchobj = re.findall(regex_string,str(request_parameter['@value']),re.M|re.I)
			for dp in searchobj:
				temp = "${DP:"+dp+"}"
				if temp in str(request_parameter['@value']):
					index = int(dp)
					request_parameter['@value'] = request_parameter['@value'].replace(temp, data[index])
	return temp_body

def dp_process_response_code(data,response_code):
	if '${DP:' in response_code:
		temp_body  = str(response_code)
		searchobj = re.findall(regex_string,temp_body,re.M|re.I)
		for dp in searchobj:
			temp = "${DP:"+dp+"}"
			if temp in temp_body:
				index = int(dp)
				temp_body = temp_body.replace(temp, data[index])
		return int(temp_body)
	else:
		return response_code

def dp_process_response_headers(data,response_headers):
	temp_body  = response_headers
	for request_parameter in temp_body:
		if("${DP:" in str(request_parameter['@value'])):
			searchobj = re.findall(regex_string,str(request_parameter['@value']),re.M|re.I)
			for dp in searchobj:
				temp = "${DP:"+dp+"}"
				if temp in str(request_parameter['@value']):
					index = int(dp)
					request_parameter['@value'] = request_parameter['@value'].replace(temp, data[index])
	return temp_body

def dp_process_response_body(data,response_body):
	temp_body  = str(response_body)
	searchobj = re.findall(regex_string,temp_body,re.M|re.I)
	for dp in searchobj:
		temp = "${DP:"+dp+"}"
		if temp in temp_body:
			index = int(dp)
			temp_body = temp_body.replace(temp, data[index])
	return temp_body

def dp_process_assert_response_body(data,assert_response_body):
	temp_body  = assert_response_body
	for request_parameter in temp_body:
		if("${DP:" in str(request_parameter['#text'])):
			searchobj = re.findall(regex_string,str(request_parameter['#text']),re.M|re.I)
			for dp in searchobj:
				temp = "${DP:"+dp+"}"
				if temp in str(request_parameter['#text']):
					index = int(dp)
					request_parameter['#text'] = request_parameter['#text'].replace(temp, data[index])
	return temp_body


