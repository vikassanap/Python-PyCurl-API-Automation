from get_request import *
from post_request import *
from delete_request import *
from put_request import *
from merge_override import *
from manage_extracts import *
from extract_process import *
import copy
from yaml_process import *
import logging

def execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,test_case_id_p,enable_cookie_flag):
    result = []
    for ts_index in range(len(test_suite_xml_list)):
            test_suite_name = test_suite_xml_list[ts_index]['testSuite']['@name']
            for tc_index in range(len(test_suite_xml_list[ts_index]['testSuite']['testCase'])):
                    test_case =  test_suite_xml_list[ts_index]['testSuite']['testCase'][tc_index]
                    test_case_response_body_type = None
                    test_case_response_body_match =None
                    follow_redirects_flag = 'false'
                    request_body_type = None
                    api_defaultResponse = {}
                    api_defaultHeaders = {}
                    api_defaultHeader = {}
                    api_response_code = 888
                    api_defaultHeadersList  = {}
                    api_defaultRequestHeaderList = {}
                    full_final_request_headers = {}
                    request_body_value_dp={}
                    request_headers_dp={}
                    response_code_dp=0
                    response_headers_dp={}
                    response_body_dp={}
                    assert_response_body_dp={}
                    temp_list={}
                    project_defaultHeaders = {}
                    test_case_request = {}
                    test_case_request_headers = {}
                    test_case_request_body  = {}
                    body_flag = 0
                    body_parameters = {}
                    request_body_value ={}
                    test_case_url = ''
                    body_parameter = {}
                    test_case_response ={}
                    test_case_response_code = 999
                    test_case_response_headers = {} 
                    test_case_response_extract_headers={}
                    test_case_response_assert_headers={}
                    test_case_response_assert_body={}
                    test_case_response_extract_body={}
                    test_case_response_body={}
                    before = None
                    after = None
                    beforeFlag = 0
                    afterFlag = 0
                    final_request_headers={}
                    final_response_headers={}
                    final_response_code= 1000
                    test_case_id = test_case['@testCaseId']
                    if(test_case_id == test_case_id_p):
                        testcase_name = test_case['@name']
                        logging.info("execute_api:Executing test case")
                        group = test_case['@group']
                        api_id = test_case['@apiId']
                        project_id = test_case['@projectId']
                        test_case_request = test_case['request']
                        test_case_url = test_case['@extUrl']
                        try:
                            before = test_case['@before']
                            logging.info("execute_api:Executing before test case")
                            execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,before,enable_cookie_flag)
                        except KeyError:
                            logging.warn("execute_api:Ignoring test case before")
                        try:
                            after = test_case['@after']
                            afterFlag = 1
                        except KeyError:
                            logging.warn("execute_api:Ignoring test cases after")

                        try:
                            test_case_request_headers = test_case_request['headers']['header']
                        except KeyError:
                            pass
                            logging.warn("execute_api:Ignoring test case request headers")
                        try:
                            follow_redirects_flag = test_case_request['@followRedirects']
                        except KeyError:
                            logging.error("execute_api:Please specify followRedirects")
                        try:
                            test_case_request_body = test_case_request['body']
                            body_flag = 1
                        except KeyError:
                            logging.warn("execute_api:Ignoring Test Case Request Body[Only for delete and get request]")
                            body_flag = 0
                        if(body_flag == 1 and test_case_request_body['@type'] == 'form'):
                            try:
                                body_parameters = test_case_request_body['parameter']
                                request_body_value = body_parameters
                                request_body_type = 'form'
                            except KeyError:
                                logging.error("execute_api:No body parameter found")
                        if(body_flag == 1 and test_case_request_body['@type'] == 'text'):
                            try:
                                body_parameter = test_case_request_body['parameter']
                                request_body_value = body_parameter['#text']
                                request_body_type = 'text'
                            except KeyError:
                                logging.error("execute_api:No body parameter found")

                        try:
                            test_case_response =  test_case['response']
                            test_case_response_code = test_case_response['@code']
                            test_case_response_headers = test_case_response['headers']['header']
                        except KeyError:
                            logging.warn("execute_api:Ignoring response headers Specific to test case")
                        try:
                            test_case_response_extract_headers = test_case_response['extractHeader']
                        except KeyError:
                            logging.warn("execute_api:Ignoring extractHeader Specific to test case")
                        try:
                            test_case_response_assert_headers = test_case_response['assertHeaderValue']
                        except KeyError:
                            logging.warn("execute_api:Ignoring assertHeaderValue Specific to test case")
                        try:
                            test_case_response_assert_body = test_case_response['assertBodyValue']
                        except KeyError:
                            logging.warn("execute_api:Ignoring assertBodyValue Specific to test case")
                        try:
                            test_case_response_extract_body = test_case_response['extractBody']
                        except KeyError:
                            logging.warn("execute_api:Ignoring extractBody Specific to test case")
                        try:
                            test_case_response_body = test_case_response['body']['#text']
                            test_case_response_body_type = test_case_response['body']['@type']
                            test_case_response_body_match = test_case_response['body']['@match']
                        except KeyError:
                            logging.warn("execute_api:Ignoring response body Specific to test case")
                        for project_index in range(len(project_info_xml['projectGroup']['project'])):
                            if(project_info_xml['projectGroup']['project'][project_index]['@id'] == project_id):
                                project = project_info_xml['projectGroup']['project'][project_index]
                        project_name = project['@name']

                        for api_list_index in range(len(final_api_list)):
                            temp_api =  final_api_list[api_list_index]
                            if(temp_api['@id'] == api_id):
                                project_api = temp_api

                        base_url = project['@serviceType'] + "://" + project['@baseUrl'] + project_api['@requestUrl'] + test_case_url

                        project_name = project['@name']
                        api_name = project_api['@name']
                        api_request_description = project_api['@requestDescription']
                        api_request_type = project_api['@requestType']

                        try:
                            api_defaultResponse = project_api['defaultResponse']
                            api_defaultHeaders = api_defaultResponse['defaultHeaders']
                            api_defaultHeader =  api_defaultHeaders['defaultHeader']
                            api_response_code = project_api['defaultResponse']['@code']
                            api_defaultHeadersList = project_api['defaultResponse']['defaultHeaders']['defaultHeader']
                        except KeyError:
                            logging.warn("execute_api:Ignoring Header Specific to API")

                        try:
                            api_defaultRequest = project_api['defaultRequest']
                            api_defaultRequestHeaders = api_defaultRequest['defaultRequestHeaders']
                            api_defaultRequestHeaderList =  api_defaultRequestHeaders['header']
                        except KeyError:
                            logging.warn("execute_api:Ignoring Header Specific to API")

                        try:
                            project_defaultHeaders = project['defaultRequestHeaders']['header']
                        except KeyError:
                            logging.warn("execute_api:Ignoring Headers Specific to Project")

                        logging.info("execute_api:Started processing yaml parameters")
                        ###print "YML--------------------------YML"
                        #------extract code
                        #---------------- Start Process Extract
                        base_url_extract = extract_process_base_url(base_url)

                        temp_list = copy.deepcopy(request_body_value)
                        request_body_value_extract = extract_process_request_body(temp_list,request_body_type)
                                
                        temp_list = copy.deepcopy(test_case_request_headers)
                        test_case_request_headers_extract = extract_process_request_headers(temp_list)

                        temp_list = copy.deepcopy(test_case_response_body)
                        test_case_response_body_extract = extract_process_response_body(temp_list)
                                
                        temp_list = copy.deepcopy(test_case_response_assert_body)
                        test_case_response_assert_body_extract = extract_process_assert_response_body(temp_list)

                        #---------------End Process Extract

                        ###print "YML--------------------------YML"
                        base_url_yaml = yaml_process_url(base_url_extract)

                        request_body_value_yaml = yaml_process_request_body(request_body_value_extract,request_body_type)

                        test_case_request_headers_yaml = yaml_process_request_headers(test_case_request_headers_extract)

                        temp_list = copy.deepcopy(project_defaultHeaders)
                        project_defaultHeaders_dp = yaml_process_request_headers(temp_list)

                        temp_list = copy.deepcopy(api_defaultRequestHeaderList)
                        api_defaultRequestHeaderList_dp = yaml_process_request_headers(temp_list)

                        test_case_response_code_yaml  = yaml_process_response_code(test_case_response_code)

                        temp_list = copy.deepcopy(test_case_response_headers)
                        test_case_response_headers_yaml = yaml_process_response_headers(temp_list)

                        temp_list = copy.deepcopy(api_defaultHeadersList)
                        api_defaultHeadersList_dp = yaml_process_response_headers(temp_list)

                        test_case_response_body_yaml = yaml_process_response_body(test_case_response_body_extract)
                                
                        test_case_response_assert_body_yaml = yaml_process_assert_response_body(test_case_response_assert_body_extract)
                        #-----YML Processing Ended---------
                        final_request_headers =  merge_request_headers(project_defaultHeaders_dp,api_defaultRequestHeaderList_dp,test_case_request_headers_yaml)
                        final_response_headers =  merge_response_headers(api_defaultHeadersList_dp,test_case_response_headers_yaml)
                        final_response_code =  override_code(test_case_response_code_yaml, api_response_code)
                        ###print final_response_code
                        if(final_response_code == '302'):
                            test_case_response_body_yaml = ''
                        if api_request_type == 'post':
                                    post_request(project_name,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name, group,base_url_yaml,final_request_headers,request_body_type, request_body_value_yaml,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,test_case_response_extract_headers,"false",follow_redirects_flag,enable_cookie_flag)
                        if api_request_type == 'get':
                            if(final_response_code == '302'):
                                get_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"false",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)
                            else:
                                get_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"false",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)
                        if api_request_type == 'put':
                            put_request(project_name,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name, group,base_url_yaml,final_request_headers,request_body_type, request_body_value_yaml,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,test_case_response_extract_headers,"false",follow_redirects_flag,enable_cookie_flag)
                        if api_request_type == 'delete':
                            delete_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"false",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)   
                        logging.info("execute_api:Executing after test case")
                        execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,after,enable_cookie_flag)    

