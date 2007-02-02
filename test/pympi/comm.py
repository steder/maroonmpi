import Numeric
from mpi import pympi as mpi

evencomm, oddcomm = None, None

if( mpi.rank % 2 == 0 ):
    evencomm = mpi.comm_split( 0 )
else:
    oddcomm = mpi.comm_split(1)

# the above is equivalent to:
if( mpi.rank % 2 == 0 ):
    evencomm = mpi.WORLD.comm_split(0)
else:
    oddcomm = mpi.WORLD.comm_split(1)


if evencomm:
    print "%d=evencomm.comm_size()"%(evencomm.comm_size())
    print "%d=evencomm.comm_rank()"%(evencomm.comm_rank())
if oddcomm:
    print "%d=oddcomm.comm_size()"%(oddcomm.comm_size())
    print "%d=oddcomm.comm_rank()"%(oddcomm.comm_rank())
