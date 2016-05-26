from setuptools import find_packages, setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name = 'pylexa',
    version = '0.0.15',
    author = 'Patrick Smith',
    author_email = 'pjs482@gmail.com',
    description = ('A library to ease creation of an Alexa Skills Kit'),
    keywords = 'amazon alexa ask',
    url = 'http://www.github.com/patricksmith/pylexa',
    packages=find_packages(),
    install_requires=[
        'flask', 'python-dateutil', 'pycrypto', 'pyopenssl', 'pyyaml', 'requests'],
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'generate-alexa-conf = pylexa.tools.parse_conf:main',
        ]
    },
)
