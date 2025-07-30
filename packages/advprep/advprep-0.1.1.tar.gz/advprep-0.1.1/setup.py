from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="advprep",  # Your package name
    version="0.1.1",  # Update version each time you upload
    author="Mukku Sumanth",
    author_email="sumanth8383@gmail.com",
    description="Advanced data imputation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Or your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn"
    ],
)




