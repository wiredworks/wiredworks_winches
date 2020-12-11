print('Started')

try:
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension


#from distutils.core import setup
from Cython.Build import cythonize
import numpy as np
#import scipy

setup(
  name = 'GrenzVel',
  include_dirs = [np.get_include()],
  ext_modules = cythonize("GrenzVel.pyx",annotate=True),
)