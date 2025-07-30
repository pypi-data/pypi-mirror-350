import sys
from setuptools import setup, find_packages

with open('requirements.txt') as reqs:
    install_requires = [
        line for line in reqs.read().split('\n')
        if (line and not line.startswith('--')) and (";" not in line)
    ]
if sys.version_info[:2] < (3, 5):
    install_requires.append("configparser>=3.7.4")

with open(".metwork-framework/README.md") as f:
    long_description = f.read()

setup(
    author="Fabien MARTY",
    author_email="fabien.marty@gmail.com",
    name="opinionated_configparser",
    version="1.0.2",
    license="MIT",
    python_requires='>=2.7',
    url="https://github.com/metwork-framework/opinionated_configparser",
    description="opinionated python configparser library override to deal "
    "with configuration variants (PROD, DEV...) and jija2 interpolation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="configparser extension",
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ]
)
