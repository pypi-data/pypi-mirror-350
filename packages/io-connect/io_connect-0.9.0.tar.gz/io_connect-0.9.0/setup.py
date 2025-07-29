from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="io_connect",
    version="0.9.0",
    author="Faclon-Labs",
    author_email="datascience@faclon.com",
    description="io connect library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "wheel",
        "pandas",
        "numpy",
        "Requests",
        "pytz",
        "python_dateutil",
        "requests",
        "typing_extensions",
        "typeguard",
        "urllib3",
        "pymongo",
        "paho_mqtt==1.6.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
