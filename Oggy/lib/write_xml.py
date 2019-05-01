import os
import yaml
import re
import logging

PATH = os.getcwd()
time_stamp = ''
def encodeXMLText(text):
    text = text.replace("&", "&amp;")
    text = text.replace("\"", "&quot;")
    text = text.replace("'", "&apos;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def write_result(project_name,testcase_name, testcase_id, api, suite,group, request_type, url, request_h, request_b, eresponse_c, eresponse_h, eresponse_b, response_c, response_h, response_b, header, body, code, overall,primary_request,assert_body_result,reason,extraction_details,extract_body_result):
    request_h = ','.join(request_h)
    eresponse_b = str(eresponse_b)
    eresponse_c = str(eresponse_c)
    eresponse_h = ','.join(eresponse_h)
    response_c = str(response_c)
    response_h = ",".join(["%s=%s" % (k, v) for k, v in response_h.items()])
    temp = re.sub('<[^<]+?>', '', response_b)
    temp = re.sub('\n',' ',temp)
    temp = re.sub('\t',' ',temp)
    temp = re.sub(' +',' ',temp)

    temp1 = re.sub('<[^<]+?>', '', reason)
    temp1 = re.sub('\n',' ',temp1)
    temp1 = re.sub('\t',' ',temp1)
    temp1 = re.sub(' +',' ',temp1)
    
    xml_string = """
    <data id ='"""+testcase_id+"""' project ='""" +project_name+"""' n ='""" +testcase_name+ """' api = '"""+api+"""' ts='"""+suite+"""' g = '"""+group+"""' type='"""+request_type+"""' hr = '"""+header+"""' br = '"""+body+"""' cr = '"""+code+"""' ab = '"""+assert_body_result+"""' o ='"""+overall+"""' parentRequest = '"""+primary_request+"""'>
    <rh>"""+encodeXMLText(request_h)+"""</rh>
    <rb>"""+encodeXMLText(request_b)+"""</rb>
    <url>"""+encodeXMLText(url)+"""</url>
    <erh>"""+encodeXMLText(eresponse_h)+"""</erh>
    <erb>"""+encodeXMLText(eresponse_b)+"""</erb>
    <erc>"""+encodeXMLText(eresponse_c)+"""</erc>
    <resheaders>"""+encodeXMLText(response_h)+"""</resheaders>
    <resbody>"""+encodeXMLText(temp)+"""</resbody>
    <rescode>"""+encodeXMLText(response_c)+"""</rescode>
    <reason>"""+encodeXMLText(temp1)+"""</reason>
    <extractbodyresult>"""+encodeXMLText(extract_body_result)+"""</extractbodyresult>
    <extractheaderresult>"""+encodeXMLText(extraction_details)+"""</extractheaderresult>
    </data>
    """

    fname = PATH+"/test_data/temp/result_"+time_stamp+".xml"
    with open(fname, 'a+') as outfile:
        outfile.write(xml_string)

def write_root(time_value):
    global time_stamp
    time_stamp = time_value
    root_xml = """
    <result>
    """
    fname = PATH+"/test_data/temp/result_"+time_stamp+".xml"
    with open(fname, 'a+') as outfile:
        outfile.seek(0)
        outfile.write(root_xml)

def write_end():
    root_xml = """
    </result>
    """
    fname = PATH+"/test_data/temp/result_"+time_stamp+".xml"
    with open(fname, 'a+') as outfile:
        outfile.write(root_xml)
    #print "See Result at "+ fname
