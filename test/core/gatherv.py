import Numeric as nm
import mpi

mpi.init()
rank = mpi.comm_rank( mpi.MPI_COMM_WORLD )
size = mpi.comm_size( mpi.MPI_COMM_WORLD )
root = 0

message = [rank] * (size+rank)
print "Sending:",message

recvcounts = mpi.gather( len(message),1,mpi.MPI_INT,
                         1, mpi.MPI_INT,
                         root,mpi.MPI_COMM_WORLD)

displacements = [0]
for i in recvcounts[:-1]:
    displacements.append( i )
    
result = mpi.gatherv( message, len(message), mpi.MPI_INT,
             recvcounts, displacements, mpi.MPI_INT,
             root, mpi.MPI_COMM_WORLD )
if(rank == root):
    print "Received:",result
    
mpi.finalize()
