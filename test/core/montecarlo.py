"""
This example approxiamates PI using a monte carlo simulation.
"""

import mpi
import random

def computePi( size, nsamples):
    oldpi, pi, mypi,pisum = 0.0,0.0,0.0,0.0
    done = False
    
    inside = 0
    # Monte Carlo bit
    for i in xrange(nsamples):
        x = random.random()
        y = random.random()
        if ((x*x)+(y*y)<1):
            inside+=1
    # 
    sum_inside = mpi.allreduce(inside, 1, mpi.MPI_INT, mpi.MPI_SUM, mpi.MPI_COMM_WORLD) 
    # The "* 4" is needed because we're computing the number of points inside
    # a QUARTER unit circle.  So we're really computing (PI / 4).
    pi = ( sum_inside[0] / (nsamples*size*1.0) ) * 4
    return pi

if __name__=="__main__":
    rank, size = mpi.init()
    # More sample points should make a more accurate value for pi.
    pi = computePi( size, 10000 )
    if(rank==0):
        print "Computed value of pi on",size,"processors is",pi
    mpi.finalize()

