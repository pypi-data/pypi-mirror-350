from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mkdocs-auto-figure-list",
    version="0.1.4",
    description="Auto creation for figures in MkDocs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="privatacc",
    packages=find_packages(),
    install_requires=["mkdocs"],
    entry_points={
        'mkdocs.plugins': [
            'auto-figure-list = plugin.plugin:FigureListCreation'
        ]
    },
    url="https://github.com/Privatacc/mkdocs-auto-figure-list",
    project_urls={
        "Source": "https://github.com/Privatacc/mkdocs-auto-figure-list",
        "Tracker": "https://github.com/Privatacc/mkdocs-auto-figure-list/issues",
    },
)
