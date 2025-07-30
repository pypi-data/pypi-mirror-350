import setuptools
from pathlib import Path


setuptools.setup(
    name="aliPdfConverter",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)


# pypi-AgEIcHlwaS5vcmcCJGFiYWZjYzZiLTc3MGEtNGEwNi1iMGFlLTc5YWRkZWQ5YjhhMQACKlszLCIxNzRmYzQ4Yi1jZmNiLTQ2MzAtOTAwYy1iMTE0MDIxMDAyMGUiXQAABiBURVqgnbCKPYwSiQTMvGK1jdYSpgp87CeD38wzRe0D-A
