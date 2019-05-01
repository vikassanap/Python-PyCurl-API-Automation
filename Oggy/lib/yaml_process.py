import re
import string
import os
import yaml
import logging
PATH = os.getcwd()

regex_string = "\$\{YML:(.+?)\}"

def yaml_process_request_body(body,request_body_type):
	#print "inside dp process request body", body
	#print body

	if(request_body_type == 'form'):
		temp_body  = body
		#print temp_body
		for request_parameter in temp_body:
			if("${YML:" in str(request_parameter['@value'])):
				searchobj = re.findall(regex_string,str(request_parameter['@value']),re.M|re.I)
				for dp in searchobj:
					temp = "${YML:"+dp+"}"
					#print temp
					if temp in str(request_parameter['@value']):
						yml_path = dp.split(':')
						yml_file_name = yml_path[0]
						fname = PATH+"/test_data/yaml/"+yml_file_name+".yml"
    					with open(fname) as f:
        					YML_FILE = yaml.load(f)
						index = 1
						while index < len(yml_path):
							if index == len(yml_path) - 1:
								replace_value = YML_FILE[yml_path[index]]
								#print replace_value
								break
							else:
								YML_FILE = YML_FILE[yml_path[index]]
								#print YML_FILE
								index = index + 1
						request_parameter['@value'] = str(request_parameter['@value']).replace(temp, replace_value)
						#print request_parameter['@value']
				#print temp_body
		return temp_body
	else:
		temp_body  = str(body)
		#print temp_body
		searchobj = re.findall(regex_string,temp_body,re.M|re.I)
		for dp in searchobj:
			temp = "${YML:"+dp+"}"
		#print temp
			if temp in temp_body:
				yml_path = dp.split(':')
				yml_file_name = yml_path[0]
				fname = PATH+"/test_data/yaml/"+yml_file_name+".yml"
    			with open(fname) as f:
        			YML_FILE = yaml.load(f)
				index = 1
				while index < len(yml_path):
					if index == len(yml_path) - 1:
						replace_value = YML_FILE[yml_path[index]]
						#print replace_value
						break
					else:
						YML_FILE = YML_FILE[yml_path[index]]
						#print YML_FILE
						index = index + 1
				temp_body = temp_body.replace(temp, replace_value)
				#print temp_body
		#print temp_body
		return temp_body

def yaml_process_request_headers(request_headers):
	#print "inside dp process request headers",request_headers
	#print "inside dp process request headers",type(request_headers)
	temp_body  = request_headers
	#print temp_body
	for request_parameter in temp_body:
		if("${YML:" in str(request_parameter['@value'])):
			searchobj = re.findall(regex_string,str(request_parameter['@value']),re.M|re.I)
			for dp in searchobj:
				temp = "${YML:"+dp+"}"
				#print temp
				if temp in str(request_parameter['@value']):
					yml_path = dp.split(':')
					yml_file_name = yml_path[0]
					fname = PATH+"/test_data/yaml/"+yml_file_name+".yml"
    				with open(fname) as f:
        				YML_FILE = yaml.load(f)
					index = 1
					while index < len(yml_path):
						if index == len(yml_path) - 1:
							replace_value = YML_FILE[yml_path[index]]
							#print replace_value
							break
						else:
							YML_FILE = YML_FILE[yml_path[index]]
							#print YML_FILE
							index = index + 1
					request_parameter['@value'] = str(request_parameter['@value']).replace(temp, replace_value)
					#print request_parameter['@value']
			#print temp_body
	return temp_body

def yaml_process_response_code(response_code):
	#print "inside dp response code", response_code
	#print "inside dp response code", type(response_code)
	if "${YML:" in str(response_code):
		temp_body  = str(response_code)
		#print temp_body
		searchobj = re.findall(regex_string,temp_body,re.M|re.I)
		for dp in searchobj:
			temp = "${YML:"+dp+"}"
			#print temp
			if temp in temp_body:
				yml_path = dp.split(':')
				yml_file_name = yml_path[0]
				fname = PATH+"/test_data/yaml/"+yml_file_name+".yml"
	    		with open(fname) as f:
	        		YML_FILE = yaml.load(f)
				index = 1
				while index < len(yml_path):
					if index == len(yml_path) - 1:
						replace_value = YML_FILE[yml_path[index]]
						#print replace_value
						break
					else:
						YML_FILE = YML_FILE[yml_path[index]]
						#print YML_FILE
						index = index + 1
				temp_body = temp_body.replace(temp, str(replace_value))
				#print temp_body
		#print temp_body
		return int(temp_body)
	else:
		return response_code

