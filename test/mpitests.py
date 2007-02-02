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

            ### BEGIN Array-specific tests
            {"script":'array-send-recv.py',"nprocs":2,
             "summary":"special array send/recv test","expected":PASS},
            {"script":'array-bcast.py',"nprocs":2,
             "summary":"special array bcast test","expected":PASS},
            {"script":'array-gather.py',"nprocs":2,
             "summary":"special array gather test","expected":PASS},

            ### BEGIN 'Pythonic' interface tests
            {"script":'pythonic-bcast.py',"nprocs":2,
             "summary":"user-friendly bcast test","expected":PASS},

            ### BEGIN 'Pympi' interface tests
            {"script":'pympi-init.py',"nprocs":2,
             "summary":"pympi-style init test","expected":PASS},
            {"script":'pympi-barrier.py',"nprocs":2,
             "summary":"pympi-style barrier test","expected":PASS},
            {"script":'pympi-bcast.py',"nprocs":2,
             "summary":"pympi-style bcast test","expected":PASS},
            {"script":'pympi-comm.py',"nprocs":2,
             "summary":"pympi-style communicator test","expected":PASS},
            {"script":'pympi-comm-slice.py',"nprocs":2,
             "summary":"pympi-style comm slicing test","expected":PASS},
            {"script":'pympi-gather.py',"nprocs":2,
             "summary":"pympi-style gather test","expected":PASS},
            {"script":'pympi-reduce.py',"nprocs":2,
             "summary":"pympi-style reduce test","expected":PASS},
            {"script":'pympi-send-recv.py',"nprocs":2,
             "summary":"pympi-style send/recv test","expected":PASS},
           ]

