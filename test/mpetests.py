"""
This file is used by several test scripts to help run automated tests on
MaroonMPI.

This file is used by at least:
      run-allmpitests.py
      run-allmpetests.py
      run-alltests.py
"""

PASS,FAIL="PASS!","FAIL!"

testList = [{"script":'passes.py', "nprocs":1, "summary":'passing test(control)', "expected":PASS},
            {"script":'fails.py', "nprocs":1, "summary":'failure test(control)', "expected":FAIL},
           ]
