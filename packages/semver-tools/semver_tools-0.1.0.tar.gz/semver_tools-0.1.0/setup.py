from setuptools import setup, find_packages
import os

setup(
    name="semver-tools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "GitPython",
        "semantic-version",
    ],
    entry_points={
        'console_scripts': [
            'semver-tools=semver_tools.main:cli',
        ],
    },
    author="Daniel Pahima",
    author_email="dpahima98@gmail.com",
    description="A tool for managing semantic versioning in Git repositories",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/dpahima98/semver_tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 