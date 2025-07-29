from setuptools import setup, find_packages

setup(
    name="stringshift",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "stringshift = stringshift.cli:main"
        ]
    },
)
