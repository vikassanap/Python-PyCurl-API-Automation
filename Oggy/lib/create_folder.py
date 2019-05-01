import os
import shutil
DIR = os.path.dirname(os.path.realpath(__file__))
PATH = os.getcwd()
import logging

def create_files_folder():
	test_scripts_dir_path = PATH + "/test_scripts"
	test_data_path = PATH + "/test_data"
	
	os.mkdir(test_data_path)
	os.mkdir(test_scripts_dir_path)
	test_scripts_folder_list = ['api','test_suites']
	for folder in test_scripts_folder_list:
		os.mkdir(test_scripts_dir_path + '/' + folder)
	test_data_folder_list = ['assert_files','data_providers','download','mail','upload','yaml','temp']
	for folder in test_data_folder_list:
		os.mkdir(test_data_path+"/"+folder)
	reports_dir_path = PATH+"/reports"
	os.mkdir(PATH+"/reports")
	report_dir_list = ['resources','history_reports']
	for folder in report_dir_list:
		os.mkdir(reports_dir_path+"/"+folder)
	resource = ['details_close.png','jquery.dataTables.min.js','sort_asc.png','details_open.png','jquery.dataTables.css','jquery.js','sort_both.png']
	for res in resource:
		shutil.copy(DIR+"/templates/"+res,reports_dir_path+"/resources/")
	shutil.copy(DIR+"/templates/feature_api.xml",test_scripts_dir_path + '/api')
	shutil.copy(DIR+"/templates/feature_ts.xml",test_scripts_dir_path + '/test_suites')
	shutil.copy(DIR+"/templates/project_info.xml",test_scripts_dir_path)
	shutil.copy(DIR+"/templates/mail_config.yml", test_data_path+"/mail")

