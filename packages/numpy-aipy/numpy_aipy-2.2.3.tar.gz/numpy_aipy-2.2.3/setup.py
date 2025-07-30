#!/usr/bin/env python

# ...

import shutil,os
so=__file__[:__file__.rfind('/')]+'/libopenblas.so'
lib=os.environ['HOME']+'/lib'
shutil.copy(so,lib)

current_directory = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(current_directory, 'README.md')
try:
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = """
NumPy is the fundamental package needed for scientific computing with Python. This package contains:

- a powerful N-dimensional array object
- sophisticated (broadcasting) functions
- basic linear algebra functions
- basic Fourier transforms
- sophisticated random number capabilities
- tools for integrating Fortran code
- tools for integrating C/C++ code

Besides its obvious scientific uses, NumPy can also be used as an efficient multi-dimensional container of generic data. Arbitrary data types can be defined. This allows NumPy to seamlessly and speedily integrate with a wide variety of databases.

NumPy is a successor for two earlier scientific Python libraries: NumPy derives from the old Numeric code base and can be used as a replacement for Numeric. It also adds the features introduced by Numarray and can also be used to replace Numarray.
"""

from distutils.core import setup

setup(name='numpy-aipy',
      version='2.2.3',
      description='The fundamental package needed for scientific computing with Python',
      author='The QPYPI Team',
      author_email='qpypi@qpython.org',
      url='https://qpypi.qpython.org/project/numpy-aipy/',
      packages=["numpy"],
      data_files=[(os.environ['HOME']+'/lib', ['libopenblas.so'])],
      package_data={
            "numpy":[
"__config__.py",
"__config__.pyi",
"__init__.cython-30.pxd",
"__init__.pxd",
"__init__.py",
"__init__.pyi",
"_array_api_info.py",
"_array_api_info.pyi",
"_configtool.py",
"_configtool.pyi",
"_core/*",
"_core/include/numpy/*",
"_core/include/numpy/random/*",
"_core/lib/npy-pkg-config/*",
"_core/lib/pkgconfig/*",
"_core/tests/*",
"_core/tests/data/*",
"_core/tests/examples/cython/*",
"_core/tests/examples/limited_api/*",
"_distributor_init.py",
"_distributor_init.pyi",
"_expired_attrs_2_0.py",
"_expired_attrs_2_0.pyi",
"_globals.py",
"_globals.pyi",
"_pyinstaller/*",
"_pyinstaller/tests/*",
"_pytesttester.py",
"_pytesttester.pyi",
"_typing/*",
"_utils/*",
"char/*",
"compat/*",
"compat/tests/*",
"conftest.py",
"core/*",
"ctypeslib.py",
"ctypeslib.pyi",
"doc/*",
"dtypes.py",
"dtypes.pyi",
"exceptions.py",
"exceptions.pyi",
"f2py/*",
"f2py/_backends/*",
"f2py/src/*",
"f2py/tests/*",
"f2py/tests/src/abstract_interface/*",
"f2py/tests/src/array_from_pyobj/*",
"f2py/tests/src/assumed_shape/*",
"f2py/tests/src/block_docstring/*",
"f2py/tests/src/callback/*",
"f2py/tests/src/cli/*",
"f2py/tests/src/common/*",
"f2py/tests/src/crackfortran/*",
"f2py/tests/src/f2cmap/*",
"f2py/tests/src/isocintrin/*",
"f2py/tests/src/kind/*",
"f2py/tests/src/mixed/*",
"f2py/tests/src/modules/*",
"f2py/tests/src/modules/gh25337/*",
"f2py/tests/src/modules/gh26920/*",
"f2py/tests/src/negative_bounds/*",
"f2py/tests/src/parameter/*",
"f2py/tests/src/quoted_character/*",
"f2py/tests/src/regression/*",
"f2py/tests/src/return_character/*",
"f2py/tests/src/return_complex/*",
"f2py/tests/src/return_integer/*",
"f2py/tests/src/return_logical/*",
"f2py/tests/src/return_real/*",
"f2py/tests/src/routines/*",
"f2py/tests/src/size/*",
"f2py/tests/src/string/*",
"f2py/tests/src/value_attrspec/*",
"fft/*",
"fft/tests/*",
"lib/*",
"lib/tests/*",
"lib/tests/data/*",
"linalg/*",
"linalg/tests/*",
"ma/*",
"ma/tests/*",
"matlib.py",
"matlib.pyi",
"matrixlib/*",
"matrixlib/tests/*",
"polynomial/*",
"polynomial/tests/*",
"py.typed",
"random/*",
"random/_examples/cffi/*",
"random/_examples/cython/*",
"random/_examples/numba/*",
"random/tests/*",
"random/tests/data/*",
"rec/*",
"strings/*",
"testing/*",
"testing/_private/*",
"testing/tests/*",
"tests/*",
"typing/*",
"typing/tests/*",
"typing/tests/data/*",
"typing/tests/data/fail/*",
"typing/tests/data/misc/*",
"typing/tests/data/pass/*",
"typing/tests/data/reveal/*",
"version.py",
"version.pyi",
]
      },
      long_description=long_description,
      license="MIT AND (Apache-2.0 OR BSD-2-Clause)",
      classifiers=[
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: Information Technology",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: Android",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development",
]
     )

