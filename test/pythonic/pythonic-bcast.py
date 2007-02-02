import mpi
import Numeric as nm

rank,size = mpi.init()
#atexit.register(mpi.finalize)

import mpi.pythonic
test = mpi.pythonic.bcast( 0 )
print test
test = mpi.pythonic.bcast( 1.0 )
print test
test = mpi.pythonic.bcast( "a" )
print test
test = mpi.pythonic.bcast( 'b' )
print test
test = mpi.pythonic.bcast( "hello" )
print test
test = mpi.pythonic.bcast( (1,2,3) )
print test
test = mpi.pythonic.bcast( [1,2,3,4,5,6,7,8,9,10] )
print test
test = mpi.pythonic.bcast( [1.0,2.0,3.0,4.0,5.0] )
print test
test = mpi.pythonic.bcast( nm.array([1,2,3,4,5],nm.Int32) )
print test
test = mpi.pythonic.bcast( nm.array([[1,2,3,4,5],[6,7,8,9,0]],nm.Int32) )
print test
test = mpi.pythonic.bcast( ["hello","mpi","world"] )
print test
test = mpi.pythonic.bcast( mpi.finalize )
print test
test()
