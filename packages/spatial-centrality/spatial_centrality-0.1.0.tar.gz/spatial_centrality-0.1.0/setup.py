from setuptools import setup, find_packages

setup(
    name="spatial_centrality",
    version="0.1.0",
    author="marubekko",
    description="Spatial centrality scores for syntactic dependency trees",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
    install_requires=["networkx"]
)
