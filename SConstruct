#!/usr/bin/env python
# Edit these variables to taste:
COMPILER="/usr/local/bin/mpicc"
INCLUDES=[".","/usr/local/include","/usr/include/python2.4"]
FLAGS='-fPIC -O2'
DEBUG_FLAGS='-g -fPIC -Wall -ansi'# -pedantic
DEBUG=True

# Don't modify below this line, please!
# Fine, but if it breaks you get to keep both pieces!
import sys,os

print "About this python..."
print "Python:",sys.executable
print "Version:",sys.version

Help("""
Type: 'scons release' to build the production version of the MMPI module,
          'scons debug' to build the debug version.
          """)

# Allows us to modify the environment, the compiler, compiler options, etc
release = Environment(CC = COMPILER,
                    CCFLAGS = FLAGS)
debug = Environment(CC = COMPILER,
                    CCFLAGS = DEBUG_FLAGS) 

# Print all the environment variables:
#dict = env.Dictionary()
#keys = dict.keys()
#keys.sort()
#for key in keys:
#    print "construction variable = '%s', value = '%s'" % (key, dict[key])

# CPPPATH tells SCons to look in this directory for any header files and watch
# them for changes.
if DEBUG:
    debug = debug.SharedLibrary('_mpi', ['mmpi_module.c'],CPPPATH=INCLUDES)
else:
    release = release.SharedLibrary('_mpi', ['mmpi_module.c'],CPPPATH=INCLUDES)
