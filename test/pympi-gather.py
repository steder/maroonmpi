import Numeric
from mpi import pympi as mpi

# Requires 2 or more processors to be relevant
assert mpi.size > 1

# Simple Case:
ids = mpi.gather( mpi.rank )
if(mpi.rank == 0):
    print ids

## Multiple Element Case:
ids = mpi.gather( [mpi.rank]*mpi.size )
if(mpi.rank == 0):
    print ids

# Multiple Element Case (different size lists):
ids = mpi.gather( [mpi.rank]*(mpi.rank+1) )
if(mpi.rank == 0):
    print ids
