from setuptools import setup, find_packages
import pathlib

# Read the contents of README.md
this_directory = pathlib.Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="hamidreza",
    version="0.4",
    description="Personal information and tools by Hamidreza Moghaddam",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hamidreza Moghaddam",
    author_email="h4midrezam@gmail.com",
    url="https://hamidrezamoghaddam.ir",
    packages=find_packages(include=["hamidreza", "hamidreza.*"]),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
