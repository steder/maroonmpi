"""
This file is used by several test scripts to help run automated tests on
MaroonMPI.

This file is used by at least:
      run-allmpitests.py
      run-allmpetests.py
      run-alltests.py
"""

PASS,FAIL="PASS!","FAIL!"


testList = [
            ### BEGIN Array-specific tests
            {"script":'array-send-recv.py',"nprocs":2,
             "summary":"special array send/recv test","expected":PASS},
            {"script":'array-bcast.py',"nprocs":2,
             "summary":"special array bcast test","expected":PASS},
            {"script":'array-gather.py',"nprocs":2,
             "summary":"special array gather test","expected":PASS},

            ]

