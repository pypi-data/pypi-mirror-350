import requests
from setuptools import setup, find_packages


def get_incremented_version(package_name: str):
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        latest_version = data['info']['version']
        version_parts = latest_version.split('.')
        
        # Convert last part to int and increment
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        
        incremented_version = '.'.join(version_parts)
        return incremented_version
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch version for package '{package_name}': {e}")
    except Exception as e:
        print(f"Error processing version: {e}")

# Read the long description from README.md
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = (
        "A simple command-line tool to count lines in files by extension. "
        "See the documentation for more details."
    )

# Read the list of requirements from requirements.txt
try:
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = fh.read().splitlines()
except FileNotFoundError:
    requirements = ["tabulate==0.9.0"]

__package__ = "extliner"
__version__ = get_incremented_version(__package__)
__author__ = "Deepak Raj"
__author_email__ = "deepak008@live.com"
__description__ = "A simple command-line tool to count lines in files by extension."
__github_url__ = f"https://github.com/codeperfectplus/{__package__}"
__python_requires__ = ">=3.6"

setup(
    name=__package__,
    version=get_incremented_version(__package__),
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=__github_url__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires=__python_requires__,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"
    ],
    project_urls={
        "Documentation": f"https://{__package__}.readthedocs.io/en/latest/",
        "Source": __github_url__,
        "Tracker": f"{__github_url__}/issues",
    },
    entry_points={
        "console_scripts": [
            "extliner=extliner.cli:main",
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