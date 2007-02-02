from mpi import pympi as mpi

# Test Slice Notation:
print "Even processor ids:",mpi.WORLD[0::2]
print "Odd processor ids:",mpi.WORLD[1::2]

# Use it to create new communicators (the primary use for it):

evencomm = mpi.comm_create( mpi.WORLD[0::2] )
oddcomm = mpi.comm_create( mpi.WORLD[1::2] )

if(evencomm):
    print "%d = evencomm.size()"%(evencomm.size())
if(oddcomm):
    print "%d = oddcomm.size()"%(oddcomm.size())
