"""
This file is used by several test scripts to help run automated tests on
MaroonMPI.

This file is used by at least:
      run-allmpitests.py
      run-allmpetests.py
      run-alltests.py
"""

PASS,FAIL="PASS!","FAIL!"


testList = [            ### BEGIN 'Pythonic' interface tests
            {"script":'pythonic-bcast.py',"nprocs":2,
             "summary":"user-friendly bcast test","expected":PASS},

           ]

