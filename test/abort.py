"""
Extremely simple MPI program.

Acts as a control to help calibrate the test system.

This must *fail*, and the counterpart to this file 'init.py'
must *pass*.

If one or the other of these files fails to produce the expected result
then there is likely something wrong with either the module or the MPI
environment.
"""
import mpi
import sys
import os

rank, size = mpi.init( len(sys.argv), sys.argv )
print "(%s,%s): initialized..." %(rank,size)

returnCode = 1

if ( rank == 0 ):
    file = open("fails.py.out","a")
    file.write( "My return code is %s\n"%returnCode )
    file.close()
    mpi.barrier(mpi.MPI_COMM_WORLD)    
    mpi.abort(mpi.MPI_COMM_WORLD, returnCode)
else:
    mpi.barrier(mpi.MPI_COMM_WORLD)

mpi.finalize()
