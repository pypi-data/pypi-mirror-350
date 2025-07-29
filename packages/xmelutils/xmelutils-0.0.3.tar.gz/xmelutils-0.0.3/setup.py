# setup.py
from setuptools import setup, find_packages

setup(
    name="xmelutils",
    version="0.0.3",
    author="Igor Xmelnikov",
    author_email="egorkholkin2018@gmail.com",
    description=(
        "Personal utility functions by Igor Xmelnikov. "
        "Developed for personal use but shared for anyone who might find them helpful. "
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GigaGitCoder/XmelUtils",  
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=[],
    license="MIT",
    keywords="igor xmel utilities string tools",
)