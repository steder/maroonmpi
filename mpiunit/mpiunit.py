#! /usr/bin/env python
"""
MPI programs need to be run in their own process to prevent errors from crashing the test suite.
"""
import sys,os

class Test:
    def __init__( self ):
        pass

    def setup( self ):
        pass

    def teardown(self):
        pass

    def run( self, test ):
        f = self.tests[ test ]
        # spawn thread/process and execute setUp
        # tearDown, and test.
            
    def runall( self ):
        pass


    
