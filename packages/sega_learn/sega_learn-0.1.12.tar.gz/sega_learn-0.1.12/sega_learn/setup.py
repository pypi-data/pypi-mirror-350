# from setuptools import setup
# from Cython.Build import cythonize
# import numpy as np

# setup(
#     ext_modules=cythonize("sega_learn/linear_models/linear_models_cython.pyx"),
#     include_dirs=[np.get_include()]
# )

# Automatically finds all cython files in the project and builds them
import os

import numpy as np
from Cython.Build import cythonize
from setuptools import setup


def find_pyx_files(root_dir):
    """Find all .pyx files in the given directory and its subdirectories."""
    pyx_files = []
    for dirpath, _dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".pyx"):
                pyx_files.append(os.path.join(dirpath, filename))
    return pyx_files


extensions = cythonize(find_pyx_files("sega_learn/"))

setup(ext_modules=extensions, include_dirs=[np.get_include()])

# To build the cython code, run the following command in the terminal:
# The inplace flag is used to build the extension in the same directory as the source code.
# python setup.py build_ext --inplace
