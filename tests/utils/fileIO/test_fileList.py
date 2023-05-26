""" 
======================== UNIT TEST FILE LISTING =======================
"""

import reqpy
import os

def test_listdirectory():
    
    try:
        reqpy.utils.fileIO.listdirectory(os.getcwd(),extensions=".py",excluded_folders=("venv",".git"))
    except:
        assert False  