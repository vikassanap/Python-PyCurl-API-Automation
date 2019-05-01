#!/usr/bin/python
import logging
import sys, getopt
from lib.parse_xml import *
from lib.execute_apis import *
from lib.send_mail import *
from lib.write_xml import *
import datetime
from lib.report import *
import os
import glob
from lib.save_reports import *
from lib.write_json import *
from lib.create_folder import *
PATH = os.getcwd()
import time
ts = time.time()
import datetime
time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H_%M_%S')
time_stamp = time_stamp.replace(" ","_")
DIR = os.path.dirname(os.path.realpath(__file__))

def start():
 main(sys.argv[1:])

def main(argv):
    group_v = None
    id_v = None
    send_mail_flag = 0
    tag_v = None
    test_suites = None
    test_suite_list = ''
    report_file = ''
    welcome_text="""
      Usage : oggy [Option] [Input]\n
      \tOptions: \t\t\tInput\t\t\tDescription\t\t\t\t\t\n
      \t-v\t--version\t\tNo Input\t\tVersion details\t\t\t\n
      \t-n\t--init\t\t\tNo Input\t\tInit Oggy Framework :)\t\t\t\t\n 
      \t-s\t--suites\t\t(test_suite)+ or all\tExecute by Test Suite Id\t\t\t\n
      \t-i\t--id\t\t\t(test_case_id)+\t\tExecute by Test Case Id\t\t\t\n
      \t-g\t--group\t\t\t(group_name)+\t\tExecute by Test Case Group Name\t\t\n
      \t-t\t--tag\t\t\t(tag_name)+\t\tExecute by Test Case Tag Name\t\t\t\n
      \t-m\t--mail\t\t\tNo Input\t\tExecution report auto emails\t\n
       
      """
    try:
      opts, args = getopt.getopt(argv,"hvnms:i:g:t:",["help","version","init","mail","suites=","id=","group=","tag="])
    except getopt.GetoptError:
      print welcome_text
      sys.exit()
    for opt, arg in opts:
      if opt == '-h' or opt == '--help':
        print welcome_text
        sys.exit()
      elif opt in ("-s", "--suites"):
        if arg == '':
            print welcome_text
            sys.exit()
        test_suites = arg
        #break
      elif opt in ("-v", "--version"):
            print "Oggy Framework version 1.0"
            sys.exit()
      elif opt in ("-i", "--id"):
        if arg == '':
            print welcome_text
            sys.exit()
        id_v = arg
        #break
      elif opt in ("-g", "--group"):
        if arg == '':
            print welcome_text
            sys.exit()
        group_v = arg
        #break
      elif opt in ("-t", "--tag"):
        if arg == '':
            print welcome_text
            sys.exit()
        tag_v = arg
        #break
      elif opt in ("-n", "--init"):
        create_files_folder()
	print "Created required directories !"
        print "Thanks for using Oggy Framework !!!"
        sys.exit()
      elif opt in ("-m", "--mail"):
        send_mail_flag = 1
    if test_suites is None:
      pass
    if id_v is None:
      pass
    if group_v is None:
      pass
    if tag_v is None:
      pass
    filelist = glob.glob(PATH + "/reports/*.log")
    for f in filelist:
      os.remove(f)
    logging.basicConfig(filename=PATH + "/reports/oggy.log", level=logging.INFO)
    logging.info("Program started")
    today_date = datetime.datetime.now().isoformat()
    filelist = glob.glob(PATH + "/reports/*.html")
    for f in filelist:
      os.remove(f)
    logging.info("Removed older reports/result.html file")
    filelist = glob.glob(PATH + "/test_data/temp/*.yml")
    for f in filelist:
      os.remove(f)
    logging.info("Removed older /temp/*.yml file")
    filelist = glob.glob(PATH + "/test_data/temp/*.xml")
    for f in filelist:
      os.remove(f)
    logging.info("Removed older /temp/*.xml file")
    filelist = glob.glob(PATH + "/test_data/temp/*.html")
    for f in filelist:
      os.remove(f)
    logging.info("Removed older /temp/*.html file")
    filelist = glob.glob(PATH + "/test_data/temp/*.json")
    for f in filelist:
      os.remove(f)
    logging.info("Removed older /temp/*.json file")
    filelist = glob.glob(PATH + "/test_data/temp/*.txt")
    for f in filelist:
      os.remove(f)
    logging.info("Removed older /temp/*.txt file")

    project_info_xml = parse_xml(PATH + '/test_scripts/project_info.xml','project_info')
    logging.info("Project_info.xml parsing is completed")
    project_name =  project_info_xml['projectGroup']['project'][0]['@name']

    test_api_xml_list = []
    list_api = glob.glob(PATH + "/test_scripts/api/*.xml")
    for test_api in list_api:
      test_api_xml = parse_xml(test_api,'meta_api')
      test_api_xml_list.append(test_api_xml)
    final_api_list = []
    for dict_index in range(len(test_api_xml_list)):
      for api_index in range(len(test_api_xml_list[dict_index]['apiGroup']['api'])):
        final_api_list.append(test_api_xml_list[dict_index]['apiGroup']['api'][api_index])

    logging.info("Created final API list")
    test_suite_xml_list = []
    list_suites = glob.glob(PATH + "/test_scripts/test_suites/*.xml")
    for test_suite in list_suites:
      test_suite_xml = parse_xml(test_suite,'test_data')
      test_suite_xml_list.append(test_suite_xml)
    logging.info("Created final test suite list")
    if test_suites == None and id_v==None and group_v == None and tag_v == None:
      print welcome_text
      logging.warn("Please enter valid command line parameters")
      sys.exit()
    write_root(time_stamp)
    logging.info("Initialized XML report creation")
    logging.info("Test case execution started at "+time_stamp)
    test_suite_list = []
    tags = ''
    overall_result = []
    if test_suites != None:
      if(test_suites == 'all'):
        logging.info("Executing all test suites")
        result = execute_apis(project_info_xml, final_api_list, test_suite_xml_list, test_suite_list, tags = "", all = 'true')
      else:
        test_suite_list  = test_suites.split(',')
        logging.info("Executing selected test suites")
        execute_apis(project_info_xml, final_api_list, test_suite_xml_list, test_suite_list, tags = "", all = 'false')
    if id_v != None:
      list_ids = id_v.split(',')
      for temp_id in list_ids:
        logging.info("Executing selected test cases by Id")
        execute_api_by_id(project_info_xml,final_api_list,test_suite_xml_list,temp_id,enable_cookie_flag='true')
    if group_v != None:
      list_ids = group_v.split(',')
      logging.info("Executing selected test cases by Group")
      execute_api_by_group(project_info_xml,final_api_list,test_suite_xml_list,list_ids,enable_cookie_flag='true')
    if tag_v != None:
      list_ids = tag_v.split(',')
      logging.info("Executing selected test cases by Tags")
      execute_api_by_tag(project_info_xml,final_api_list,test_suite_xml_list,list_ids,enable_cookie_flag='true')
    write_end()
    logging.info("XML report is generated")
    (json_data,file_name) = write_json(time_stamp)
    logging.info("Created JSON report")
    generate_report(json_data,file_name,time_stamp,send_mail_flag)
    logging.info("Created HTML report")
    save_reports()
    logging.info("Copied reports from temp dir to reports dir")

#if __name__ == '__main__':
 #   main(sys.argv[1:])

