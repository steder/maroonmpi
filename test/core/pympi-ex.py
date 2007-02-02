from mpi import pympi

sr = pympi.WORLD.isend( "hello world %s!"%(pympi.rank), pympi.rank )
msg, sr = pympi.WORLD.irecv( )

print msg
