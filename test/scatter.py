import sys, os
import Numeric
import mpi

if __name__=="__main__":
    rank,size = mpi.init()
    if(size >= 2):
        print "testing scatter on",size,"processors..."
    else:
        print "unable to run test on",size,"processors!"
        print "please rerun on 2 or more processors."
        sys.exit()
    print "\n"
    print "allocating test data:"

    data = 0
    if(rank==0):
        data = Numeric.array("abcdefghijklmnopqrst",Numeric.Character)

    print "scattering data:"
    mydata = mpi.scatter(data, 10, mpi.MPI_CHAR, 10, mpi.MPI_CHAR,
                         0, mpi.MPI_COMM_WORLD)
    print "scattered data:",mydata
    mpi.barrier(mpi.MPI_COMM_WORLD)
    mpi.finalize()
