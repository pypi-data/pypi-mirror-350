from setuptools import setup, find_packages

setup(
    name="vplotlib",
    version="0.2",
    packages=find_packages(),
    install_requires=["matplotlib"],
    description="A simple matplotlib wrapper for setting title and labels in one line",
    author="Vishwa shah",
    author_email="vishwashah686@gmail.com",
    license = "MIT",
    include_package_data=True,
    package_data={"": ["LICENSE"]},


)
