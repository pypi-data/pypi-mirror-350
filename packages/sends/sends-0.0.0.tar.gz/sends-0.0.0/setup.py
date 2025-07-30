#!/usr/bin/env python3

from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='sends',
    version='0.0.0',
    license='MIT',
    author='nggit',
    author_email='contact@anggit.com',
    description=(
        'Initial sends package.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nggit/sends',
    packages=['sends'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
)
