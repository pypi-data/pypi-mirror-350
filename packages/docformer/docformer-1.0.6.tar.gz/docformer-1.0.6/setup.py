from setuptools import setup

setup(
    name="docformer",
    version="1.0.6",
    packages=["docformer"],
    entry_points={
        "console_scripts": [
            "docformer=docformer.docformer:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A document editor for .docformer and .docform files",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/docformer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 