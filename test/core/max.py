"""
Trivial Gather Example

One way to find the max of a large set of numbers by
divide and conquer.
"""

import mpi
import random

def main():
    # Start MPI
    myrank, size = mpi.init()
    # Create a toy dataset:
    data = range( 1, 1001 ) # We know what the max will be already :-)
    random.shuffle( data ) # Modifies data in place

    #  Divide up the problem (if we can divide it evenly)
    if( len(data) % size == 0 ):  
        blocksize = len(data) / size
        start = blocksize * myrank
        end = start + blocksize
        mydata = data[ start : end ]
        max = -1
        for i in mydata:
            if ( i > max ):
                max = i
        maximums = mpi.gather( max, 1, mpi.MPI_INT, size, mpi.MPI_INT, 0,
                                       mpi.MPI_COMM_WORLD)
        if ( myrank == 0 ):
            max = -1
            for i in maximums:
                if ( i > max ):
                    max = i
            print "The maximum value is:",max
    else:
        print "Sorry, I don't know how to split up the problem, aborting!"
    mpi.finalize()
            
if __name__=="__main__":
    main()
