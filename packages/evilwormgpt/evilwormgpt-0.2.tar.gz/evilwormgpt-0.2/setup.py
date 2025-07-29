
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='evilwormgpt',
    version='0.2',
    packages=find_packages(),
    description='Unofficial wrapper for a sarcastic and evil GPT-style API chatbot',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Hamza',
    author_email='hamza@example.com',
    url='https://github.com/hamza/evilwormgpt',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ],
)
