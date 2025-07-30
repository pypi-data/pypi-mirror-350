from setuptools import setup

setup(
    name="tableausdk",
    version="0.0.2",
    author="cdh@wearehackerone.com",
    author_email="cdh@wearehackerone.com",
    description="Telemetry research package for dependency analysis.",
    long_description="This package is used for research purposes to detect dependency loading.",
    long_description_content_type="text/markdown",
    url="https://github.com/cybercdh",
    packages=["tableausdk"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
