import Numeric as nm
from mpi import pympi as mpi

assert mpi.size > 1

def average( alist ):
    n = len(alist)
    s = 0
    for a in alist:
        s += a
    return (s/(n*1.0))

def calcsum( alist ):
    s = 0
    for a in alist:
        s += a
    return s


ave = mpi.WORLD.reduce( mpi.rank, average )
s = mpi.WORLD.reduce( mpi.rank, calcsum )

print "ave:",ave
print "s:",s
