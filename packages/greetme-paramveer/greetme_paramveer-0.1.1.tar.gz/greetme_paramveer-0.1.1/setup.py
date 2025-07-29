from setuptools import setup, find_packages

setup(
    name="greetme_paramveer",           # Must be unique on PyPI
    version="0.1.1",
    description="A simple greeting package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Paramveer Singh",
    author_email="paramveer.yaduvanshi@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
