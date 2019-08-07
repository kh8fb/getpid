from setuptools import setup

package_name = "getpid"
description = "A script for accessing info about a user's working processes"

with open("README.md","r") as readme:
    long_description = readme.read()

setup(
    name=package_name,
    description=description,
    version='0.1',
    
    maintainer="Kieran Heese",
    maintainer_email="kh8fb@virginia.edu",

    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=[package_name],

    install_requires=[
        "click",
        "psutil",
        "paramiko",

    ],

    entry_points='''
        [console_scripts]
        getpid=getpid:cli
    ''',
    
    python_requires='>=3',
    #classifiers=[
     #   "Programming Language :: Python :: 3",
      #  "License :: OSI Approved :: MIT License",
       # "Operating System :: OS Independent",
    #],
)
    
