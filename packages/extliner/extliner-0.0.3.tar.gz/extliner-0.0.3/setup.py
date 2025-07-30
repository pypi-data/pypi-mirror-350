from setuptools import setup, find_packages
from fetch_and_bump_version import get_incremented_version
import os

# ---------------------- Package Metadata ---------------------- #

PACKAGE_NAME = "extliner"
AUTHOR = "Deepak Raj"
AUTHOR_EMAIL = "deepak008@live.com"
DESCRIPTION = "A simple command-line tool to count lines in files by extension."
PYTHON_REQUIRES = ">=3.6"
GITHUB_USER = "codeperfectplus"
GITHUB_URL = f"https://github.com/{GITHUB_USER}/{PACKAGE_NAME}"
DOCS_URL = f"https://{PACKAGE_NAME}.readthedocs.io/en/latest/"

# ---------------------- Utility Functions ---------------------- #

def load_file_content(file_path):
    """Read and return the contents of a file if it exists."""
    if os.path.exists(file_path):
        with open(file_path, encoding="utf-8") as f:
            return f.read().strip()
    return ""

def load_requirements(file_path):
    """Parse requirements from a file."""
    content = load_file_content(file_path)
    return content.splitlines() if content else []

# ---------------------- Setup Execution ---------------------- #

setup(
    name=PACKAGE_NAME,
    version=get_incremented_version(PACKAGE_NAME),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=load_file_content("README.md"),
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    packages=find_packages(),
    include_package_data=True,
    install_requires=load_requirements("requirements.txt"),
    python_requires=PYTHON_REQUIRES,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    project_urls={
        "Documentation": DOCS_URL,
        "Source": GITHUB_URL,
        "Tracker": f"{GITHUB_URL}/issues",
    },
    entry_points={
        "console_scripts": [
            f"{PACKAGE_NAME}={PACKAGE_NAME}.cli:main",
        ],
    },
    keywords=[
        "line count", "file analysis", "command line tool",
        "file extension", "python", "CLI", "file processing",
    ],
    license="MIT",
)
