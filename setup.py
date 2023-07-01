from setuptools import setup, find_packages
from pip._internal.req import parse_requirements

VERSION = '0.1.0'

install_reqs = parse_requirements('requirements.txt', session='install')
reqs = [str(ir.requirement) for ir in install_reqs]

setup(
    name='pychatgpt',
    version=VERSION,
    description='Unofficial ChatGPT Python API using Selenium',
    author='Zhicheng (Jason) Liang',
    author_email='zcjasonliang@gmail.com',
    url='https://github.com/gychant/unofficial-chatgpt-python-api',
    packages=find_packages(),
    install_requires=reqs
)