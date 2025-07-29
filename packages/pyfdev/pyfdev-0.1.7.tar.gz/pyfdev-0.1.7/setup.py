import io
from setuptools import setup, find_packages

setup(
    name="pyfdev",
    version="0.1.7",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pyfdev = pyfdev.compiler.cli:main",
        ],
    },
    author="Priyanshu Rauth",
    author_email="raut.priyanshu30@gmail.com",
    description="Pyfdev transpiler and CLI",
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords=["pyfdev", "transpiler", "compiler", "cli", "python"],
)
