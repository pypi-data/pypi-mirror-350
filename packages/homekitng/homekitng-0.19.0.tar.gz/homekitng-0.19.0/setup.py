#
# Copyright 2018 Joachim Lusiardi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='homekitng',
    packages=setuptools.find_packages(exclude=['tests']),
    version='0.19.0',
    description='Python code to interface HomeKit Accessories and Controllers',
    author='Pierre Hugo',
    author_email='pierrekin@househugo.com',
    url='https://github.com/pierrekin/homekit_python',
    download_url='https://example.com/jlusiardi/homekit_python/archive/0.18.0.tar.gz',
    keywords=['HomeKit'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Home Automation',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop'
    ],
    install_requires=[
        'hkdf',
        'PyNaCl',
        'cryptography',
        'tlv8',
    ],
    extras_require={
        'IP': ['zeroconf'],
    },
    license='Apache License 2.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
