#!/usr/bin/env python
"""Extract all available inversion examples in the present directory
"""
import importlib.resources
import os
import glob
import zipfile


def main():
    base = os.sep.join((
        str(importlib.resources.files('crtomo_tests')),
        'data',
    ))
    filenames = sorted(glob.glob(base + os.sep + 'example_inversion*'))

    for filename in filenames:
        print(filename)
        zipobj = zipfile.ZipFile(filename)
        targetdir = os.getcwd() + os.sep + os.path.basename(filename)[:-4]
        os.makedirs(targetdir)
        zipobj.extractall(targetdir)
