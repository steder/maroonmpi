"""
This file is used by several test scripts to help run automated tests on
MaroonMPI.

This file is used by at least:
      run-allmpitests.py
      run-allmpetests.py
      run-alltests.py
"""

PASS,FAIL="PASS!","FAIL!"


testList = [{"script":'init.py', "nprocs":1, "summary":'passing test(control)', "expected":PASS},
            {"script":'abort.py', "nprocs":1, "summary":'failure test(control)', "expected":FAIL},
            ### BEGIN CORE TESTS ###
            # Verify this behavior fails
            {"script":'init-multi.py', "nprocs":1, "summary":'attempts to init mpi twice', "expected":FAIL},

            # Non-blocking sends
            {"script":'isend-1process.py',"nprocs":1,
             "summary":"non-blocking send test","expected":PASS},
            {"script":'isend-2process.py',"nprocs":2,
             "summary":"non-blocking send test","expected":PASS},
            {"script":'isend-2process-wait.py',"nprocs":2,
             "summary":"non-blocking send test w/wait","expected":PASS},
            {"script":'isend-2process.py',"nprocs":2,
             "summary":"non-blocking send test w/test","expected":PASS},
           ]

