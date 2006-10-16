import Numeric
from mpi import pympi as mpi

assert mpi.size >= 2

A = Numeric.array(range(100),'i')

if( mpi.rank == 0 ):
    mpi.send( A, 1 )
elif( mpi.rank == 1 ):
    B = mpi.recv( 0 )
else:
    pass

if( mpi.rank == 1 ):
    print "B=",B
