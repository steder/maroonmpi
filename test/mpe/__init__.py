"""
This file is used by several test scripts to help run automated tests on
MaroonMPI.

This file is used by at least:
      run-allmpitests.py
      run-allmpetests.py
      run-alltests.py
"""

PASS,FAIL="PASS!","FAIL!"


testList = [{"script":'mpe-log.py',"nprocs":2,
             "summary":"simple mpe logging example","expected":PASS},
           ]

