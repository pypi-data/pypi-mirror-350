from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name='async_elastic_logger',
    version='0.4.5.1.4',
    packages=find_packages(),
    install_requires=[
        'pydantic==2.9.2',
        'pydantic-settings==2.6.1',
        'elasticsearch[async]==8.16.0'
    ],
    author='Nima Miri',
    author_email='nimamiri9248@gmail.com',
    description='A custom asynchronous logging library with Elasticsearch integration.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nimamiri9248/async_elastic_logger',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging'
    ],
)
