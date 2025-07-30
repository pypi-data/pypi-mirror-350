from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

# Load README.md as long description
with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="xor-py",
    version="1.0",
    author="0xsweat",
    author_email="0x.sweat@tutanota.com",
    description="An easy way to use xor in python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0xsweat/xor",
    download_url="https://github.com/0xsweat/xor",
    packages=find_packages(),
    install_requires=[],
    license="MIT",
    keywords=["python", "python xor", "xor", "encryption"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
