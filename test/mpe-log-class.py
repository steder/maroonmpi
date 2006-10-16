#mpe-log-class.py
import mpi
from mpi import mpe

INIT_EVENT    = 1
BARRIER_EVENT = 0
EVENT_COUNTER = 0

rank,size = mpi.init()
logfile = mpe.Log("mpe-test.log")
logfile.log_event( INIT_EVENT, EVENT_COUNTER, "After Init..." )
logfile.log_event(BARRIER_EVENT,EVENT_COUNTER,"Before Barrier...")
EVENT_COUNTER+=1
mpi.barrier(mpi.MPI_COMM_WORLD)
logfile.log_event(BARRIER_EVENT,EVENT_COUNTER,"After Barrier!")
EVENT_COUNTER+=1
logfile.describe_state(0,1,"full run","blue")

logfile.log_event(INIT_EVENT,EVENT_COUNTER,"Before finalize...")

logfile.describe_event(INIT_EVENT,"Init/Finalize Event","red")
logfile.describe_event(BARRIER_EVENT,"Barrier Event","green")
logfile.finish_log("mpe-test.log")

logfile.displayEvents()
logfile.displayStates()
logfile.displayEventDescriptions()

mpi.finalize()
