#mpe-log.py
import mpi
from mpi import mpe

INIT_EVENT    = 1
BARRIER_EVENT = 0
EVENT_COUNTER = 0

rank,size = mpi.init()
mpe.init_log()
mpe.log_event(INIT_EVENT,EVENT_COUNTER,"After Init...")

mpe.log_event(BARRIER_EVENT,EVENT_COUNTER,"Before Barrier...")
EVENT_COUNTER+=1
mpi.barrier(mpi.MPI_COMM_WORLD)
mpe.log_event(BARRIER_EVENT,EVENT_COUNTER,"After Barrier!")
EVENT_COUNTER+=1
mpe.describe_state(0,1,"full run","blue")

mpe.log_event(INIT_EVENT,EVENT_COUNTER,"Before finalize...")

mpe.describe_event(INIT_EVENT,"Init/Finalize Event","red")
mpe.describe_event(BARRIER_EVENT,"Barrier Event","green")
mpe.finish_log("mpe-test.log")
mpi.finalize()
