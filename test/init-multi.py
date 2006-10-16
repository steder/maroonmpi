# Standard Python Modules
import sys
import unittest

# Code to test:
import mpi

# Test Cases:
class TestInitTwice( unittest.TestCase ):
    def setUp( self ):
        pass
        
    def tearDown( self ):
        pass

    def testMultiInit( self ):
        rank, size = mpi.init( len(sys.argv), sys.argv )
        self.assertRaises(mpi.mpiException, mpi.init, len(sys.argv), sys.argv )
        mpi.finalize()

if __name__=="__main__":
    unittest.main()
