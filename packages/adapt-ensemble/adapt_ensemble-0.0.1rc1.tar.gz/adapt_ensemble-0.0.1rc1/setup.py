from setuptools import setup, find_packages

setup(
    name="adapt-ensemble",
    version="0.0.1rc1",
    author="Ferdinand Koenig",
    author_email="ferdinand@koenix.de",
    description="Placeholder for an adaptive ensemble learning framework.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9,<3.11",
)
