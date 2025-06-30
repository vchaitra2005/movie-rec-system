from setuptools import setup

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

AUTHOR_NAME = 'CHAITRA V'
SRC_REPO = 'src'
LIST_OF_REQIREMENTS = ['streamlit']

setup(
    name= SRC_REPO,
    version = '0.0.1',
    author = AUTHOR_NAME,
    author_email = 'vchaitra2005@gmail.com',
    description = 'a simple python package to make a simple web app'
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    package = [SRC_REPO],
    python_requires = '>=3.7',
    install_requires = LIST_OF_REQIREMENTS,

)