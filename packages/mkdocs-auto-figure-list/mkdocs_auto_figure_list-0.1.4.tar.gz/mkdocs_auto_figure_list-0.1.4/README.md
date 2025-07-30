# MkDocs auto figure list

**Note: This plugin is still in an early development phase and may contain some bugs. You are welcome to contribute to its further development.**

This plugin searches through all markdown files for the HTML tags `<figure>` and `<figcaption>`. These are then collected in ascending order, and a new markdown file named `figure-list.md` is created. This file lists all the figures and adds a link to the corresponding image.

This plugin works with the PDF-Exporter Plugin: https://github.com/Privatacc/mkdocs-to-pdf.git

Example of a `<figure>` tag:
```
<figure>
  <img src="path/to/img.jpg" alt="my image">
  <figcaption>My figcaption</figcaption>`
</figure>
```

Installation:
You can install this package with pip:
```
pip install mkdocs-auto-figure-list
```

Use:
The plugin must be added to the `mkdocs.yml` file as follows:
plugins:

Options:
```
    - auto-figure-list:
        heading: "Figure-List"
        figure_label: "Figure"
```
