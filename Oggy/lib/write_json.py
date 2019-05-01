from xml_to_dict import *
import xml.etree.ElementTree as ET
import xmltodict, json
from xml_json import *
import os
import glob
import logging

PATH = os.getcwd()

def write_json(time_stamp):
    logging.info("write_json:started writing json")
    xml_file = open(PATH+"/test_data/temp/result_"+time_stamp+".xml",'r')
    xml_data = xml_file.read()
    json_value = xml2json(xml_data)
    #json_value = json.loads(json_value)
    #json_value = json_value['result']
    temp = json_value.lstrip("{\"result\":");
    temp = temp[:-1]
    if ("{\"data\": {" in temp):
        temp = temp.replace("{\"data\": {","{\"data\": [{")
        temp = temp.replace("}}","}]}")
    fname = PATH+"/test_data/temp/result_"+time_stamp+".json"
    with open(fname, 'a+') as outfile:
        outfile.write(temp)
    return (temp,"result_"+time_stamp+".json")
    logging.info("write_json:ended writing json")

