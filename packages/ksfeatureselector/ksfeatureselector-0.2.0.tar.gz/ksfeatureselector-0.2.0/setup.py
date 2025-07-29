from setuptools import setup, find_packages

setup(
    name='ksfeatureselector',
    version='0.2.0',
    description='A robust and flexible Python package designed for selecting the most discriminatory features in both **binary and multi-class classification problems** using the Kolmogorov-Smirnov (K-S) test. It provides advanced options for handling multi-class scenarios and aggregating p-values.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    author='V Subrahmanya Raghu Ram Kishore Parupudi',
    author_email='pvsrrkishore@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
