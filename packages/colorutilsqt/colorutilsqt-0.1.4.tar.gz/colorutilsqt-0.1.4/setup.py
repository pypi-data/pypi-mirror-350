from setuptools import setup, find_packages

setup(
    name='colorutilsqt',
    version='0.1.4',
    author='Quinten Teusink',
    description='A simple library to convert and print colors in terminal',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Quinosaur/pycolortools', 
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
