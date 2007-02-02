#!/usr/bin/env python
# A simple python script to mpiexec a parallel python script

"""
This script provides the core functionality for running a test script
on a specific environment (Windows/Linux/Mac OS X) and MPI Library( MPICH1/2, LAM-MPI, OpenMPI, etc )

The platform specific code necessary to run a test is here.
"""

import sys, os, traceback, string

def main( ):
    try:
        numprocs = int(sys.argv[1])
        script = os.path.realpath(sys.argv[2])
        
        mode = os.P_WAIT
        exe = os.popen( "which mpiexec" ).readline().strip("\n")
        python = os.popen( "which python" ).readline().strip("\n")
        args = ("-l", "-n", "%s"%(numprocs),"%s"%(python),  "%s"%(script),)
        command = "mpiexec -l -n %s python %s" % (numprocs, script)
        
        print exe,string.join(args," ")
        
        result = os.spawnv( os.P_WAIT, exe, (exe,)+args )
        print result
        
    except:
        traceback.print_exc()
        print "Usage:  run.py number_of_processors parallel_script.py"

if __name__=="__main__":
    main()