def execute_api_by_group(project_info_xml,final_api_list,test_suite_xml_list,test_case_group_p,enable_cookie_flag):
    result = []
    for ts_index in range(len(test_suite_xml_list)):
            test_suite_name = test_suite_xml_list[ts_index]['testSuite']['@name']
            for tc_index in range(len(test_suite_xml_list[ts_index]['testSuite']['testCase'])):
                    test_case =  test_suite_xml_list[ts_index]['testSuite']['testCase'][tc_index]
                    test_case_response_body_type = None
                    test_case_response_body_match =None
                    follow_redirects_flag = 'false'
                    request_body_type = None
                    api_defaultResponse = {}
                    api_defaultHeaders = {}
                    api_defaultHeader = {}
                    api_response_code = 888
                    api_defaultHeadersList  = {}
                    api_defaultRequestHeaderList = {}
                    full_final_request_headers = {}
                    request_body_value_dp={}
                    request_headers_dp={}
                    response_code_dp=0
                    response_headers_dp={}
                    test_case_url = ''
                    response_body_dp={}
                    assert_response_body_dp={}
                    group = ''
                    temp_list={}
                    project_defaultHeaders = {}
                    test_case_request = {}
                    test_case_request_headers = {}
                    test_case_request_body  = {}
                    body_flag = 0
                    body_parameters = {}
                    request_body_value ={}
                    body_parameter = {}
                    test_case_response ={}
                    test_case_response_code = 999
                    test_case_response_headers = {} 
                    test_case_response_extract_headers={}
                    test_case_response_assert_headers={}
                    test_case_response_assert_body={}
                    test_case_response_extract_body={}
                    test_case_response_body={}
                    before = None
                    after = None
                    beforeFlag = 0
                    afterFlag = 0
                    final_request_headers={}
                    final_response_headers={}
                    final_response_code= 1000
                    test_case_id = test_case['@testCaseId']
                    group = test_case['@group']
                    if(set(test_case_group_p).intersection(set(group.split(',')))):
                        testcase_name = test_case['@name']
                        logging.info("execute_api:Executing test case")
                        group = test_case['@group']
                        api_id = test_case['@apiId']
                        project_id = test_case['@projectId']
                        test_case_request = test_case['request']
                        test_case_url = test_case['@extUrl']
                        try:
                            before = test_case['@before']
                            logging.info("execute_api: before test")
                            execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,before,enable_cookie_flag)
                        except KeyError:
                            logging.warn("execute_api:Ignoring before")
                        try:
                            after = test_case['@after']
                            afterFlag = 1
                        except KeyError:
                            logging.warn("execute_api:Ignoring after")
                        try:
                            test_case_request_headers = test_case_request['headers']['header']
                        except KeyError:
                            pass
                            logging.warn("execute_api:Ignoring request headers Specific to test case")
                        try:
                            follow_redirects_flag = test_case_request['@followRedirects']
                        except KeyError:
                            logging.warn("execute_api:Ignoring followRedirects")
                        try:
                            test_case_request_body = test_case_request['body']
                            body_flag = 1
                        except KeyError:
                            logging.warn("execute_api:Ignoring Test Case Request Body")
                            body_flag = 0
                        if(body_flag == 1 and test_case_request_body['@type'] == 'form'):
                            try:
                                body_parameters = test_case_request_body['parameter']
                                request_body_value = body_parameters
                                request_body_type = 'form'
                            except KeyError:
                                logging.warn("execute_api:Ignoring form parameters")
                        if(body_flag == 1 and test_case_request_body['@type'] == 'text'):
                            try:
                                body_parameter = test_case_request_body['parameter']
                                request_body_value = body_parameter['#text']
                                request_body_type = 'text'
                            except KeyError:
                                logging.warn("execute_api:Ignoring form: Text")
                        try:
                            test_case_response =  test_case['response']
                            test_case_response_code = test_case_response['@code']
                            test_case_response_headers = test_case_response['headers']['header']
                        except KeyError:
                            logging.warn("execute_api:Ignoring response headers Specific to test case")
                        try:
                            test_case_response_extract_headers = test_case_response['extractHeader']
                        except KeyError:
                            logging.warn("execute_api:Ignoring extractHeader Specific to test case")
                        try:
                            test_case_response_assert_headers = test_case_response['assertHeaderValue']
                        except KeyError:
                            logging.warn("execute_api:Ignoring assertHeaderValue Specific to test case")
                        try:
                            test_case_response_assert_body = test_case_response['assertBodyValue']
                        except KeyError:
                            logging.warn("execute_api:Ignoring assertBodyValue Specific to test case")
                        try:
                            test_case_response_extract_body = test_case_response['extractBody']
                        except KeyError:
                            logging.warn("execute_api:Ignoring extractBody Specific to test case")
                        try:
                            test_case_response_body = test_case_response['body']['#text']
                            test_case_response_body_type = test_case_response['body']['@type']
                            test_case_response_body_match = test_case_response['body']['@match']
                        except KeyError:
                            logging.warn("execute_api:Ignoring response body Specific to test case")
                        for project_index in range(len(project_info_xml['projectGroup']['project'])):
                            if(project_info_xml['projectGroup']['project'][project_index]['@id'] == project_id):
                                project = project_info_xml['projectGroup']['project'][project_index]
                        project_name = project['@name']

                        for api_list_index in range(len(final_api_list)):
                            temp_api =  final_api_list[api_list_index]
                            if(temp_api['@id'] == api_id):
                                project_api = temp_api

                        base_url = project['@serviceType'] + "://" + project['@baseUrl'] + project_api['@requestUrl'] + test_case_url

                        project_name = project['@name']
                        api_name = project_api['@name']
                        api_request_description = project_api['@requestDescription']
                        api_request_type = project_api['@requestType']

                        try:
                            api_defaultResponse = project_api['defaultResponse']
                            api_defaultHeaders = api_defaultResponse['defaultHeaders']
                            api_defaultHeader =  api_defaultHeaders['defaultHeader']
                            api_response_code = project_api['defaultResponse']['@code']
                            api_defaultHeadersList = project_api['defaultResponse']['defaultHeaders']['defaultHeader']
                        except KeyError:
                            logging.warn("execute_api:Ignoring Header Specific to API")

                        try:
                            api_defaultRequest = project_api['defaultRequest']
                            api_defaultRequestHeaders = api_defaultRequest['defaultRequestHeaders']
                            api_defaultRequestHeaderList =  api_defaultRequestHeaders['header']
                        except KeyError:
                            logging.warn("execute_api:Ignoring Header Specific to API")

                        try:
                            project_defaultHeaders = project['defaultRequestHeaders']['header']
                        except KeyError:
                            logging.warn("execute_api:Ignoring Headers Specific to Project")

                        logging.info("execute_api:Started processing yaml parameters")
                                                ###print "YML--------------------------YML"
                        #------extract code
                        #---------------- Start Process Extract
                        base_url_extract = extract_process_base_url(base_url)

                        temp_list = copy.deepcopy(request_body_value)
                        request_body_value_extract = extract_process_request_body(temp_list,request_body_type)
                                
                        temp_list = copy.deepcopy(test_case_request_headers)
                        test_case_request_headers_extract = extract_process_request_headers(temp_list)

                        temp_list = copy.deepcopy(test_case_response_body)
                        test_case_response_body_extract = extract_process_response_body(temp_list)
                                
                        temp_list = copy.deepcopy(test_case_response_assert_body)
                        test_case_response_assert_body_extract = extract_process_assert_response_body(temp_list)

                        #---------------End Process Extract

                        ###print "YML--------------------------YML"
                        base_url_yaml = yaml_process_url(base_url_extract)

                        request_body_value_yaml = yaml_process_request_body(request_body_value_extract,request_body_type)

                        test_case_request_headers_yaml = yaml_process_request_headers(test_case_request_headers_extract)

                        temp_list = copy.deepcopy(project_defaultHeaders)
                        project_defaultHeaders_dp = yaml_process_request_headers(temp_list)

                        temp_list = copy.deepcopy(api_defaultRequestHeaderList)
                        api_defaultRequestHeaderList_dp = yaml_process_request_headers(temp_list)

                        test_case_response_code_yaml  = yaml_process_response_code(test_case_response_code)

                        temp_list = copy.deepcopy(test_case_response_headers)
                        test_case_response_headers_yaml = yaml_process_response_headers(temp_list)

                        temp_list = copy.deepcopy(api_defaultHeadersList)
                        api_defaultHeadersList_dp = yaml_process_response_headers(temp_list)

                        test_case_response_body_yaml = yaml_process_response_body(test_case_response_body_extract)
                                
                        test_case_response_assert_body_yaml = yaml_process_assert_response_body(test_case_response_assert_body_extract)
                        #-----YML Processing Ended---------
                        final_request_headers =  merge_request_headers(project_defaultHeaders_dp,api_defaultRequestHeaderList_dp,test_case_request_headers_yaml)
                        final_response_headers =  merge_response_headers(api_defaultHeadersList_dp,test_case_response_headers_yaml)
                        final_response_code =  override_code(test_case_response_code_yaml, api_response_code)
                        ###print final_response_code
                        if(final_response_code == '302'):
                            test_case_response_body_yaml = ''
                        if api_request_type == 'post':
                                    post_request(project_name,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name, group,base_url_yaml,final_request_headers,request_body_type, request_body_value_yaml,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,test_case_response_extract_headers,"false",follow_redirects_flag,enable_cookie_flag)
                        if api_request_type == 'get':
                            if(final_response_code == '302'):
                                get_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"false",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)
                            else:
                                get_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"false",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)
                        if api_request_type == 'put':
                            put_request(project_name,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name, group,base_url_yaml,final_request_headers,request_body_type, request_body_value_yaml,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,test_case_response_extract_headers,"false",follow_redirects_flag,enable_cookie_flag)
                        if api_request_type == 'delete':
                            delete_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"false",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)   
                        logging.info("execute_api:Executing after")
                        execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,after,enable_cookie_flag) 

