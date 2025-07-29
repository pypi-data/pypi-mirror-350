from setuptools import setup, find_packages

setup(
    name="reedautomated",
    version="0.1.0",  
     packages=find_packages(include=['reedautomated', 'reedautomated.*']),
      entry_points={
        "console_scripts": [
        "run-reedautoassistant = reedautomated.main:main"
        ]
    },
)
