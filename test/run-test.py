#!/usr/bin/env python
# A simple python script to mpiexec a parallel python script

import sys, os, traceback, string

try:
    numprocs = int(sys.argv[1])
    script = os.path.realpath(sys.argv[2])

    mode = os.P_WAIT
    exe = os.popen( "which mpiexec" ).readline().strip("\n")
    python = os.popen( "which python" ).readline().strip("\n")
    args = ("-l", "-n", "%s"%(numprocs),"%s"%(python),  "%s"%(script),)
    command = "mpiexec -l -n %s python %s" % (numprocs, script)

    print exe,string.join(args," ")
    
    #result = os.popen( command ).read()

    #result = os.spawnv( mode, exe, args )

    #exe = os.popen( "which touch" ).readline().strip("\n")
    #args = ("spawnv.out",)

    result = os.spawnv( os.P_WAIT, exe, (exe,)+args )
    print result
    
except:
    traceback.print_exc()
    print "Usage:  run.py number_of_processors parallel_script.py"