def execute_api_by_tag(project_info_xml,final_api_list,test_suite_xml_list,test_case_tag_p,enable_cookie_flag):
    result = []
    for ts_index in range(len(test_suite_xml_list)):
            test_suite_name = test_suite_xml_list[ts_index]['testSuite']['@name']
            for tc_index in range(len(test_suite_xml_list[ts_index]['testSuite']['testCase'])):
                    test_case =  test_suite_xml_list[ts_index]['testSuite']['testCase'][tc_index]
                    test_case_response_body_type = None
                    test_case_response_body_match =None
                    follow_redirects_flag = 'false'
                    request_body_type = None
                    api_defaultResponse = {}
                    api_defaultHeaders = {}
                    api_defaultHeader = {}
                    api_response_code = 888
                    test_case_url = ''
                    api_defaultHeadersList  = {}
                    api_defaultRequestHeaderList = {}
                    full_final_request_headers = {}
                    request_body_value_dp={}
                    request_headers_dp={}
                    response_code_dp=0
                    response_headers_dp={}
                    response_body_dp={}
                    assert_response_body_dp={}
                    temp_list={}
                    project_defaultHeaders = {}
                    test_case_request = {}
                    test_case_request_headers = {}
                    test_case_request_body  = {}
                    body_flag = 0
                    tag = ''
                    body_parameters = {}
                    request_body_value ={}
                    body_parameter = {}
                    test_case_response ={}
                    test_case_response_code = 999
                    test_case_response_headers = {} 
                    test_case_response_extract_headers={}
                    test_case_response_assert_headers={}
                    test_case_response_assert_body={}
                    test_case_response_extract_body={}
                    test_case_response_body={}
                    before = None
                    after = None
                    beforeFlag = 0
                    afterFlag = 0
                    final_request_headers={}
                    final_response_headers={}
                    final_response_code= 1000
                    test_case_id = test_case['@testCaseId']
                    group = test_case['@group']
                    tag = test_case['@tag']
                    
                    if(set(tag.split(',')).intersection(set(test_case_tag_p))):
                        testcase_name = test_case['@name']
                        group = test_case['@group']
                        api_id = test_case['@apiId']
                        project_id = test_case['@projectId']
                        test_case_request = test_case['request']
                        test_case_url = test_case['@extUrl']
                        try:
                            before = test_case['@before']
                            logging.info("execute_api:Executing before")
                            execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,before,enable_cookie_flag)
                        except KeyError:
                            logging.warn("execute_api:Ignoring test case before")
                        try:
                            after = test_case['@after']
                            afterFlag = 1
                        except KeyError:
                            logging.warn("execute_api:Ignoring test case after")
                        try:
                            test_case_request_headers = test_case_request['headers']['header']
                        except KeyError:
                            logging.warn("execute_api:Ignoring request headers Specific to test case")
                        try:
                            follow_redirects_flag = test_case_request['@followRedirects']
                        except KeyError:
                            logging.warn("execute_api:Ignoring followRedirects")
                        try:
                            test_case_request_body = test_case_request['body']
                            body_flag = 1
                        except KeyError:
                            logging.warn("execute_api:Ignoring Test Case Request Body")
                            body_flag = 0
                        if(body_flag == 1 and test_case_request_body['@type'] == 'form'):
                            try:
                                body_parameters = test_case_request_body['parameter']
                                request_body_value = body_parameters
                                request_body_type = 'form'
                            except KeyError:
                                logging.warn("execute_api:Ignoring form parameters")
                        if(body_flag == 1 and test_case_request_body['@type'] == 'text'):
                            try:
                                body_parameter = test_case_request_body['parameter']
                                request_body_value = body_parameter['#text']
                                request_body_type = 'text'
                            except KeyError:
                                logging.warn("execute_api:Ignoring form: Text")

                        try:
                            test_case_response =  test_case['response']
                            test_case_response_code = test_case_response['@code']
                            test_case_response_headers = test_case_response['headers']['header']
                        except KeyError:
                            logging.warn("execute_api:Ignoring response headers Specific to test case")
                        try:
                            test_case_response_extract_headers = test_case_response['extractHeader']
                        except KeyError:
                            pass
                            logging.warn("execute_api:Ignoring extractHeader Specific to test case")
                        try:
                            test_case_response_assert_headers = test_case_response['assertHeaderValue']
                        except KeyError:
                            logging.warn("execute_api:Ignoring assertHeaderValue Specific to test case")
                        try:
                            test_case_response_assert_body = test_case_response['assertBodyValue']
                        except KeyError:
                            logging.warn("execute_api:Ignoring assertBodyValue Specific to test case")
                        try:
                            test_case_response_extract_body = test_case_response['extractBody']
                        except KeyError:
                            logging.warn("execute_api:Ignoring extractBody Specific to test case")
                        try:
                            test_case_response_body = test_case_response['body']['#text']
                            test_case_response_body_type = test_case_response['body']['@type']
                            test_case_response_body_match = test_case_response['body']['@match']
                        except KeyError:
                            logging.warn("execute_api:Ignoring response body Specific to test case")

                        for project_index in range(len(project_info_xml['projectGroup']['project'])):
                            if(project_info_xml['projectGroup']['project'][project_index]['@id'] == project_id):
                                project = project_info_xml['projectGroup']['project'][project_index]
                        project_name = project['@name']

                        for api_list_index in range(len(final_api_list)):
                            temp_api =  final_api_list[api_list_index]
                            if(temp_api['@id'] == api_id):
                                project_api = temp_api

                        base_url = project['@serviceType'] + "://" + project['@baseUrl'] + project_api['@requestUrl'] +test_case_url


                        project_name = project['@name']
                        api_name = project_api['@name']
                        api_request_description = project_api['@requestDescription']
                        api_request_type = project_api['@requestType']

                        try:
                            api_defaultResponse = project_api['defaultResponse']
                            api_defaultHeaders = api_defaultResponse['defaultHeaders']
                            api_defaultHeader =  api_defaultHeaders['defaultHeader']
                            api_response_code = project_api['defaultResponse']['@code']
                            api_defaultHeadersList = project_api['defaultResponse']['defaultHeaders']['defaultHeader']
                        except KeyError:
                            logging.warn("execute_api:Ignoring Header Specific to API")
                        try:
                            api_defaultRequest = project_api['defaultRequest']
                            api_defaultRequestHeaders = api_defaultRequest['defaultRequestHeaders']
                            api_defaultRequestHeaderList =  api_defaultRequestHeaders['header']
                        except KeyError:
                            logging.warn("execute_api:Ignoring Header Specific to API")
                        try:
                            project_defaultHeaders = project['defaultRequestHeaders']['header']
                        except KeyError:
                            logging.warn("execute_api:Ignoring Headers Specific to Project")

                        logging.info("execute_api:Started processing yaml parameters")
                                                ###print "YML--------------------------YML"
                        #------extract code
                        #---------------- Start Process Extract
                        base_url_extract = extract_process_base_url(base_url)

                        temp_list = copy.deepcopy(request_body_value)
                        request_body_value_extract = extract_process_request_body(temp_list,request_body_type)
                                
                        temp_list = copy.deepcopy(test_case_request_headers)
                        test_case_request_headers_extract = extract_process_request_headers(temp_list)

                        temp_list = copy.deepcopy(test_case_response_body)
                        test_case_response_body_extract = extract_process_response_body(temp_list)
                                
                        temp_list = copy.deepcopy(test_case_response_assert_body)
                        test_case_response_assert_body_extract = extract_process_assert_response_body(temp_list)

                        #---------------End Process Extract

                        ###print "YML--------------------------YML"
                        base_url_yaml = yaml_process_url(base_url_extract)

                        request_body_value_yaml = yaml_process_request_body(request_body_value_extract,request_body_type)

                        test_case_request_headers_yaml = yaml_process_request_headers(test_case_request_headers_extract)

                        temp_list = copy.deepcopy(project_defaultHeaders)
                        project_defaultHeaders_dp = yaml_process_request_headers(temp_list)

                        temp_list = copy.deepcopy(api_defaultRequestHeaderList)
                        api_defaultRequestHeaderList_dp = yaml_process_request_headers(temp_list)

                        test_case_response_code_yaml  = yaml_process_response_code(test_case_response_code)

                        temp_list = copy.deepcopy(test_case_response_headers)
                        test_case_response_headers_yaml = yaml_process_response_headers(temp_list)

                        temp_list = copy.deepcopy(api_defaultHeadersList)
                        api_defaultHeadersList_dp = yaml_process_response_headers(temp_list)

                        test_case_response_body_yaml = yaml_process_response_body(test_case_response_body_extract)
                                
                        test_case_response_assert_body_yaml = yaml_process_assert_response_body(test_case_response_assert_body_extract)
                        #-----YML Processing Ended---------
                        final_request_headers =  merge_request_headers(project_defaultHeaders_dp,api_defaultRequestHeaderList_dp,test_case_request_headers_yaml)
                        final_response_headers =  merge_response_headers(api_defaultHeadersList_dp,test_case_response_headers_yaml)
                        final_response_code =  override_code(test_case_response_code_yaml, api_response_code)
                        ###print final_response_code
                        if(final_response_code == '302'):
                            test_case_response_body_yaml = ''
                        if api_request_type == 'post':
                                    post_request(project_name,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name, group,base_url_yaml,final_request_headers,request_body_type, request_body_value_yaml,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,test_case_response_extract_headers,"false",follow_redirects_flag,enable_cookie_flag)
                        if api_request_type == 'get':
                            if(final_response_code == '302'):
                                get_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"false",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)
                            else:
                                get_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"false",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)
                        if api_request_type == 'put':
                            put_request(project_name,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name, group,base_url_yaml,final_request_headers,request_body_type, request_body_value_yaml,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,test_case_response_extract_headers,"false",follow_redirects_flag,enable_cookie_flag)
                        if api_request_type == 'delete':
                            delete_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"false",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)   
                        logging.info("execute_api:Executing after")
                        execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,after,enable_cookie_flag) 
