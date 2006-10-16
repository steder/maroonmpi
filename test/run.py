#!/usr/bin/env python
# A simple python script to mpiexec a parallel python script

import sys, os

try:
    numprocs = int(sys.argv[1])
    script = os.path.realpath(sys.argv[2])

    result = os.popen( "mpiexec -l -n %s python %s" % (numprocs, script) ).read()
    
    print result
    
except:
    print "Usage:  run.py number_of_processors parallel_script.py"
