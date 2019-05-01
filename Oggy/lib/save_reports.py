import shutil
import os
PATH = os.getcwd()
from os import path
import glob
import logging
DIR = os.path.dirname(os.path.realpath(__file__))

def save_reports():
	reports_dir = PATH+"/reports"
	history_reports_dir = PATH+"/reports/history_reports"
	temp_dir = PATH+"/test_data/temp"
	files = glob.glob(reports_dir+"/*.html")
	print files
	for file_name in files:
		try:
			shutil.move(file_name,history_reports_dir)
		except IOError:
			logging.error("save_reports:Can't move old reports to history_reports_dir")

	files = glob.glob(reports_dir+"/*.xml")
	for file_name in files:
		try:
			shutil.move(file_name,history_reports_dir)
		except IOError:
			logging.error("save_reports:Can't move old reports to history_reports_dir")

	files = glob.glob(reports_dir+"/*.json")
	for file_name in files:
		try:
			shutil.move(file_name,history_reports_dir)
		except IOError:
			logging.error("save_reports:Can't move old reports to history_reports_dir")
			
	files = glob.glob(temp_dir+"/*.xml")
	for file_name in files:
		try:
			shutil.move(file_name,reports_dir)
		except IOError:
			logging.error("save_reports:Can't move new xml report to reports_dir")

	files = glob.glob(temp_dir+"/*.json")
	for file_name in files:
		try:
			shutil.move(file_name,reports_dir)
		except IOError:
			logging.error("save_reports:Can't move new json report to reports_dir")

	files = glob.glob(temp_dir+"/*.html")
	for file_name in files:
		try:
			shutil.move(file_name,reports_dir)
		except IOError:
			logging.error("save_reports:Can't move new html report to reports_dir")
