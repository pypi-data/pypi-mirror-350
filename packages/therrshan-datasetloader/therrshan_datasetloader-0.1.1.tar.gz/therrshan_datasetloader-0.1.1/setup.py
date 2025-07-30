from setuptools import setup, find_packages

setup(
    name="therrshan-datasetloader",
    version="0.1.1",
    packages=find_packages(),
    description="Local loader for MNIST, Fashion MNIST, and 20 Newsgroups datasets",
    author="Darshan Rajopadhye",
    license="MIT",
    install_requires=[
        "numpy",
        "pandas"
    ],
)
