from manage_extracts import *
import logging

def merge_request_headers(project_specific, api_specific, test_case_specific):
	temp_header_list = []
	for header in project_specific:
		temp = header['@name'] + ':' + header['@value']
		#print temp
		temp_header_list.append(str(temp))
	for header in test_case_specific:
		if 'EXTRACT' in str(header['@value']):
			header_line = str(header['@value']).split(':')
			header_value = read_header(str(header_line[1]))
		elif('DELETE' in str(header['@value'])):
			header_line = str(header['@value']).split(':')
			header_value = read_header(str(header_line[1]))
			update_header(str(header_line[1]),'')
		else:
			header_value = header['@value']
		temp = header['@name'] + ':' + header_value
		temp_header_list.append(str(temp))
	for header in api_specific:
		temp = header['@name'] + ':' + header['@value']
		temp_header_list.append(str(temp))
	header_list = list(set(temp_header_list))
	return header_list

def merge_response_headers(default, specific):
	temp_header_list = []
	for header in default:
		temp = header['@name'] + ':' + header['@value']
		temp_header_list.append(str(temp))
	for header in specific:
		temp = header['@name'] + ':' + header['@value']
		temp_header_list.append(str(temp))
	header_list = list(set(temp_header_list))
	return header_list


def override_code(specific, default):
	if(specific != 999):
		return specific
	if(default != 888):
		return default
	return 450