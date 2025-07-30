# setup.py
from setuptools import setup, find_packages

setup(
    name="global_cmd",
    version="6.2",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pdf2image",
        "python-dotenv",
        "PyPDF2"
    ],
    entry_points={
        "console_scripts": [
            "global_cmd=global_cmd.global_cmd:main",  
        ],
    },
)
