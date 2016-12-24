import os
from setuptools import setup, find_packages

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='jellyfish',
    version="0.1.3",
    description='simple file encryption using pycryptodome',
    long_description=readme,
    author='Wannaphong',
    author_email='wannaphong@yahoo.com',
    url='http://github.com/wannaphongcom/jellyfish/',
    py_modules=['beefish'],
    install_requires=['pycryptodome','six'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python 3',
    ],
    scripts = ['beefish.py'],
)