def yaml_process_response_headers(response_headers):
	#print "inside dp response headers", response_headers
	#print "inside dp response headers", type(response_headers)
	temp_body  = response_headers
	#print temp_body
	for request_parameter in temp_body:
		if("${YML:" in str(request_parameter['@value'])):
			searchobj = re.findall(regex_string,str(request_parameter['@value']),re.M|re.I)
			for dp in searchobj:
				temp = "${YML:"+dp+"}"
				#print temp
				if temp in str(request_parameter['@value']):
					yml_path = dp.split(':')
					yml_file_name = yml_path[0]
					fname = PATH+"/test_data/yaml/"+yml_file_name+".yml"
    				with open(fname) as f:
        				YML_FILE = yaml.load(f)
					index = 1
					while index < len(yml_path):
						if index == len(yml_path) - 1:
							replace_value = YML_FILE[yml_path[index]]
							#print replace_value
							break
						else:
							YML_FILE = YML_FILE[yml_path[index]]
							#print YML_FILE
							index = index + 1
					request_parameter['@value'] = request_parameter['@value'].replace(temp, replace_value)
					#print request_parameter['@value']
			#print temp_body
	return temp_body

def yaml_process_response_body(response_body):
	#print "inside dp response body", response_body
	#print "inside dp response body", type(response_body)
	temp_body  = str(response_body)
	#print temp_body
	searchobj = re.findall(regex_string,temp_body,re.M|re.I)
	for dp in searchobj:
		temp = "${YML:"+dp+"}"
		#print temp
		if temp in temp_body:
			yml_path = dp.split(':')
			yml_file_name = yml_path[0]
			fname = PATH+"/test_data/yaml/"+yml_file_name+".yml"
    		with open(fname) as f:
        		YML_FILE = yaml.load(f)
			index = 1
			while index < len(yml_path):
				if index == len(yml_path) - 1:
					replace_value = YML_FILE[yml_path[index]]
					#print replace_value
					break
				else:
					YML_FILE = YML_FILE[yml_path[index]]
					#print YML_FILE
					index = index + 1
			temp_body = temp_body.replace(temp, replace_value)
			#print temp_body
	#print temp_body
	return temp_body

def yaml_process_assert_response_body(assert_response_body):
	#print "inside dp assert response body", assert_response_body
	#print "inside dp assert response body", type(assert_response_body)
	temp_body  = assert_response_body
	#print temp_body
	for request_parameter in temp_body:
		if("${YML:" in str(request_parameter['#text'])):
			searchobj = re.findall(regex_string,str(request_parameter['#text']),re.M|re.I)
			for dp in searchobj:
				temp = "${YML:"+dp+"}"
				#print temp
				if temp in str(request_parameter['#text']):
					yml_path = dp.split(':')
					yml_file_name = yml_path[0]
					fname = PATH+"/test_data/yaml/"+yml_file_name+".yml"
    				with open(fname) as f:
        				YML_FILE = yaml.load(f)
					index = 1
					while index < len(yml_path):
						if index == len(yml_path) - 1:
							replace_value = YML_FILE[yml_path[index]]
							#print replace_value
							break
						else:
							YML_FILE = YML_FILE[yml_path[index]]
							#print YML_FILE
							index = index + 1
					request_parameter['#text'] = request_parameter['#text'].replace(temp, replace_value)
					#print request_parameter['#text']
			#print temp_body
	return temp_body

def yaml_process_url(base_url):
	if "${YML:" in str(base_url):
		temp_body  = str(base_url)
		#print temp_body
		searchobj = re.findall(regex_string,temp_body,re.M|re.I)
		for dp in searchobj:
			temp = "${YML:"+dp+"}"
			#print temp
			if temp in temp_body:
				yml_path = dp.split(':')
				yml_file_name = yml_path[0]
				fname = PATH+"/test_data/yaml/"+yml_file_name+".yml"
	    		with open(fname) as f:
	        		YML_FILE = yaml.load(f)
				index = 1
				while index < len(yml_path):
					if index == len(yml_path) - 1:
						replace_value = YML_FILE[yml_path[index]]
						#print replace_value
						break
					else:
						YML_FILE = YML_FILE[yml_path[index]]
						#print YML_FILE
						index = index + 1
				temp_body = temp_body.replace(temp, str(replace_value))
				#print temp_body
		#print temp_body
		return temp_body
	else:
		return base_url


