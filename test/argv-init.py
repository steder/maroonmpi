#!/usr/bin/env python
import sys
import mpi

def main():
    print sys.argv
    rank, size = mpi.init()
    print "size: %d, rank: %d" % (size, rank)
    print sys.argv
    mpi.finalize()

if __name__ == "__main__":
    main()
