from setuptools import setup, find_packages

setup(
    name="reedautomated",
    version="0.3.0",  
     packages=find_packages(include=['reedautomated', 'reedautomated.*']),
     install_requires=[
        "selenium",
        "schedule"
    ],
      entry_points={
        "console_scripts": [
        "run-reedautoassistant = reedautomated.main:run_as_script"
        ]
    },
)
