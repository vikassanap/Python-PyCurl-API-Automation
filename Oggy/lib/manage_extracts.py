import os
import yaml
import logging

PATH = os.getcwd()
def store_header(key, value):
    data = {
        key : value
    }
    fname = PATH+"/test_data/temp/headers.yml"
    with open(fname, 'a+') as outfile:
        outfile.write( yaml.dump(data, default_flow_style=False))
    logging.info("manage_extracts:written to yaml file")

def read_header(key):
    fname = PATH+"/test_data/temp/headers.yml"
    with open(fname) as f:
        config = yaml.load(f)
    return config[key]
    logging.info("manage_extracts:read from yaml file")

def update_header(key,value):
    fname = PATH+"/test_data/temp/headers.yml"
    with open(fname) as f:
        config = yaml.load(f)
    config[key] = value
    with open(fname, 'w') as outfile:
        #yaml.dump(config, outfile)
        outfile.write( yaml.dump(config, default_flow_style=False))
    logging.info("manage_extracts:update to yaml file")

def store_body_extract(key, value):
    data = {
        key : value
    }
    fname = PATH+"/test_data/temp/headers.yml"
    with open(fname, 'a+') as outfile:
        outfile.write( yaml.dump(data, default_flow_style=False))
    logging.info("manage_extracts:written body extract to yaml file")

def read_body_extract(key):
    fname = PATH+"/test_data/temp/headers.yml"
    with open(fname) as f:
        config = yaml.load(f)
    return config[key]
    logging.info("manage_extracts:read body extract from yaml file")







