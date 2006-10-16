#!/usr/bin/env python
# A simple python script to mpiexec
# an MMPI test script.

import sys, os


try:
    numprocs = int(sys.argv[1])
    script = os.path.realpath(sys.argv[2])
    mode = os.P_WAIT
    #exe = "/usr/bin/mpiexec"
    exe = "/usr/bin/python"
    #args = "-l","-n",numprocs,"python",script
    args = (script)
    returncode = os.spawnv( mode, exe, args )
    print returncode

except:
    print "Usage:  run.py number_of_processors parallel_script.py"
    
    


