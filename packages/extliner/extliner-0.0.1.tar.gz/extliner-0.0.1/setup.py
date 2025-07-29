from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the list of requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="extliner",
    version="0.0.1",
    author="Deepak Raj",
    author_email="deepak008@live.com",
    description=(
        "A simple command-line tool to count lines in files by extension, "
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codeperfectplus/extliner",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"
    ],
    project_urls={
        "Documentation": "https://extliner.readthedocs.io/en/latest/",
        "Source": "https://github.com/codeperfectplus/extliner",
        "Tracker": "https://github.com/codeperfectplus/extliner/issues"
    },
    entry_points={
        "console_scripts": [
            "extliner=extliner.cli:main",  # Update path if needed
        ],
    },
    keywords=[
        "line count",
        "file analysis",
        "command line tool",
        "file extension",
        "python",
        "CLI",
        "file processing",
        
    ],
    license="MIT",
)