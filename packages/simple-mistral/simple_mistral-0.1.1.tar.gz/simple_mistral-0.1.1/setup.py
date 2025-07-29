from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="simple-mistral",
    version="0.1.1",
    packages=find_packages(),
    author="Alexander Balashov",
    author_email="alaex777@gmail.com",
    description="A simple async and sync Mistral API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alaex777/simple-mistral",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
