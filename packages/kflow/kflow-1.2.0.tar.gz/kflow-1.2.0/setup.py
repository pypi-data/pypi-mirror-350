"""This module does blah blah."""
import os
from setuptools import setup

version = None
github_run_number = os.getenv("GITHUB_RUN_NUMBER")
if github_run_number is not None:
    version = f"1.2.{github_run_number}"

setup(name='kflow',
    version=version if version != None else "1.2.0",
    description='KLog.co package for ETLs with performance optimizations',
    long_description='High-performance functions to extract, transform, and load data from various sources. Features optimized chunked processing, connection pooling, and performance monitoring for data engineering pipelines.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='etl data science airflow redshift connection pooling',
    url='https://github.com/teu-ai/etl',
    author='KLog.co Data & BI',
    author_email='data@klog.co',
    license='Apache',
    license_files = ('LICENSE.txt',),
    packages=['kflow'],
    include_package_data=True,
    install_requires=[
        'sqlalchemy',
        'pandas',
        'psycopg2-binary',
        'boto3',
        'smart_open',
        'jinjasql',
        'fastparquet',
        'pyarrow'
    ]
)
