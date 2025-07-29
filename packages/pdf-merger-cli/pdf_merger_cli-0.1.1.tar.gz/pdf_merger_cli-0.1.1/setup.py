from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pdf-merger-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyPDF2",
        "typer[all]"
    ],
    entry_points={
        "console_scripts": [
            "pdf-merge=pdf_merger_cli.__main__:app",
        ],
    },
    author="Francesco Dell'Ascenza",
    description="A simple CLI tool to merge PDFs using Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
