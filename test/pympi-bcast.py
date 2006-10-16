import Numeric
from mpi import pympi as mpi

A=0
if( mpi.rank == 0 ):
    A = Numeric.array(range(100),'i')

B = mpi.bcast(A)
B = mpi.bcast(B,0)
C = mpi.WORLD.bcast(B)
C = mpi.WORLD.bcast(C,0)


print B
print C
