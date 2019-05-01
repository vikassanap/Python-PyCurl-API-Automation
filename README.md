# PythonPyCurlAPIAutomation
- Oggy the Python based API automation framework, XML based, non coding approach to automate APIs
- This framework allows you to automate and execute API test cases without writing single line of code.

## Requirements
- Python 2.7+

## Features
- Specify your test cases in XML files
- Automate more than one project APIs
- HTML report, log generation
- Generates automation template using simple command line option
- In built report mailing mechanism

## How to use it?
1. Clone this repo using `git clone` command
2. Run `build.sh` file, this will generate `.egg` file in `dist/` directory and will install it with required dependencies
3. From terminal execute `oggy` command
4. Follow command line options to setup automation framework and start automating your test cases
```
Usage : oggy [Option] [Input]
      Options       Input                   Description
      --version     No Input                Version details
      --init        No Input                Init Oggy Framework
      --suites      (test_suite)+ or all    Execute by Test Suite Id
      --id          (test_case_id)+         Execute by Test Case Id
      --group       (group_name)+           Execute by Test Case Group Name
      --tag        (tag_name)+              Execute by Test Case Tag Name
      -m --mail     No Input                Execution report auto emails
```
6. Execute `oggy --init` to create automation framework template
7. Edit configuration files and get started

## oggy --init
This will create a framework folder structure with below directories
- `reports` directory: will contain test case execution `.html` report with `.log file`; it will also save historical reports in this directory for future references
- `test_data` directory: `assert_files` will contain files which you want to match directly e.g. download file match; `mail` directory allows you to specify report emailing SMTP details; `temp` is used by framework to store temp files while execution; `upload` to put upload test files; `yaml` test data variable values will be specified here
- `test_scripts` directory: `project_info.xml` to specify project information; `api` contains API metadata information; `test_suites` contains test cases grouped under different files

## Sample files
### project_info.xml
```xml
<?xml version="1.0"?>
<projectGroup>
	<project id = 'Project_id' serviceType = 'http/http' baseUrl = 'host:port' name = 'Application_name'>
		<defaultRequestHeaders>
			<header name='header1' value = 'value'/>
			<header name='headerN' value = 'value'/>
		</defaultRequestHeaders>
	</project>
</projectGroup>
```
### testSuiteName_api.xml
```xml
<apiGroup>
	<api id = 'api_id_1' name = 'api_name' requestUrl = 'request-url' requestType = 'get/post/delete/put' requestName = 'request name' requestDescription = 'API description' projectId = 'project_id'>
		<defaultRequest>
			<defaultRequestHeaders>
				<header name='header1' value = 'default_value'/>
				<header name='header2' value = 'default_value'/>
			</defaultRequestHeaders>
		</defaultRequest>
		<defaultResponse code = '200/302/400/500'>
			<defaultHeaders>
				<defaultHeader name='header1' value = 'default_value'/>
				<defaultHeader name='header1' value = 'default_value'/>
			</defaultHeaders>
		</defaultResponse>
	</api>
</apiGroup>
```

### testSuiteName_ts.xml
```xml
<apiGroup>
	<api id = 'api_id_1' name = 'api_name' requestUrl = 'request-url' requestType = 'get/post/delete/put' requestName = 'request name' requestDescription = 'API description' projectId = 'project_id'>
		<defaultRequest>
			<defaultRequestHeaders>
				<header name='header1' value = 'default_value'/>
				<header name='header2' value = 'default_value'/>
			</defaultRequestHeaders>
		</defaultRequest>
		<defaultResponse code = '200/302/400/500'>
			<defaultHeaders>
				<defaultHeader name='header1' value = 'default_value'/>
				<defaultHeader name='header1' value = 'default_value'/>
			</defaultHeaders>
		</defaultResponse>
	</api>
</apiGroup>
```

### mail_config.yml
```yml
to_list: mail1@gmail.com,mail2@gmail.com
from_email: sender@gmail.com
from_password: password
```

## Author
[Vikas Sanap](https://www.linkedin.com/in/vikassanap/)
