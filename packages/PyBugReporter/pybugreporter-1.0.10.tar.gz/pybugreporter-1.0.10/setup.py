import setuptools
import os

from PyBugReporter._version import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    longDescription = fh.read()

requirements = ""
with open("PyBugReporter/requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

requirements = requirements.split("\n")

def listFolders(directory: str) -> list[str]:
    """Lists all folders in a directory and its subdirectories.

    Args:
        directory (str): the directory to search

    Returns:
        list[str]: the list of folders in the directory and its subdirectories
    """
    folders = []
    for item in os.listdir(directory):
        itemPath = os.path.join(directory, item)
        if os.path.isdir(itemPath) and item != "__pycache__":
            folders.append(itemPath)
    otherFolders = [listFolders(itemPath) for itemPath in folders]
    for folder in otherFolders:
        folders.extend(folder)
    return folders

folderPath = "PyBugReporter"
folders = listFolders(folderPath)
folders.append("PyBugReporter")
print(folders)

setuptools.setup(
    name='PyBugReporter',
    version=__version__,
    author='Record Linking Lab',
    author_email='recordlinkinglab@gmail.com',
    description='A python library for catching thrown exceptions and automatically creating issues on a GitHub repo.',
    long_description=longDescription,
    long_description_content_type="text/markdown",
    url='https://github.com/byuawsfhtl/PyBugReporter.git',
    project_urls = {
        "Bug Tracker": "https://github.com/byuawsfhtl/PyBugReporter/issues"
    },
    packages=folders,
    install_requires=requirements,
    package_data={"": ["*.json", "*.txt"]},
)
