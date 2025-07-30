from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="spruce-compiler",
    version="0.1.0",
    author="Spruce Team",
    author_email="sprucecompiler@gmail.com",
    description="A cute placeholder for an eventual compiler",
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Compilers",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        "console_scripts": [
            "spruce=spruce.cli:main",
        ],
    },
) 