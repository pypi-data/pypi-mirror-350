from setuptools import setup, find_packages

setup(
    name="sunra-apispec",
    version="0.0.1-dev26",
    author="sunra.ai",
    author_email="admin@sunra.ai",
    description="A toolkit for managing and generating API specifications for various AI services",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sunra-ai/APISpecToolkit",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={
        "sunra_apispec": ["*.json", "*.yaml"],
    },
    install_requires=[
        "pydantic",
        "fastapi",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
