from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="rhyan-sistema_bancario",
    version="0.0.1",
    author="Rhyan",
    author_email="rhyanaa1211@gmail.com",
    description="Sistema Bancário",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rhyan121121/Sistema-Bancario-Para_Pypi",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)