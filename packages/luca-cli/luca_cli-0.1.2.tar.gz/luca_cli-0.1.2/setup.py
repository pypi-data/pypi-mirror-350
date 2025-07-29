from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="luca-cli",
    version="0.1.2",
    author="Hrishi Garud",
    author_email="hrishi.garud@gmail.com",
    description="CLI tool for the Luca assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hgarud/client",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "luca=luca.main:entrypoint",
        ],
    },
    install_requires=[
        "requests",
    ],
) 