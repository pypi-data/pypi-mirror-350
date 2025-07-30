from setuptools import setup, find_packages

setup(
    name='am-random-generator',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[],
    author='Ashish',
    author_email='ashishmaurya0408@gmail.com',
    description='A Python package to generate random strings with numbers, characters, or both',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ashish4824/RandomValue',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    keywords='random generator string number character',
)