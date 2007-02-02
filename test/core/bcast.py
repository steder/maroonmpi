import sys
import mpi
import Numeric
import unittest

class MPI_Broadcast_TestCase(unittest.TestCase):
    def setUp(self):
        self.rank = mpi.comm_rank(mpi.MPI_COMM_WORLD)
        self.size = mpi.comm_size(mpi.MPI_COMM_WORLD)

    def tearDown(self):
        pass

    def testNil1(self):
        nil1 = mpi.bcast( Numeric.zeros(0,Numeric.Int32), 1, mpi.MPI_INT, 0, mpi.MPI_COMM_WORLD )
        self.assertEqual( [0], nil1 )

    def testSingleChar(self):
        sigma = mpi.bcast( 'g', 1, mpi.MPI_CHAR, 0, mpi.MPI_COMM_WORLD )
        self.assertEqual( Numeric.array(['g'],'c'), sigma )
    def testSingleInt(self):
        sigma = mpi.bcast( 7, 1, mpi.MPI_INT, 0, mpi.MPI_COMM_WORLD )
        self.assertEqual( Numeric.array([7],'i'), sigma )
    def testSingleFloat(self):
        sigma = mpi.bcast( 7.7, 1, mpi.MPI_FLOAT, 0, mpi.MPI_COMM_WORLD )
        self.assertEqual( Numeric.array([7.7],'f'), sigma)
        
    def testSingleDouble(self):
        sigma = mpi.bcast( 7.7, 1, mpi.MPI_DOUBLE, 0, mpi.MPI_COMM_WORLD )
        self.assertEqual( Numeric.array([7.7],'d'), sigma)
        
    def testArrayChar(self):
        gamma = mpi.bcast( ['i','c','d'],3,mpi.MPI_CHAR,0,mpi.MPI_COMM_WORLD )
        self.assertEqual( Numeric.array(['i','c','d'],'c'), gamma )

    def testArrayInt(self):
        gamma = mpi.bcast( [9,3,4],3,mpi.MPI_INT,0,mpi.MPI_COMM_WORLD )
        self.assertEqual( Numeric.array([9,3,4],'i'), gamma )

    def testArrayFloat(self):
        gamma = mpi.bcast( [9.9,3.3,4.4],3,mpi.MPI_FLOAT,0,mpi.MPI_COMM_WORLD )
        self.assertEqual( Numeric.array([9.9,3.3,4.4],'f'), gamma )

    def testArrayDouble(self):
        gamma = mpi.bcast( [9.9,3.3,4.4],3,mpi.MPI_DOUBLE,0,mpi.MPI_COMM_WORLD )
        self.assertEqual( Numeric.array([9.9,3.3,4.4],'d'), gamma )

def suite():
    suite = unittest.TestSuite()
    # suite.addTest(MPI_Broadcast_TestCase("testNil0"))
    suite.addTest(MPI_Broadcast_TestCase("testNil1"))
    suite.addTest(MPI_Broadcast_TestCase("testSingleChar"))
    suite.addTest(MPI_Broadcast_TestCase("testSingleInt"))
    suite.addTest(MPI_Broadcast_TestCase("testSingleFloat"))
    suite.addTest(MPI_Broadcast_TestCase("testSingleDouble"))
    suite.addTest(MPI_Broadcast_TestCase("testArrayChar"))
    suite.addTest(MPI_Broadcast_TestCase("testArrayInt"))
    suite.addTest(MPI_Broadcast_TestCase("testArrayFloat"))
    suite.addTest(MPI_Broadcast_TestCase("testArrayDouble"))
    return suite

if __name__=="__main__":
    try:
        rank, size = mpi.init(len(sys.argv), sys.argv)
        mpi_bcast_suite = suite()
        #result = mpi_bcast_suite.run(unittest.TestResult())
        test_runner = unittest.TextTestRunner()
        result = test_runner.run( mpi_bcast_suite )
        print result
        mpi.finalize()
    except:
        mpi.finalize()
        raise
