#!/usr/bin/env python
import importlib.resources
import os
import tempfile
import zipfile
import pycrtomo


def main():

    inv_zip_file = str(
        str(importlib.resources.files('crtomo_tests')) +
        os.sep +
        'data' +
        os.sep +
        'example_inversion_01.zip'
    )
    with tempfile.TemporaryDirectory() as tempdir:
        print('tempdir', tempdir)
        zipobj = zipfile.ZipFile(inv_zip_file)
        zipobj.extractall(tempdir)
        basedir = tempdir + os.sep + 'example_inversion_01' + os.sep
        pwd = os.getcwd()
        os.chdir(basedir + 'exe')
        r = pycrtomo.pyinv.invertpy()
        print('Return value', r)
        # now check
        assert os.path.isfile(basedir + os.sep + 'inv' + os.sep + 'inv.ctr'), \
            'inv.ctr was not created'

        os.chdir(pwd)
        print('Press enter to continue')
        input()
