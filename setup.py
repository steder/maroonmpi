#!/usr/bin/env python

import sys, os, glob

from distutils.core import setup, Extension
from distutils.sysconfig import get_python_inc, get_python_lib
import distutils.unixccompiler

# process special arguments; these are default values

# /somepath/include/python2.4/Numeric
# /somepath/include/python2.4/Numarray
# /somepath/include/python2.4/numpy
# The last element of the above 3 paths
# are possible values for "array_prefix"
array_prefix = ''
mpicc_bin = 'mpicc'

argv_replace = []

# Default array implementation:
array_lower,array_prefix="numpy","numpy"
enable_mpe=False

for arg in sys.argv:
    if arg.startswith('--with-array='):
        array_prefix = arg.split('=', 1)[1]
        array_lower = array_prefix.lower()
    elif arg.startswith('--with-mpicc='):
        mpicc_bin = arg.split('=', 1)[1]
    elif arg.startswith('--enable-mpe'):
        enable_mpe = True
    else:
        argv_replace.append(arg)

sys.argv = argv_replace

# this will handle most of the compiler calls, using mpicc_bin

os.environ["CC"]=mpicc_bin

# hack into distutils to replace the compiler in "linker_so" with mpicc_bin

class MPI_UnixCCompiler(distutils.unixccompiler.UnixCCompiler):
    __set_executable = distutils.unixccompiler.UnixCCompiler.set_executable

    def set_executable(self,key,value):
        if key == 'linker_so' and type(value) == str:
            value = mpicc_bin + ' ' + ' '.join(value.split()[1:])

        return self.__set_executable(key,value)
    
distutils.unixccompiler.UnixCCompiler = MPI_UnixCCompiler

# now go on and do the actual setup

SOURCE = ["src/mmpi_module.c"]

if( array_lower == "numeric" ):
    INCLUDES = [os.path.join( get_python_inc(), array_prefix ),
                ]
elif( array_lower == "numpy" ):
    INCLUDES = [os.path.join( get_python_lib(), array_prefix, "core", "include", "numpy" ),
                ]
else:
    INCLUDES = [os.path.join( get_python_inc(), array_prefix ),
                os.path.join( get_python_lib(), array_prefix, "core", "include", "numpy" ),
                ]
    
MPESOURCE = ["src/mpe_module.c"]
LIBRARIES = ["mpe"]

print 'Setting MMPI setup with Python ',sys.executable,', version ',sys.version

if( enable_mpe ):
    extension_modules = [Extension('_mpi', SOURCE, include_dirs=INCLUDES),
                         Extension('_mpe', MPESOURCE, include_dirs=INCLUDES, libraries=LIBRARIES),
                         ]
else:
    extension_modules = [Extension('_mpi', SOURCE, include_dirs=INCLUDES),
                         ]

setup(name='MaroonMPI',
      version='1.1',
      description='Lightweight MPI module for Python 2.4+',
      long_description='',
      author='Mike Steder',
      author_email='steder@gmail.com',
      packages=['lib'],
      ext_package='mpi',
      ext_modules=extension_modules,
      )

