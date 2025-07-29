import os
print("Current working directory:", os.getcwd())
print("Files in this directory:", os.listdir())


from setuptools import setup, find_packages
from pathlib import Path

# Always resolve paths relative to the location of setup.py
here = Path(__file__).resolve().parent
requirements_path = here / "requirements.txt"
readme_path = here / "README.md"

# Defensive: Check if files exist
if not requirements_path.exists():
    raise FileNotFoundError(f"{requirements_path} does not exist")
if not readme_path.exists():
    raise FileNotFoundError(f"{readme_path} does not exist")

requirements = requirements_path.read_text().splitlines()
long_description = readme_path.read_text()

setup(
    name="Wilson_Beta_wrapper",
    version="0.1.2",
    author="Koushik Kamalahasan",
    author_email="koushikkamalahasan@gmail.com",
    description="A wrapper to modify beta functions in the Wilson SMEFT package.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
