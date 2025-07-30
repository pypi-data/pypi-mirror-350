from setuptools import setup, find_packages

setup(
    name="mkdocs-auto-figure-list",
    version="0.1.3",
    description="auto creation for figures",
    author = "privatacc",
    packages=find_packages(),
    install_requires=[
        "mkdocs"
        ],
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