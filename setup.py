import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'pylexa',
    version = '0.0.1',
    author = 'Patrick Smith',
    author_email = 'pjs482@gmail.com',
    description = ('A library to ease creation of an Alexa Skills Kit'),
    keywords = 'amazon alexa ask',
    url = 'http://www.promptworks.com',
    packages=['pylexa'],
    install_requires=['flask'],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
    ],
)
