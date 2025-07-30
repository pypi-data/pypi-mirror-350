import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LibGram", 
    version="1.0.2",      
    author="NEFOR",
    author_email="gram@gmail.com",
    description="libraly in create database in gram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/my_gram_library", 
    packages=setuptools.find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
