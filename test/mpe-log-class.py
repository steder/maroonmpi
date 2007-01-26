#mpe-log-class.py
import mpi
from mpi import mpe
import Numeric

rank,size = mpi.init()
assert (size == 2), "This example requires 2 processors to run properly!"

logfile = mpe.Log("test2")
runEventStart = mpe.log_get_event_number()
runEventEnd = mpe.log_get_event_number()
sendEventStart = mpe.log_get_event_number()
sendEventEnd = mpe.log_get_event_number()
recvEventStart = mpe.log_get_event_number()
recvEventEnd = mpe.log_get_event_number()
sleepEventStart = mpe.log_get_event_number()
sleepEventEnd = mpe.log_get_event_number()

logfile.describe_state( runEventStart, runEventEnd, "Full Runtime", "blue" )
logfile.describe_state( sendEventStart, sendEventEnd, "send", "red" )
logfile.describe_state( recvEventStart, recvEventEnd, "recv", "green" )
logfile.describe_state( sleepEventStart, sleepEventEnd, "sleep", "turquoise" )

logfile.log_event( runEventStart, rank, "starting run")
# Let's send and receive a 100 messages and generate 100(200?) events.
for i in xrange(100):
    if( rank == 0 ):
        # Generate 100 numbers, send them to rank 1
        logfile.log_event( sendEventStart, i, "start send" )
        data = Numeric.array( range(10000), Numeric.Int32 )
        mpi.send( data, 10000, mpi.MPI_INT, 1, i, mpi.MPI_COMM_WORLD )
        logfile.log_event( sendEventEnd, i, "end send")
    else:
        logfile.log_event( recvEventStart, i, "start recv" )
        rdata = mpi.recv( 10000, mpi.MPI_INT, 0, i, mpi.MPI_COMM_WORLD )
        logfile.log_event( recvEventEnd, i, "end recv" )
    if( i == 50 ):
        logfile.log_event( sleepEventStart, i, "start sleep" )
        time.sleep(1)
        mpi.barrier( mpi.MPI_COMM_WORLD )
        logfile.log_event( sleepEventEnd, i, "end sleep")

logfile.log_event( runEventEnd, rank, "stopping run")
logfile.finish_log("test1")

mpi.finalize()
