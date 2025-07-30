from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="anbima-data",
    version="0.1.0",
    author="Aliane Vieira de Castro",
    author_email="seu@email.com",
    description="Provides Python functions to retrieve public data from ANBIMA related to the Brazilian fixed income market",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlianeVdeC/anbima-data",
    packages=find_packages(),  
    include_package_data=True,
    install_requires=[
        "pandas",
        "requests",
        "beautifulsoup4",
        "plotly"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

