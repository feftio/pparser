from setuptools import setup, find_packages


with open("README.md", "r") as readme:
    long_description = readme.read()


setup(
    name='pparser',
    version='0.1',
    author="Lik Eduard",
    author_email='feft99@gmail.com',
    description='Package for parsing websites with production',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/feftio/pparser',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
         
    ],
)
