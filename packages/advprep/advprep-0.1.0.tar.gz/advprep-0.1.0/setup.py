# setup.py

from setuptools import setup, find_packages

setup(
    name='advprep',
    version='0.1.0',
    description='Advanced data preprocessing for ML and DL pipelines',
    author='Mukku Sumanth',
    author_email='sumanth8383@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn'
    ],
    python_requires='>=3.7',
)




