#!/usr/bin/python
"""
Trivial Gather Example

One way to find the max of a large set of numbers by
divide and conquer.
"""

import mpi
import random

problemlength = 1000
    
def main():
    myrank, size = mpi.init()

    # split the problem in chunks

    if problemlength % size == 0:
        blocksize = problemlength / size
    else:
        print "Sorry, I don't know how to split up the problem, aborting!"
        mpi.finalize()
        
    if myrank == 0:
        data = range(1,problemlength + 1)  # create a toy dataset...
        random.shuffle(data)               # ...modifies data in place

        mydata = data[0:blocksize] # get some data for me...
                                   # and communicate the rest to slaves

        for host in range(1,size):
            hisdata = data[blocksize*host:blocksize*(host+1)]
            mpi.send(hisdata,blocksize,mpi.MPI_INT,host,0,mpi.MPI_COMM_WORLD)
    else:
        mydata = mpi.recv(blocksize,mpi.MPI_INT,0,0,mpi.MPI_COMM_WORLD)

    mymax = max(mydata)

    maximums = mpi.gather(mymax,1,mpi.MPI_INT, size, mpi.MPI_INT, 0, mpi.MPI_COMM_WORLD)

    if myrank == 0:
        mymax = max(maximums)
        print "The maximum value is:", mymax

    mpi.finalize()            

if __name__=="__main__":
    main()

