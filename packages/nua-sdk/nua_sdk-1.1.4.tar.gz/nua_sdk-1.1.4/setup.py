from setuptools import setup, find_packages

setup(
    name="nua_sdk",
    version="1.1.4",
    packages=find_packages(),
    author="NUA Team",
    author_email="a.baqaleb@nuasecurity.com",
    description="SDK for NUA shared components",
    long_description=open("README.md", "r").read() if open("README.md", "r") else "",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
