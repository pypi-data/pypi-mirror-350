# For help with building, packaging, and uploading to PyPI, visit:
# https://packaging.python.org/en/latest/tutorials/packaging-projects/
# and
# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
#
# TLDR; For just building and uploading, `python -m build` and then `twine upload dist/*` (Get API token from Bitwarden vault)
#

from setuptools import setup
from setuptools.command.install import install
import os
import shutil

# # This dynamic version of getting version isn't working anymore
# def get_version(rel_path):
#     with open(rel_path) as f:
#         exec(f.read())
#     return locals()['__version__']

setup(
    # version=get_version("./apogee_connect_rpi/version.py")
)