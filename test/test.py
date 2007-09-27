#!/usr/bin/env python
# A python script to execute a series of parallel python test scripts for MaroonMPI.
# This script handles either a single test or an entire directory of tests
import sys, os, traceback, string
sys.path.append( os.path.realpath(os.path.join("..")) )
print sys.path
sys.exit()

PASS,FAIL="PASS!","FAIL!"
"""
- ABOUT THIS SCRIPT:

This script runs a long series of MaroonMPI test scripts.

This test handles both MPI and MPE module tests.

An example of what a single test command looks like:

        /usr/bin/mpiexec -l -n 2 /usr/bin/python /home/user/maroonmpi/test/test.py

To handle different MPI environments and implementations you may need to modify
this script.

- MODIFYING THIS SCRIPT (To add tests):

Adding a test is a single step process.  Below you'll find a list with the name:
'testList'.  All you have to do to add a single new testcase is add an element to
'testList' that matches this format:

        line = { 'script':'filename.py',
                 'nprocs': N, #where N is a positive number of processors required for the test
                 'summary': 'a brief summary of the test',
                 'expected': PASS or FAIL} #what we expect this test to do!

Assume that testList is currently:

        testList = [{"script":'passes.py', "nprocs":1, "summary":'passing control test', "expected":PASS},
                    {"script":'fails.py', "nprocs":1, "summary":'failure control test', "expected":FAIL},
                   ]

And you wish to add a new script named 'mytest.py', that requires 8 processors and that does a
simple test of the mpi.reduce average function.  Additionally, you've already run this test and
the associated code so you believe it should work.  This test isn't a reminder of functionality
you would like to implement but actually working code, so you 'expect' it to PASS.
After adding this, testList would look like:

        testList = [{"script":'passes.py', "nprocs":1, "summary":'passing control test', "expected":PASS},
                    {"script":'fails.py', "nprocs":1, "summary":'failure control test', "expected":FAIL},
                    {"script":'mytest.py', "nprocs":8,"summary":'test of mpi.reduces new average op', "expected":PASS},
                   ]

- MODIFYING THIS SCRIPT (For other MPIs):

To modify how tests are run you'll need to find and edit the following variables
to suit your system:

        exe = os.popen( "which mpiexec" ).readline().strip("\n")
        python = os.popen( "which python" ).readline().strip("\n")
        args = ("-l", "-n", "%s"%(numprocs),"%s"%(python),  "%s"%(script),)

'exe' is simply the full path to your systems mpiexec, mpirun, ibrun, etc.
'python' is simply the full path to the python interpreter you installed MaroonMPI on.
'args' is a comma seperated list (strictly speaking, a python tuple) of the arguments
that are passed to 'exe'.

If you are passing no arguments at all you want to set args to an empty tuple '(,)'
However, the no arguments case is really only good for JUST running mpiexec.  Not terribly interesting!

So starting with '(,)' you will need to add arguments.

mpiexec's most basic syntax is simply:

mpiexec program

So 'args' will most likely have to be at least:
        args = ('/the/path/to/the/program/i/want/mpiexec/to/run',)

Note the trailing comma!  It is important that args is a tuple!
"""

"""
 Entries in this list are in the format: {"script":'script.py',"nprocs":N,"summary",''}, ...
 where N is the number of processors to run script.py with.
 Test Scripts should assert they're running on sufficient processors.
"""
# This is now all set in an seperate python file:
#testList = [{"script":'passes.py', "nprocs":1, "summary":'passing control test', "expected":PASS},
#            {"script":'fails.py', "nprocs":1, "summary":'failure control test', "expected":FAIL},
#           ]

def padN( str, N ):
    """
    Returns string 'str' padded to 'N' length with space characters.
    """
    if( len(str) >= N ):
        str = str[:(N-1)] # Take only N-1 characters (this leaves a space between fields)
        str += " "
    else:
        P = N - len(str)
        str += (" " * P)
    return str

try:
    if  ( len(sys.argv) > 2 ):
        # Run the modules specified as arguments:
        modules = sys.argv[1:]
    elif( len(sys.argv) == 2 ):
        # Run the module specified as an argument
        modules = [sys.argv[1],]
    else:
        # Run the default case, just the core module
        modules = ["core",]
        
    mode = os.P_WAIT

    """
    Test list maintains the order or the tests.  We add them to this dictionary to make
    them easier to manage.  I.E. testCases[0] and results[0] will be corresponding values.
    This allows us to lookup information about the test and display it later.
    """
    index = 0
    testModules = {}
    results = {}
    for module in modules:
        testCases = {# TestNumber:{"script":'script.py', "nprocs":N, "summary":''},
            }
        m = __import__(module)
        testList = m.testList
        for test in testList:
            testCases[index] = test
            testCases[index]["script"] = os.path.join( module, testCases[index]["script"])
            index += 1
        testModules[module] = testCases
        results[module] = {}

    for module in testModules.keys():
        testCases = testModules[module] 
        for key in testCases.keys():
            # Unpack testCase info:
            script = os.path.realpath( testCases[key]["script"] )
            numprocs = testCases[key]["nprocs"]

            # Run test case:
            exe = os.popen( "which mpiexec" ).readline().strip("\n")
            python = os.popen( "which python" ).readline().strip("\n")
            args = ("-l", "-n", "%s"%(numprocs),"%s"%(python),  "%s"%(script),)
            print exe,string.join(args," "),": ... ",
            result = os.spawnv( os.P_WAIT, exe, (exe,)+args )

            # Store the results by key:
            results[module][key] = result
            if( results[module][key] == 0 ):
                print PASS
            else:
                print FAIL

    # Testing is finished, output a table of results:
    print "\nSummary of results by module:"
    for module in testModules.keys():
        print padN("Testing Module: %s"%(module),30), padN("Script",20), padN("NPROCS",10),
        print padN("Expected",10), "Result"
        testCases = testModules[module]
        for key in results[module].keys(): 
            if ( results[module][key] == 0 ):
                result = PASS
            else:
                result = FAIL
            # These all print to a single 80 column line:
            print padN(testCases[key]["summary"], 30),
            print padN(testCases[key]["script"],20),
            print padN(str(testCases[key]["nprocs"]),10),
            print padN(testCases[key]["expected"],10),
            print result
        print "\n"
        
except:
    traceback.print_exc()
    print "Usage:  ./run-alltests.py"
