from get_request import *
from post_request import *
from delete_request import *
from put_request import *
from merge_override import *
from execute_api import *
from manage_extracts import *
from dp_process import *
from yaml_process import *
from extract_process import *
import csv,os
import copy
PATH = os.getcwd()
import logging

def execute_apis(project_info_xml,final_api_list,test_suite_xml_list,test_suite_list,tags = "", all = 'true'):
    result = []
    for ts_index in range(len(test_suite_xml_list)):
        follow_redirects_flag = 'false'
        beforeAll = None
        beforeAllFlag = 0
        afterAll = None
        afterAllFlag = 0
        beforeTest = None
        beforeTestFlag = 0
        afterTest = None
        afterTestFlag = 0
        data_provider = None
        data_provider_flag = 0
        enable_cookie_flag = 'false'
        if(test_suite_xml_list[ts_index]['testSuite']['@name'] in test_suite_list or all == 'true'):
            try:
                test_suite = test_suite_xml_list[ts_index]['testSuite']
                test_suite_name = test_suite['@name']
                beforeAll = test_suite['@beforeAll']
                beforeAllFlag = 1
            except KeyError:
                logging.warn("execute_apis:Ignoring test suite name, beforeAll")
            try:
                afterAll = test_suite['@afterAll']
                afterAllFlag = 1
            except KeyError:
                logging.warn("execute_apis:Ignoring afterAll")
            try:
                beforeTest = test_suite['@beforeTest']
                beforeTestFlag = 1
            except KeyError:
                logging.warn("execute_apis:Ignoring beforeTest")
            try:
                afterTest = test_suite['@afterTest']
                afterTestFlag = 1
            except KeyError:
                logging.warn("execute_apis:Ignoring afterTest")
            try:
                data_provider = test_suite['@dataProvider']
                if data_provider == '':
                    data_provider_flag = 0
                else:
                    data_provider_flag = 1
            except KeyError:
                logging.warn("execute_apis:Ignoring data_provider")
            try:
                enable_cookie = test_suite['@enableCookie']
                if(str(enable_cookie) == 'true'):
                    enable_cookie_flag = 'true'
            except KeyError:
                logging.warn("execute_apis:Ignoring enable_cookie_flag")
                
            if(beforeAllFlag == 1):
                logging.info("execute_apis:executing Before All ")
                execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,beforeAll,enable_cookie_flag)
            if(data_provider_flag == 1):
                file_name = PATH+"/test_data/data_providers/"+data_provider
                with open(file_name, 'rb') as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        for tc_index in range(len(test_suite_xml_list[ts_index]['testSuite']['testCase'])):
                                if(beforeTestFlag == 1):
                                    logging.info("executing before test")
                                    execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,beforeTest,enable_cookie_flag)
                                test_case =  test_suite_xml_list[ts_index]['testSuite']['testCase'][tc_index]
                                test_case_response_body_type = None
                                test_case_response_body_match =None
                                request_body_type = None
                                api_defaultResponse = {}
                                api_defaultHeaders = {}
                                api_defaultHeader = {}
                                api_response_code = 888
                                api_defaultHeadersList  = {}
                                api_defaultRequestHeaderList = {}
                                full_final_request_headers = {}
                                project_defaultHeaders = {}
                                test_case_request = {}
                                test_case_request_headers = {}
                                test_case_request_body  = {}
                                body_flag = 0
                                test_case_url = ''
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
                                #-------DP
                                request_body_value_dp={}
                                request_headers_dp={}
                                response_code_dp=0
                                response_headers_dp={}
                                response_body_dp={}
                                assert_response_body_dp={}
                                #-------DP
                                temp_list={}
                                before = None
                                after = None
                                beforeFlag = 0
                                afterFlag = 0
                                final_request_headers={}
                                final_response_headers={}
                                final_response_code= 1000
                                testcase_name = test_case['@name']
                                group = test_case['@group']
                                api_id = test_case['@apiId']
                                project_id = test_case['@projectId']
                                test_case_request = test_case['request']
                                test_case_id = test_case['@testCaseId']
                                test_case_url = test_case['@extUrl']
                                ###print "#--------------------------"
                                ###print "-----*before and after extraction*---------"
                                try:
                                    before = test_case['@before']
                                    logging.info("executing before")
                                    execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,before,enable_cookie_flag)
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring before execution")
                                try:
                                    after = test_case['@after']
                                    afterFlag = 1
                                except KeyError:
                                    logging.warn("execute_apis:after flag is set")

                                ###print "------*Request Headers: Specific to Test Case"
                                try:
                                    test_case_request_headers = test_case_request['headers']['header']
                                    #for header in test_case_request_headers:
                                        ###print header['@name'] + " --> " + header['@value']
                                except KeyError: 
                                    logging.warn("execute_apis:Ignoring test case request headers")
                                    ###print ""
                                    ###print "Ignoring request headers Specific to test case"
                                try:
                                    follow_redirects_flag = test_case_request['@followRedirects']
                                    ###print "*******", follow_redirects_flag

                                except KeyError:
                                    logging.warn("execute_apis:Ignoring followRedirects")
                                ###print "------*Request Body*------"
                                ###print "identifying body"
                                try:
                                    test_case_request_body = test_case_request['body']
                                    ###print test_case_request_body['@type']
                                    body_flag = 1
                                except KeyError:
                                    ###print ""
                                    logging.warn("execute_apis:Ignoring test case body")
                                    body_flag = 0
                                if(body_flag == 1 and test_case_request_body['@type'] == 'form'):
                                    try:
                                        body_parameters = test_case_request_body['parameter']
                                        #for parameter  in body_parameters:
                                            ###print parameter['@name'] + " -- " + parameter['@type'] + "--" +parameter['@value']
                                        request_body_value = body_parameters
                                        request_body_type = 'form'
                                    except KeyError:
                                        logging.warn("execute_apis:Ignoring request body parameters")
                                        ###print ""
                                        ###print "Ignoring form parameters"
                                if(body_flag == 1 and test_case_request_body['@type'] == 'text'):
                                    try:
                                        body_parameter = test_case_request_body['parameter']
                                        ###print body_parameter['@type']
                                        ###print body_parameter['#text']
                                        request_body_value = body_parameter['#text']
                                        request_body_type = 'text'
                                    except KeyError:
                                        logging.warn("execute_apis:Ignoring request body text")

                                ###print "------*Response Headers: Specific to Test Case*------"
                                try:
                                    test_case_response =  test_case['response']
                                    test_case_response_code = test_case_response['@code']
                                    test_case_response_headers = test_case_response['headers']['header']
                                    #for header in test_case_response_headers:
                                        ###print header['@name'] + " --> " + header['@value']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring test case response headers")
                                try:
                                    ###print "------*Extract Header Values*------"
                                    test_case_response_extract_headers = test_case_response['extractHeader']
                                    #for response_extract_header in test_case_response_extract_headers:
                                        ###print response_extract_header['@name'] + " --> " + response_extract_header['#text']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring test case header extraction")
                                try:
                                    ###print "------*Assert Header Value*------"
                                    test_case_response_assert_headers = test_case_response['assertHeaderValue']
                                    #for test_case_response_assert_header in test_case_response_assert_headers:
                                        ###print test_case_response_assert_header['@name'] + " --> " + test_case_response_assert_header['#text']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring assertHeaderValue")
                                try:
                                    ###print "------*Assert body value*------"
                                    test_case_response_assert_body = test_case_response['assertBodyValue']
                                    #for test_case_response_assert_body_param in test_case_response_assert_body:
                                            ###print "--------------"+test_case_response_assert_body_param['@type'] + " + " + test_case_response_assert_body_param['@method']+ " + " + test_case_response_assert_body_param['@exp']+ " --> " + test_case_response_assert_body_param['#text']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring assertBodyValue")
                                try:
                                    ###print "------*Extract body value*------"
                                    test_case_response_extract_body = test_case_response['extractBody']
                                    #for test_case_response_extract_param in test_case_response_extract_body:
                                            ###print "--------------"+test_case_response_extract_param['@type'] + " + " + test_case_response_extract_param['@method']+ " + " + test_case_response_extract_param['@exp']+ " --> " + test_case_response_extract_param['#text']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring extractBody")
                                try:
                                    ###print "------*Response body value*------"
                                    test_case_response_body = test_case_response['body']['#text']
                                    test_case_response_body_type = test_case_response['body']['@type']
                                    test_case_response_body_match = test_case_response['body']['@match']
                                    ###print test_case_response_body['@type'] + " --> " + test_case_response_body['@match']+ " --> " + test_case_response_body['#text']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring response body")
                                ###print "-================================================-"
                                ###print project_defaultHeaders
                                ###print test_case_request_headers
                                ###print api_defaultHeadersList
                                ###print test_case_response_headers
                                for project_index in range(len(project_info_xml['projectGroup']['project'])):
                                    if(project_info_xml['projectGroup']['project'][project_index]['@id'] == project_id):
                                        project = project_info_xml['projectGroup']['project'][project_index]
                                project_name = project['@name']

                                for api_list_index in range(len(final_api_list)):
                                    temp_api =  final_api_list[api_list_index]
                                    if(temp_api['@id'] == api_id):
                                        project_api = temp_api

                                base_url = project['@serviceType'] + "://" + project['@baseUrl'] + project_api['@requestUrl'] + test_case_url

                                ###print base_url
                                project_name = project['@name']
                                api_name = project_api['@name']
                                api_request_description = project_api['@requestDescription']
                                api_request_type = project_api['@requestType']

                                    ###print "------*Default Header: Specific to API*------"
                                try:
                                    api_defaultResponse = project_api['defaultResponse']
                                    api_defaultHeaders = api_defaultResponse['defaultHeaders']
                                    api_defaultHeader =  api_defaultHeaders['defaultHeader']
                                    api_response_code = project_api['defaultResponse']['@code']
                                    ###print api_response_code
                                    api_defaultHeadersList = project_api['defaultResponse']['defaultHeaders']['defaultHeader']
                                    #for default_header in api_defaultHeadersList:
                                        ###print default_header['@name'] + "  -->  " + default_header['@value']
                                except KeyError:
                                    ###print ""
                                    logging.warn("execute_apis:Ignoring response headers Specific to api")

                                try:
                                    api_defaultRequest = project_api['defaultRequest']
                                    api_defaultRequestHeaders = api_defaultRequest['defaultRequestHeaders']
                                    api_defaultRequestHeaderList =  api_defaultRequestHeaders['header']
                                    ###print "@@@",api_defaultRequestHeaderList is list
                                    #for default_header in api_defaultRequestHeaderList:
                                        ###print default_header['@name'] + "  -->  " + default_header['@value']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring request body parameters")


                                ###print "------*Default Header: Specific to Project*------"
                                try:
                                    project_defaultHeaders = project['defaultRequestHeaders']['header']
                                    #for header in project_defaultHeaders:
                                        ###print header['@name'] + " --> " +header['@value']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring request headers Specific to project")

                                ###print "before:",request_body_value
                                #------------- Start process dp

                                base_url_dp = dp_process_base_url(row,base_url)

                                temp_list = copy.deepcopy(request_body_value)
                                request_body_value_dp = dp_process_request_body(row,temp_list,request_body_type)

                                temp_list = copy.deepcopy(test_case_request_headers)
                                test_case_request_headers_dp = dp_process_request_headers(row,temp_list)

                                test_case_response_code_dp  = dp_process_response_code(row,test_case_response_code)

                                temp_list = copy.deepcopy(test_case_response_headers)
                                test_case_response_headers_dp = dp_process_response_headers(row,temp_list)

                                temp_list = copy.deepcopy(test_case_response_body)
                                test_case_response_body_dp = dp_process_response_body(row, temp_list)
                                
                                temp_list = copy.deepcopy(test_case_response_assert_body)
                                test_case_response_assert_body_dp = dp_process_assert_response_body(row, temp_list)

                                #---------------- Start Process Extract
                                base_url_extract = extract_process_base_url(base_url_dp)

                                request_body_value_extract = extract_process_request_body(request_body_value_dp,request_body_type)

                                test_case_request_headers_extract = extract_process_request_headers(test_case_request_headers_dp)

                                test_case_response_body_extract = extract_process_response_body(test_case_response_body_dp)
                                
                                test_case_response_assert_body_extract = extract_process_assert_response_body(test_case_response_assert_body_dp)

                                #---------------End Process Extract

                                ###print "YML--------------------------YML"
                                base_url_yaml = yaml_process_url(base_url_extract)

                                request_body_value_yaml = yaml_process_request_body(request_body_value_extract,request_body_type)

                                test_case_request_headers_yaml = yaml_process_request_headers(test_case_request_headers_extract)

                                temp_list = copy.deepcopy(project_defaultHeaders)
                                project_defaultHeaders_dp = yaml_process_request_headers(temp_list)

                                temp_list = copy.deepcopy(api_defaultRequestHeaderList)
                                api_defaultRequestHeaderList_dp = yaml_process_request_headers(temp_list)

                                test_case_response_code_yaml  = yaml_process_response_code(test_case_response_code_dp)

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
                                    post_request(project_name,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name, group,base_url_yaml,final_request_headers,request_body_type, request_body_value_yaml,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,test_case_response_extract_headers,"true",follow_redirects_flag,enable_cookie_flag)
                                if api_request_type == 'get':
                                    if(final_response_code == '302'):
                                        get_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"true",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)
                                    else:
                                        get_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"true",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)
                                if api_request_type == 'put':
                                    put_request(project_name,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name, group,base_url_yaml,final_request_headers,request_body_type, request_body_value_yaml,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,test_case_response_extract_headers,"true",follow_redirects_flag,enable_cookie_flag)
                                if api_request_type == 'delete':
                                    delete_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"true",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)
                                if(afterFlag == 1):
                                    logging.info("execute_apis:executing after")
                                    execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,after,enable_cookie_flag)
                                if(afterTestFlag == 1):
                                    logging.warn("execute_apis:executing after test")
                                    execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,afterTest,enable_cookie_flag)
            else:
                        for tc_index in range(len(test_suite_xml_list[ts_index]['testSuite']['testCase'])):
                                if(beforeTestFlag == 1):
                                    execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,beforeTest,enable_cookie_flag)
                                test_case =  test_suite_xml_list[ts_index]['testSuite']['testCase'][tc_index]
                                test_case_response_body_type = None
                                test_case_response_body_match =None
                                request_body_type = None
                                api_defaultResponse = {}
                                api_defaultHeaders = {}
                                api_defaultHeader = {}
                                api_response_code = 888
                                api_defaultHeadersList  = {}
                                api_defaultRequestHeaderList = {}
                                full_final_request_headers = {}
                                project_defaultHeaders = {}
                                test_case_request = {}
                                test_case_request_headers = {}
                                test_case_request_body  = {}
                                body_flag = 0
                                body_parameters = {}
                                request_body_value ={}
                                body_parameter = {}
                                request_body_value_dp={}
                                request_headers_dp={}
                                response_code_dp=0
                                response_headers_dp={}
                                response_body_dp={}
                                assert_response_body_dp={}
                                test_case_url = ''                                #-------DP
                                temp_list={}
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
                                testcase_name = test_case['@name']
                                group = test_case['@group']
                                api_id = test_case['@apiId']
                                project_id = test_case['@projectId']
                                test_case_request = test_case['request']
                                test_case_id = test_case['@testCaseId']
                                test_case_url = test_case['@extUrl']
                                ###print "#--------------------------"
                                ###print "-----*before and after extraction*---------"
                                try:
                                    before = test_case['@before']
                                    execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,before,enable_cookie_flag)
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring before execution")
                                try:
                                    after = test_case['@after']
                                    afterFlag = 1
                                except KeyError:
                                    logging.warn("execute_apis:after flag is set")

                                ###print "------*Request Headers: Specific to Test Case"
                                try:
                                    test_case_request_headers = test_case_request['headers']['header']
                                    #for header in test_case_request_headers:
                                        ###print header['@name'] + " --> " + header['@value']
                                except KeyError: 
                                    logging.warn("execute_apis:Ignoring test case request headers")
                                try:
                                    follow_redirects_flag = test_case_request['@followRedirects']
                                    ####print "*******", follow_redirects_flag

                                except KeyError:
                                    logging.warn("execute_apis:Ignoring followRedirects")
                                ####print "------*Request Body*------"
                                try:
                                    test_case_request_body = test_case_request['body']
                                    ####print test_case_request_body['@type']
                                    body_flag = 1
                                except KeyError:
                                    ####print ""
                                    logging.warn("execute_apis:Ignoring test case body")
                                    body_flag = 0
                                if(body_flag == 1 and test_case_request_body['@type'] == 'form'):
                                    try:
                                        body_parameters = test_case_request_body['parameter']
                                        #for parameter  in body_parameters:
                                            ####print parameter['@name'] + " -- " + parameter['@type'] + "--" +parameter['@value']
                                        request_body_value = body_parameters
                                        request_body_type = 'form'
                                    except KeyError:
                                        pass
                                        logging.warn("execute_apis:Ignoring request body parameters")
                                if(body_flag == 1 and test_case_request_body['@type'] == 'text'):
                                    try:
                                        body_parameter = test_case_request_body['parameter']
                                        ####print body_parameter['@type']
                                        ####print body_parameter['#text']
                                        request_body_value = body_parameter['#text']
                                        request_body_type = 'text'
                                    except KeyError:
                                        logging.warn("execute_apis:Ignoring request body text")

                                ####print "------*Response Headers: Specific to Test Case*------"
                                try:
                                    test_case_response =  test_case['response']
                                    test_case_response_code = test_case_response['@code']
                                    test_case_response_headers = test_case_response['headers']['header']
                                    #for header in test_case_response_headers:
                                        ####print header['@name'] + " --> " + header['@value']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring test case response headers")
                                try:
                                    ####print "------*Extract Header Values*------"
                                    test_case_response_extract_headers = test_case_response['extractHeader']
                                    #for response_extract_header in test_case_response_extract_headers:
                                        ####print response_extract_header['@name'] + " --> " + response_extract_header['#text']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring test case header extraction")
                                try:
                                    ####print "------*Assert Header Value*------"
                                    test_case_response_assert_headers = test_case_response['assertHeaderValue']
                                    #for test_case_response_assert_header in test_case_response_assert_headers:
                                        ####print test_case_response_assert_header['@name'] + " --> " + test_case_response_assert_header['#text']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring assertHeaderValue")
                                try:
                                    ###print "------*Assert body value*------"
                                    test_case_response_assert_body = test_case_response['assertBodyValue']
                                    #for test_case_response_assert_body_param in test_case_response_assert_body:
                                            ###print "--------------"+test_case_response_assert_body_param['@type'] + " + " + test_case_response_assert_body_param['@method']+ " + " + test_case_response_assert_body_param['@exp']+ " --> " + test_case_response_assert_body_param['#text']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring assertBodyValue")
                                try:
                                    ###print "------*Extract body value*------"
                                    test_case_response_extract_body = test_case_response['extractBody']
                                    #for test_case_response_extract_param in test_case_response_extract_body:
                                            ##print "--------------"+test_case_response_extract_param['@type'] + " + " + test_case_response_extract_param['@method']+ " + " + test_case_response_extract_param['@exp']+ " --> " + test_case_response_extract_param['#text']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring extractBody")
                                try:
                                    ###print "------*Response body value*------"
                                    test_case_response_body = test_case_response['body']['#text']
                                    test_case_response_body_type = test_case_response['body']['@type']
                                    test_case_response_body_match = test_case_response['body']['@match']
                                    ###print test_case_response_body['@type'] + " --> " + test_case_response_body['@match']+ " --> " + test_case_response_body['#text']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring response body")
                                ###print "-================================================-"
                                ###print project_defaultHeaders
                                ###print test_case_request_headers
                                ###print api_defaultHeadersList
                                ###print test_case_response_headers
                                for project_index in range(len(project_info_xml['projectGroup']['project'])):
                                    if(project_info_xml['projectGroup']['project'][project_index]['@id'] == project_id):
                                        project = project_info_xml['projectGroup']['project'][project_index]
                                project_name = project['@name']

                                for api_list_index in range(len(final_api_list)):
                                    temp_api =  final_api_list[api_list_index]
                                    if(temp_api['@id'] == api_id):
                                        project_api = temp_api

                                base_url = project['@serviceType'] + "://" + project['@baseUrl'] + project_api['@requestUrl'] + test_case_url

                                ###print base_url
                                project_name = project['@name']
                                api_name = project_api['@name']
                                api_request_description = project_api['@requestDescription']
                                api_request_type = project_api['@requestType']

                                    ###print "------*Default Header: Specific to API*------"
                                try:
                                    api_defaultResponse = project_api['defaultResponse']
                                    api_defaultHeaders = api_defaultResponse['defaultHeaders']
                                    api_defaultHeader =  api_defaultHeaders['defaultHeader']
                                    api_response_code = project_api['defaultResponse']['@code']
                                    ###print api_response_code
                                    api_defaultHeadersList = project_api['defaultResponse']['defaultHeaders']['defaultHeader']
                                    for default_header in api_defaultHeadersList:
                                        ###print default_header['@name'] + "  -->  " + default_header['@value']
                                        pass
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring response headers Specific to api")
                                    ###print ""
                                    ###print "Ignoring Header Specific to API"

                                try:
                                    api_defaultRequest = project_api['defaultRequest']
                                    api_defaultRequestHeaders = api_defaultRequest['defaultRequestHeaders']
                                    api_defaultRequestHeaderList =  api_defaultRequestHeaders['header']
                                    for default_header in api_defaultRequestHeaderList:
                                        ###print default_header['@name'] + "  -->  " + default_header['@value']
                                        pass
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring api Specific request headers")
                                    ###print ""
                                    ###print "Ignoring Header Specific to API"


                                ###print "------*Default Header: Specific to Project*------"
                                try:
                                    project_defaultHeaders = project['defaultRequestHeaders']['header']
                                    #for header in project_defaultHeaders:
                                        ###print header['@name'] + " --> " +header['@value']
                                except KeyError:
                                    logging.warn("execute_apis:Ignoring project Specific request headers")
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
                                    post_request(project_name,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name, group,base_url_yaml,final_request_headers,request_body_type, request_body_value_yaml,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,test_case_response_extract_headers,"true",follow_redirects_flag,enable_cookie_flag)
                                if api_request_type == 'get':
                                    if(final_response_code == '302'):
                                        get_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"true",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)
                                    else:
                                        get_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"true",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)
                                if api_request_type == 'put':
                                    put_request(project_name,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name, group,base_url_yaml,final_request_headers,request_body_type, request_body_value_yaml,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,test_case_response_extract_headers,"true",follow_redirects_flag,enable_cookie_flag)
                                if api_request_type == 'delete':
                                    delete_request(project_name,test_case_response_extract_headers,test_case_response_extract_body,test_case_response_assert_body_yaml,testcase_name, test_case_id, api_id, test_suite_name,group,base_url_yaml,final_request_headers,final_response_code,final_response_headers,test_case_response_body_yaml,test_case_response_body_type,test_case_response_body_match,"true",follow_redirects_flag,enable_cookie_flag,request_body_type, request_body_value_yaml)
                                
                                #--extract code
                                if(afterFlag == 1):
                                    execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,after,enable_cookie_flag)
                                if(afterTestFlag == 1):
                                    execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,afterTest,enable_cookie_flag)
            logging.info("execute_apis:Executing afterAll")
            if(afterAllFlag == 1):
                execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,afterAll,enable_cookie_flag)
