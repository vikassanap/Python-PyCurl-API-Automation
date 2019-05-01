from setuptools import setup, find_packages

setup(
    name = 'Oggy',
    version = '1.0',
    description = 'Oggy : Generic Rest API testing Framework',
    author = 'Vikas Sanap',
    url = 'TBD',
    license = 'TBD',
    author_email='vikassanap2011@gmail.com',
    packages = find_packages(),
    package_data={'': ['*.*']},
    entry_points = {'console_scripts': ['oggy = Oggy.oggy:start',],},
    install_requires=["Jinja2==2.7.3","PyYAML==3.10","lxml==3.4.1","pycurl==7.19.0","simplejson==2.3.2","xmltodict==0.9.0"]
)
