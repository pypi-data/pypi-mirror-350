from setuptools import setup, find_packages

setup(
    name="festivus",
    version="0.1.0",
    author="Avinash Parab",
    author_email="your_email@example.com",
    description="A simple Indian festival finder package by month, region, religion, and date",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/festivus",
    packages=find_packages(),
    include_package_data=True,
    package_data={'festivus': ['data/*.json']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
