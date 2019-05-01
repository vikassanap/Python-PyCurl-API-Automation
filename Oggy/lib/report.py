import os
from jinja2 import Environment, FileSystemLoader
from send_mail import *
DIR = os.path.dirname(os.path.realpath(__file__))
import logging
PATH = os.getcwd()
import json
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(DIR+'/templates/'),
    trim_blocks=False)
 
 
def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)
 
 
def create_index_html(total_count, total_pass, total_fail, pass_percentage, today_date,project_name,file_name):
    fname = PATH+"/test_data/temp/result_"+today_date+".html"
    context = {
        'file_path':file_name,
        'total_pass': total_pass,
        'total_fail': total_fail,
        'total_count': total_count,
        'pass_percentage': pass_percentage,
        'today_date': today_date.replace("_",":"),
        'project_name': project_name
    }
    #
    with open(fname, 'w') as f:
        html = render_template('index.html', context)
        f.write(html)
    return fname
 
def create_summary_html(total_count, total_pass, total_fail, pass_percentage, today_date,project_name,json_data):
    fname = PATH+"/test_data/temp/summary_"+today_date+".html"
    base_string = """
    <html>
    <head><title> """+project_name+ """ API Functionality Testing Report </title></head>
    <body>
    <table><tr><td>
    Project Name : """+project_name+"""</td></tr><tr><td>
    Exection Timestamp : """+today_date.replace("_",":")+"""</td></tr></table>
    <table style="border-collapse: collapse;border: 1px solid black;">
    <tr><th style="border-collapse: collapse;border: 1px solid black;"> Total # TCs </th><th style="border-collapse: collapse;border: 1px solid black;"> Total Pass </th><th style="border-collapse: collapse;border: 1px solid black;"> Total Failures </th><th style="border-collapse: collapse;border: 1px solid black;"> Passed % </th> </tr><tr>
    <td style="border-collapse: collapse;border: 1px solid black;">"""+str(total_count)+"""</td><td style="border-collapse: collapse;border: 1px solid black;">"""+str(total_pass)+"""</td><td style="border-collapse: collapse;border: 1px solid black;">"""+str(total_fail)+"""</td><td style="border-collapse: collapse;border: 1px solid black;">"""+str(pass_percentage)+"""</td>
    </table>
    </br>
    <hr>
    </br>
    Summary Report:
    </br>
    </br>
    <table style="border-collapse: collapse;border: 1px solid black;">
    <tr><th style="border-collapse: collapse;border: 1px solid black;">ID</th><th style="border-collapse: collapse;border: 1px solid black;">Summary</th><th style="border-collapse: collapse;border: 1px solid black;">API</th><th>Header Match Result</th><th style="border-collapse: collapse;border: 1px solid black;">Body Match Result</th><th style="border-collapse: collapse;border: 1px solid black;">Code Match Result</th><th style="border-collapse: collapse;border: 1px solid black;">Overall Result</th><th style="border-collapse: collapse;border: 1px solid black;">Reason of Failure</th></tr>
    """
    body_string = ""
    for test_case in json_data['data']:
        body_string = body_string + """
        <tr><td style="border-collapse: collapse;border: 1px solid black;">"""+str(test_case['@id'])+"""</td><td style="border-collapse: collapse;border: 1px solid black;">"""+str(test_case['@n'])+"""</td><td style="border-collapse: collapse;border: 1px solid black;">
        """+str(test_case['@api'])+"""</td><td style="border-collapse: collapse;border: 1px solid black;">"""+str(test_case['@hr'])+"""</td><td style="border-collapse: collapse;border: 1px solid black;">
        """+str(test_case['@br'])+"""</td><td style="border-collapse: collapse;border: 1px solid black;">"""+str(test_case['@cr'])+"""</td><td style="border-collapse: collapse;border: 1px solid black;">
        """+str(test_case['@o'])+"""</td><td style="border-collapse: collapse;border: 1px solid black;">"""+str(test_case['reason'])+"""</td>
        """
    body_end_string = """
    </table>
    """
    final_string = base_string + body_string + body_end_string
    send_mail(final_string,project_name)

def generate_report(json_data,file_name,time_stamp,mail_flag):
    logging.info("report:HTML Report Generation started")
    json_data = json.loads(json_data)
    total_pass = 0
    project_name = json_data['data'][0]['@project']
    total_count = len(json_data['data'])
    for test_case in json_data['data']:
        if test_case['@o'] == 'pass':
            total_pass = total_pass +1
    total_fail = total_count - total_pass
    pass_percentage = total_pass*100/total_count
    full_report_fname = create_index_html(total_count, total_pass, total_fail, pass_percentage,time_stamp, project_name,file_name)
    logging.info("report:HTML report generation completed")
    if mail_flag == 1:
        logging.info("report:creating summary report for email")
        create_summary_html(total_count, total_pass, total_fail, pass_percentage,time_stamp, project_name,json_data)
        logging.info("report:created summary report for email")
    return (full_report_fname)



 
 
