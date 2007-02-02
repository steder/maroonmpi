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
            {"script":'init.py',"nprocs":2,
             "summary":"pympi-style init test","expected":PASS},
            {"script":'barrier.py',"nprocs":2,
             "summary":"pympi-style barrier test","expected":PASS},
            {"script":'bcast.py',"nprocs":2,
             "summary":"pympi-style bcast test","expected":PASS},
            {"script":'comm.py',"nprocs":2,
             "summary":"pympi-style communicator test","expected":PASS},
            {"script":'comm-slice.py',"nprocs":2,
             "summary":"pympi-style comm slicing test","expected":PASS},
            {"script":'gather.py',"nprocs":2,
             "summary":"pympi-style gather test","expected":PASS},
            {"script":'reduce.py',"nprocs":2,
             "summary":"pympi-style reduce test","expected":PASS},
            {"script":'send-recv.py',"nprocs":2,
             "summary":"pympi-style send/recv test","expected":PASS},
           ]

