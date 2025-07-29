from setuptools import setup, find_packages

setup(
    name='evilwormgpt',
    version='0.1',
    packages=find_packages(),
    description='مكتبة واجهة API Worm GPT الشريرة',
    author='Hamza',
    author_email='hamza@example.com',
    url='https://github.com/hamza/evilwormgpt',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests'
    ],
)
