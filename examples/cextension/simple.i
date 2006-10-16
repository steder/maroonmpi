%module simplempi
int getsize();
int getrank();

/* Yes, the type here is INT instead of MPI_Comm.  Nearly all MPI types
 can be represented simply as integers 

    Additionally: this typemap is required to force the conversion 
    from a Python type to an integer type.

    i.e.:  MMPI Communicator objects have a __int__ method that defines
    how to convert them to integers (the real C MPI_Comm handle).  
    However, SWIG does not automatically request this conversion any
    longer, so we can force this behavior with the typemap.
*/

%typemap(in) (int comm) {
  $1 = (int) PyInt_AsLong($input);
};

int getrankfromcomm(int comm);
int getsizefromcomm(int comm);