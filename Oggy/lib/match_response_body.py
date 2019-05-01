import os
import logging

PATH = os.getcwd()

def match_response_body(test_case_response_body_type, test_case_response_body_match, actual_response_body, expected_response_body):
	result = 'NA'
	input_file_name = PATH
	reason = ''

	#print "$$$$$$$$$$$$$$$$$$",test_case_response_body_type, test_case_response_body_match

	if test_case_response_body_type == 'html' and test_case_response_body_match == 'contains':
		#print "Inside html,contains"
		if expected_response_body.strip() in actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+expected_response_body.strip()+ " Actual Response Body => "+actual_response_body.strip()
	elif test_case_response_body_type == 'html' and test_case_response_body_match == 'matches':
		#print "Inside html,matches"
		if expected_response_body.strip() == actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+expected_response_body.strip()+ " Actual Response Body => "+actual_response_body.strip()

	elif test_case_response_body_type == 'html' and test_case_response_body_match == 'contains:file':
		with open(input_file_name+"/test_data/assert_files/"+expected_response_body,'r') as myfile:
			file_contents = myfile.read().strip()
			#print file_contents
		if file_contents in actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+file_contents+ " Actual Response Body => "+actual_response_body.strip()

	elif test_case_response_body_type == 'html' and test_case_response_body_match == 'matches:file':
		with open(input_file_name+"/test_data/assert_files/"+expected_response_body,'r') as myfile:
			file_contents = myfile.read().strip()
			#print file_contents
		if file_contents  ==  actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+file_contents+ " Actual Response Body => "+actual_response_body.strip()

	if test_case_response_body_type == 'json' and test_case_response_body_match == 'contains':
		#print "Inside json,contains"
		if expected_response_body.strip() in actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+expected_response_body.strip()+ " Actual Response Body => "+actual_response_body.strip()

	elif test_case_response_body_type == 'json' and test_case_response_body_match == 'matches':
		#print "Inside json,matches"
		if expected_response_body.strip() == actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+expected_response_body.strip()+ " Actual Response Body => "+actual_response_body.strip()

	elif test_case_response_body_type == 'json' and test_case_response_body_match == 'contains:file':
		with open(input_file_name+"/test_data/assert_files/"+expected_response_body,'r') as myfile:
			file_contents = myfile.read().strip()
			#print file_contents
		if file_contents in actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+file_contents+ " Actual Response Body => "+actual_response_body.strip()

	elif test_case_response_body_type == 'json' and test_case_response_body_match == 'matches:file':
		with open(input_file_name+"/test_data/assert_files/"+expected_response_body,'r') as myfile:
			file_contents = myfile.read().strip()
			#print file_contents
		if file_contents  ==  actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+file_contents+ " Actual Response Body => "+actual_response_body.strip()

	if test_case_response_body_type == 'xml' and test_case_response_body_match == 'contains':
		#print "Inside xml,contains"
		if expected_response_body.strip() in actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+expected_response_body.strip()+ " Actual Response Body => "+actual_response_body.strip()

	elif test_case_response_body_type == 'xml' and test_case_response_body_match == 'matches':
		#print "Inside xml,matches"
		if expected_response_body.strip() == actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+expected_response_body.strip()+ " Actual Response Body => "+actual_response_body.strip()

	elif test_case_response_body_type == 'xml' and test_case_response_body_match == 'contains:file':
		with open(input_file_name+"/test_data/assert_files/"+expected_response_body,'r') as myfile:
			file_contents = myfile.read().strip()
			#print file_contents
		if file_contents in actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+file_contents+ " Actual Response Body => "+actual_response_body.strip()

	elif test_case_response_body_type == 'xml' and test_case_response_body_match == 'matches:file':
		with open(input_file_name+"/test_data/assert_files/"+expected_response_body,'r') as myfile:
			file_contents = myfile.read().strip()
			#print file_contents
		if file_contents  ==  actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+file_contents+ " Actual Response Body => "+actual_response_body.strip()

	if test_case_response_body_type == 'text' and test_case_response_body_match == 'contains':
		#print "Inside text,contains"
		if expected_response_body.strip() in actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+expected_response_body.strip()+ " Actual Response Body => "+actual_response_body.strip()

	elif test_case_response_body_type == 'text' and test_case_response_body_match == 'matches':
		#print "Inside text,matches"
		if expected_response_body.strip() == actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+expected_response_body.strip()+ " Actual Response Body => "+actual_response_body.strip()

	elif test_case_response_body_type == 'text' and test_case_response_body_match == 'contains:file':
		with open(input_file_name+"/test_data/assert_files/"+expected_response_body,'r') as myfile:
			file_contents = myfile.read().strip()
			#print file_contents
		if file_contents in actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+file_contents+ " Actual Response Body => "+actual_response_body.strip()

	elif test_case_response_body_type == 'text' and test_case_response_body_match == 'matches:file':
		with open(input_file_name+"/test_data/assert_files/"+expected_response_body,'r') as myfile:
			file_contents = myfile.read().strip()
			#print file_contents
		if file_contents  ==  actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+file_contents+ " Actual Response Body => "+actual_response_body.strip()

	if test_case_response_body_type == 'file' and test_case_response_body_match == 'nothing':
		#print "Inside file,nothing"
		list_file_name = expected_response_body.split(',')
		match_file_name = list_file_name[0]
		expected_file_name = list_file_name[1]
		if expected_response_body.strip() in actual_response_body.strip():
			result = 'pass'
		else:
			result = 'fail'
			reason = 'Response Body Match Error : Expected Response Body => '+expected_response_body.strip()+ " Actual Response Body => "+actual_response_body.strip()

	return (result,reason)
