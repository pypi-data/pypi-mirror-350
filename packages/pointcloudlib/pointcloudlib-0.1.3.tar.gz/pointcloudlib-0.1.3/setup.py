from setuptools import setup, find_packages

setup(
    name="pointcloudlib",
    version="0.1.3",
    packages=find_packages(),
    description="Python library for image processing, focused on 3D environment modeling. This project is part of the final graduation project at the Costa Rica Institute of Technology.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Yordi Brenes Roda",
    author_email="ybrenesr@estudiantec.cr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[],
)
