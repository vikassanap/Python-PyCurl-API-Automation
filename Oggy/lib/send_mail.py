import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import yaml
import logging

def send_mail(body, project_name):
	path =  os.getcwd()
	config_path = path+"/test_data/mail/mail_config.yml"
	logging.info("Reading from "+ config_path)
	with open(config_path, 'r') as f:
  		config = yaml.load(f)
	msg = MIMEMultipart()
	msg['Subject'] = project_name + " : API Functionality Testing Report"
	msg['From'] = config['from_email']
	msg['To'] = config['to_list']
	text = MIMEText(body,'html')
	msg.attach(text)
	s = smtplib.SMTP("smtp.gmail.com", 587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(config['from_email'], config['from_password'])
	logging.info("Mail authentication is done")
	s.sendmail(config['from_email'], config['to_list'], msg.as_string())
	logging.info("Mail is sent")
	s.quit()