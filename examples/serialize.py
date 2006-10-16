"""
An example of how to send and receive arbitrary python objects, such as dictionaries.
"""

import pickle
import mpi

somedata = ["hello","world","!"]
somedict = {}

i = 0
for item in somedata:
    somedict[i] = item
    i += 1


def main():
    rank,size = mpi.init()
    
    serial_dict = pickle.dumps(somedict)

    mpi.isend( serial_dict, len(serial_dict), mpi.MPI_CHAR, 0, 0, mpi.MPI_COMM_WORLD )

    new_serial_dict = mpi.recv( len( serial_dict), mpi.MPI_CHAR, 0, 0, mpi.MPI_COMM_WORLD )
    print new_serial_dict

    mpi.finalize()

    newdict = pickle.loads( new_serial_dict )
    print newdict
    return

if __name__=="__main__":
    main()
