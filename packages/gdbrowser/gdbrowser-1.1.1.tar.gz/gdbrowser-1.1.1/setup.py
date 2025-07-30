from setuptools import setup, find_packages

setup(
    name="gdbrowser",
    version="1.1.1",
    description="Simple Python API wrapper for GDBrowser",
    author="noxzion",
    author_email="negroid2281488ilikrilex@gmail.com",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.7",
)