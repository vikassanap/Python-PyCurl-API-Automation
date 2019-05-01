from xml_to_dict import *
import xml.etree.ElementTree as ET
import xmltodict, json
from xml_json import *
from post_request import *
from get_request import *
import logging

def parse_xml(file_name,type_of_input):
    xml_file = open(file_name,'r')
    xml_data = xml_file.read()
    json_value = xml2json(xml_data)
    dict = json.loads(json_value)
    if(type_of_input == "meta_api"):
        project_child = dict['apiGroup']['api']

        try:
            if(type(dict['apiGroup']['api']) is not list):
                temp_list = []
                temp_list.append(dict['apiGroup']['api'])
                dict['apiGroup']['api'] = temp_list
        except KeyError:
                logging.info("There is a single api in api list")

        for api_index in range(len(dict['apiGroup']['api'])):
            try:        
                if type(dict['apiGroup']['api'][api_index]['defaultResponse']['defaultHeaders']['defaultHeader']) is not list:
                    temp_list = []
                    temp_list.append(dict['apiGroup']['api'][api_index]['defaultResponse']['defaultHeaders']['defaultHeader'])
                    dict['apiGroup']['api'][api_index]['defaultResponse']['defaultHeaders']['defaultHeader'] = temp_list
            except KeyError:
                logging.warn("parse_xml:Ignoring absent ['projectGroup']['project'][project_index]['api'][api_index]['defaultResponse']['defaultHeaders']['defaultHeader'] parameter")
            try:    
                if type(dict['apiGroup']['api'][api_index]['defaultRequest']['defaultRequestHeaders']['header']) is not list:
                    temp_list = []
                    temp_list.append(dict['apiGroup']['api'][api_index]['defaultRequest']['defaultRequestHeaders']['header'])
                    dict['apiGroup']['api'][api_index]['defaultRequest']['defaultRequestHeaders']['header'] = temp_list
            except KeyError:
                logging.warn("parse_xml:Ignoring absent ['projectGroup']['project'][project_index]['api'][api_index]['defaultRequest']['defaultHeaders']['Header'] parameter")
        return dict

    if(type_of_input == 'project_info'):
        try:
            if(type(dict['projectGroup']['project']) is not list):
                temp_list = []
                temp_list.append(dict['projectGroup']['project'])
                dict['projectGroup']['project'] = temp_list
        except KeyError:
                logging.warn("parse_xml:Ignoring absent ['projectGroup']['project'] parameter")
        for project_index in range(len(dict['projectGroup']['project'])):
            try:
                if type(dict['projectGroup']['project'][project_index]['defaultRequestHeaders']['header']) is not list:
                    temp_list = []
                    temp_list.append(dict['projectGroup']['project'][project_index]['defaultRequestHeaders']['header'])
                    dict['projectGroup']['project'][project_index]['defaultRequestHeaders']['header'] = temp_list
            except KeyError:
                logging.warn("parse_xml:Ignoring absent ['projectGroup']['project'][project_index]['defaultRequestHeaders']['header'] parameter")
        return dict

    if(type_of_input == "test_data"):
        project_child = dict['testSuite']['testCase']
        if(type(dict['testSuite']['testCase']) is not list):
            temp_list = []
            temp_list.append(dict['testSuite']['testCase'])
            dict['testSuite']['testCase'] = temp_list
        for test_case_index in range(len(dict['testSuite']['testCase'])):
            try:
                pass
                #print test_case_index
                if type(dict['testSuite']['testCase'][test_case_index]['request']['headers']['header']) is not list:
                    temp_list = []
                    temp_list.append(dict['testSuite']['testCase'][test_case_index]['request']['headers']['header'])
                    dict['testSuite']['testCase'][test_case_index]['request']['headers']['header'] = temp_list
                    #print "converted testsuites to list"
            except KeyError:
                pass
                logging.warn("parse_xml:Ignoring absent ['request']['headers']['header'] parameter")

            try:    
                if type(dict['testSuite']['testCase'][test_case_index]['response']['headers']['header']) is not list:
                        temp_list = []
                        temp_list.append(dict['testSuite']['testCase'][test_case_index]['response']['headers']['header'])
                        dict['testSuite']['testCase'][test_case_index]['response']['headers']['header'] = temp_list
            except KeyError:
                logging.warn("parse_xml:Ignoring absent ['response']['headers']['header'] parameter")

            try:
                if type(dict['testSuite']['testCase'][test_case_index]['response']['extractHeader']) is not list:
                        temp_list = []
                        temp_list.append(dict['testSuite']['testCase'][test_case_index]['response']['extractHeader'])
                        dict['testSuite']['testCase'][test_case_index]['response']['extractHeader'] = temp_list
            except KeyError:
                logging.warn("parse_xml:Ignoring absent ['response']['extractHeader'] parameter")
            
            try:
                if type(dict['testSuite']['testCase'][test_case_index]['response']['assertBodyValue']) is not list:
                        temp_list = []
                        temp_list.append(dict['testSuite']['testCase'][test_case_index]['response']['assertBodyValue'])
                        dict['testSuite']['testCase'][test_case_index]['response']['assertBodyValue'] = temp_list
            except KeyError:
                logging.warn("parse_xml:Ignoring absent ['response']['assertBodyValue'] parameter")
            
            try:
                if type(dict['testSuite']['testCase'][test_case_index]['response']['assertHeaderValue']) is not list:
                        temp_list = []
                        temp_list.append(dict['testSuite']['testCase'][test_case_index]['response']['assertHeaderValue'])
                        dict['testSuite']['testCase'][test_case_index]['response']['assertHeaderValue'] = temp_list
            except KeyError:
                logging.warn("parse_xml:Ignoring absent ['response']['assertHeaderValue'] parameter")

            try:
                if type(dict['testSuite']['testCase'][test_case_index]['response']['extractBody']) is not list:
                        temp_list = []
                        temp_list.append(dict['testSuite']['testCase'][test_case_index]['response']['extractBody'])
                        dict['testSuite']['testCase'][test_case_index]['response']['extractBody'] = temp_list
            except KeyError:
                logging.warn("parse_xml:Ignoring absent ['response']['extractBody'] parameter")


            try:    
                no_of_body =  len(dict['testSuite']['testCase'][test_case_index]['request']['body'])
            except KeyError:
                logging.warn("parse_xml:Ignoring absent ['testSuite']['testCase'][test_case_index]['request']['body'] parameter")
                no_of_body = 0;

            if(no_of_body == 0 or type(dict['testSuite']['testCase'][test_case_index]['request']['body']) is not list):
                try:
                    if (dict['testSuite']['testCase'][test_case_index]['request']['body']['@type'] == 'form'):
                            try:
                                if type(dict['testSuite']['testCase'][test_case_index]['request']['body']['parameter']) is not list:
                                    temp_list = []
                                    temp_list.append(dict['testSuite']['testCase'][test_case_index]['request']['body']['parameter'])
                                    dict['testSuite']['testCase'][test_case_index]['request']['body']['parameter'] = temp_list
                            except KeyError:
                                logging.warn("parse_xml:Ignoring absent ['testSuite']['testCase'][test_case_index]['request']['body']['parameter'] parameter")
                except KeyError:
                                logging.warn("parse_xml:Ignoring absent ['testSuite']['testCase'][test_case_index]['request']['body'] parameter")    
            else:
                logging.error("parse_xml:Request should have single body node")

        return dict



    
    



