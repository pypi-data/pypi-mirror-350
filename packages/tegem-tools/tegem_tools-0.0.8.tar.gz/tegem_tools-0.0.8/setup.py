from setuptools import setup, find_packages
from os import path

work_dir = path.abspath(path.dirname(__file__))

with open(path.join(work_dir, 'README.md'), encoding="utf-8") as f:
	long_description = f.read()


setup(
	name="tegem_tools",
	version="0.0.8",
	#url="https://github.com/alexmais95/tegem-tools.git",
	author="alexmais95",
	author_email="alexlove9596@gmail.com",
	description="package for tegem project",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=find_packages(),
	install_requires=[
		'aiohttp==3.10.5', 
		'beautifulsoup4==4.12.3', 
		'feedparser==6.0.11', 
		'lxml==5.3.0', 
		'playwright==1.47.0', 
		'requests==2.32.2',
		'requests-ip-rotator==1.0.14',
		'deep-translator==1.11.4',
		'sentry-sdk==2.19.0',
		'colorama==0.4.6',
		'fake_useragent==2.2.0'],
) 

