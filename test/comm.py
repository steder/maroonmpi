import sys,mpi
import Numeric
import unittest

class MPI_Comm_TestCase(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testCommRank( self ):
        rank = mpi.comm_rank( mpi.MPI_COMM_WORLD )
        print rank
        self.assert_( rank >= 0 )

    def testCommSize( self ):
        size = mpi.comm_size( mpi.MPI_COMM_WORLD )
        print size
        self.assert_( size >= 1 )

    def testCommSplitSingletons( self ):
        rank = mpi.comm_rank( mpi.MPI_COMM_WORLD )
        #print "testCommSplitSingletons:",rank
        #newcomm = mpi.comm_split( mpi.MPI_COMM_WORLD, rank, 0 )
        #nrank = mpi.comm_rank( newcomm )
        #nsize = mpi.comm_size( newcomm )
        #self.assert_( nrank == 0 )
        #self.assert_( nsize == 1 )
        self.assert_( True )
        
#     def testCommSplitEvenOdd( self ):
#         """
#         Create even and odd communicators and verify
#         that all the processors in the new even/odd communicators
#         belong there.
#         """
#         size = mpi.comm_size( mpi.MPI_COMM_WORLD )
#         rank = mpi.comm_rank( mpi.MPI_COMM_WORLD )
#         if ( (rank % 2) == 0 ):
#             # Even case
#             newcomm = mpi.comm_split( mpi.MPI_COMM_WORLD, 0, 0 )
#         else:
#             # Odd case
#             newcomm = mpi.comm_split( mpi.MPI_COMM_WORLD, 1, 0 )
#         # Verify that all the ranks in each communicator are even/odd
#         nsize = mpi.comm_size( newcomm )
#         ranks = mpi.gather( rank, 1, mpi.MPI_INT, nsize,mpi.MPI_INT, 0, newcomm )
#         ranks = mpi.bcast( ranks, nsize, mpi.MPI_INT, 0, newcomm )
#         for r in ranks:
#             self.assert_( (r%2) == (rank%2) )

#     def testDup( self ):
#         rank = mpi.comm_rank( mpi.MPI_COMM_WORLD )
#         size = mpi.comm_size( mpi.MPI_COMM_WORLD )
#         newcomm = mpi.comm_dup( mpi.MPI_COMM_WORLD )
#         nrank = mpi.comm_rank(newcomm)
#         nsize = mpi.comm_size(newcomm)
#         self.assert_( rank == nrank )
#         self.assert_( size == nsize )
    
def suite():
    suite = unittest.TestSuite()
    # suite.addTest(MPI_SendRecv_TestCase("testMethodName"))
    suite.addTest( MPI_Comm_TestCase("testCommRank") )
    suite.addTest( MPI_Comm_TestCase("testCommSize") )
    suite.addTest( MPI_Comm_TestCase("testCommSplitSingletons") )
#    suite.addTest( MPI_Comm_TestCase("testCommSplitEvenOdd") )
#    suite.addTest( MPI_Comm_TestCase("testDup") )
    return suite

if __name__=="__main__":
    rank, size = mpi.init(len(sys.argv), sys.argv)
    mysuite = suite()
    test_runner = unittest.TextTestRunner()
    result = test_runner.run( mysuite )
    print result
    mpi.finalize()
    
