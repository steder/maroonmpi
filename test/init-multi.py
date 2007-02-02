import sys
import mpi

def main():
    mpi.init(len(sys.argv), sys.argv)
    mpi.init(len(sys.argv), sys.argv)
    mpi.finalize()

if __name__=="__main__":
    main()
