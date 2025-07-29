from setuptools import setup, find_packages
import os

def read_requirements(filename):
    try:
        with open(filename) as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        # Fallback to hardcoded requirements if requirements.txt is not found
        return [
            "click==7.1.2",
            "numpy>=1.22.4",
            "pandas==2.2.0",
            "python-dateutil>=2.8.2",
            "pytz>=2020.5",
            "six>=1.15.0"
        ]

setup(
    name="jae-csv-linter",
    version="0.0.1",
    description="demo python CLI tool to lint csv files",
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
    entry_points={
        "console_scripts": [
            "csv-linter=csv_linter.main:main"
        ]
    },
    python_requires=">=3.8",
)
