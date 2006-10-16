import sys,mpi
import Numeric
import unittest

class MPI_SendRecv_TestCase(unittest.TestCase):
    single_char = 'Q'
    single_int = 7
    single_float = 7.7
    single_double = double(7.7)
    array_1D_char = Numeric.array(['a','b','c','d','e','f','g','h','i','j',
                                                                 'k','l','m','n','o','p','q','r','s','t',
                                                                 'u','v','w','x','y','z'], 'c' )
    array_1D_int    = Numeric.array(range(100),'i')
    array_1D_float = Numeric.array(range(100),'f')
    array_1D_double = Numeric.array(range(100),'d')
    array_2D_int = Numeric.ones( (10,10), 'i' )
    def setUp(self):
        self.rank = mpi.comm_rank( mpi.MPI_COMM_WORLD )
        self.size = mpi.comm_size( mpi.MPI_COMM_WORLD )
    def tearDown(self):
        pass

    

def suite():
    suite = unittest.TestSuite()
    # suite.addTest(MPI_SendRecv_TestCase("testMethodName"))
    return suite

if __name__=="__main__":
    try:
        rank, size = mpi.init(len(sys.argv), sys.argv)
        mysuite = suite()
        test_runner = unittest.TextTestRunner()
        result = test_runner.run( mysuite )
        print result
        mpi.finalize()
    except:
        mpi.finalize()
        raise
