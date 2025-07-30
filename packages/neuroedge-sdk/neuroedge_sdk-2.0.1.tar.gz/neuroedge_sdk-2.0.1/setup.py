from setuptools import setup, find_packages
setup(
    name='neuroedge_sdk',
    version='2.0.1',
    packages=find_packages(),
    description='This module enables logging of parameters, metrics, and artifacts to MLflow using the Tracking Log Model SDK. It also provides functionality to persist models to Amazon S3 based on specific message types.',
    author='Saurav Kumar',
    author_email='Saurav.Kumar@cognizant.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)