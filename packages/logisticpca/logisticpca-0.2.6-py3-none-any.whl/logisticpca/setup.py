from setuptools import setup, find_packages

setup(
    name="logisticpca", 
    version="0.2.6",  
    packages=find_packages(),
    install_requires=[
        "torch",
        "numpy"
    ],
    author="Reda Abouzaid",
    author_email="azaidr00@gmail.com",
    description="A Python implementation of Logistic PCA for binary data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/azaidr/logisticpca",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
